import os
import time
import datetime
import numpy as np
import tensorflow as tf
from tensorflow.contrib import learn

from text_cnn import TextCNN
import data_helpers

# Parameters
# ==================================================

# Data loading params
tf.flags.DEFINE_float("dev_sample_percentage", .1, "Percentage of the training data to use for validation")
tf.flags.DEFINE_string("positive_data_file", "./data/rt-polaritydata/rt-polarity.pos", "Data source for the positive data.")
tf.flags.DEFINE_string("negative_data_file", "./data/rt-polaritydata/rt-polarity.neg", "Data source for the negative data.")

# Model Hyperparameters
tf.flags.DEFINE_integer("embedding_dim", 128, "Dimensionality of character embedding (default: 128)")
tf.flags.DEFINE_string("filter_sizes", "3,4,5", "Comma-separated filter sizes (default: '3,4,5')")
tf.flags.DEFINE_integer("num_filters", 128, "Number of filters per filter size (default: 128)")
tf.flags.DEFINE_float("dropout_keep_prob", 0.5, "Dropout keep probability (default: 0.5)")
tf.flags.DEFINE_float("l2_reg_lambda", 0.0, "L2 regularization lambda (default: 0.0)")

# Training parameters
tf.flags.DEFINE_integer("batch_size", 64, "Batch Size (default: 64)")
tf.flags.DEFINE_integer("num_epochs", 200, "Number of training epochs (default: 200)")
tf.flags.DEFINE_integer("evaluate_every", 100, "Evaluate model on dev set after this many steps (default: 100)")
tf.flags.DEFINE_integer("checkpoint_every", 100, "Save model after this many steps (default: 100)")
tf.flags.DEFINE_integer("num_checkpoints", 5, "Number of checkpoints to store (default: 5)")

FLAGS = tf.flags.FLAGS
FLAGS._parse_flags()
print("\nParameters:")
for attr, value in sorted(FLAGS.__flags.items()):
    print("{}={}".format(attr.upper(), value))
print("")


# Data Preparation
# ==================================================

# load data
print("Loading data...")
x_text, y = data_helpers.load_data_and_labels(positive_data_file=FLAGS.positive_data_file,
                                              negative_data_file=FLAGS.negative_data_file)

# build vocabulary
max_document_length = max([len(x.split(" ")) for x in x_text])
vocab_processor = learn.preprocessing.VocabularyProcessor(max_document_length=max_document_length)
x = np.array(list(vocab_processor.fit_transform(raw_documents=x_text)))

# randomly shuffle data
np.random.seed(10)
shuffle_indices = np.random.permutation(np.arange(len(y)))
x_shuffled = x[shuffle_indices]
y_shuffle = y[shuffle_indices]

# split train/test set
dev_sample_index = -1 * int(FLAGS.dev_sample_index*float(len(y)))
x_train, x_dev = x_shuffled[:dev_sample_index], x_shuffled[dev_sample_index:]
y_train, y_dev = y_shuffled[:dev_sample_index], y_shuffled[dev_sample_index:]
print("Vocabulary Size: {:d}".format(len(vocab_processor.vocabulary_)))
print("Train/Dev split: {:d}/{:d}".format(len(y_train), len(y_dev)))


# Training
# ==================================================

with tf.Graph().as_default():
    sess = tf.Session()
    with sess.as_default():
        # initialize graph
        cnn = TextCNN(sequence_length=x_train.shape[1],
                      num_classes=2,
                      vocab_size=len(vocabulary),
                      embedding_size=FLAGS.embedding_dim,
                      filter_sizes=map(int, FLAGS.filter_sizes.split(",")),
                      num_filters=FLAGS.num_filters,
                      l2_reg_lambda=FLAGS.l2_reg_lambda)

        # minimize loss
        global_step = tf.Variable(0, name='global_step', trainable=False)
        optimizer = tf.train.AdamOptimize(1e-4)
        grads_and_vars = optimizer.compute_gradients(cnn.loss)
        # train_op here is a newly created operation that we can run to perform
        # a gradient update on our parameters
        train_op = optimizer.apply_gradients(grads_and_vars, global_step=global_step)

        # # Summaries
        # TensorFlow has a concept of a summaries, which allow you to keep track
        # of and visualize various quantities during training and evaluation.
        # Summaries are serialized objects, and they are written to disk using a
        # SummaryWriter.
        # output directory for models and summaries
        timestamp = str(int(time.time()))
        out_dir = os.path.abspath(os.path.join(os.path.curdir, "runs", timestamp))
        print("Writing to {}\n".format(out_dir))

        # summaries for loss and accuracy
        loss_summary = tf.scalar_summary("loss", cnn.loss)
        acc_summary = tf.scalar_summary("accuracy", cnn.accuracy)

        # train summaries
        train_summary_op = tf.merge_summary([loss_summary, acc_summary])
        train_summary_dir = os.path.join(out_dir, "summaries", "train")
        train_summary_writer = tf.train.SummaryWriter(train_summary_dir, sess.graph_def)

        # dev summaries
        dev_summary_op = tf.merge_summary([loss_summary, acc_summary])
        dev_summary_dir = os.path.join(out_dir, "summaries", "dev")
        dev_summary_writer = tf.train.SummaryWriter(dev_summary_dir, sess.graph_def)

        # # Checkpointing
        # Another TensorFlow feature you typically want to use is checkpointing –
        # saving the parameters of your model to restore them later on. Checkpointscan
        # be used to continue training at a later point, or to pick the best parameters
        # setting using early stopping. Checkpoints are created using a Saver object
        checkpoint_dir = os.path.abspath(os.path.join(out_dir, "checkpoints"))
        checkpoint_prefix = os.path.join(checkpoint_dir, "model")
        # TensorFlow assumes this directory already exists so we need to create it
        if not(os.path.lexists(checkpoint_dir)):
            os.makedirs(checkpoint_dir)
        saver = tf.train.Saver(tf.all_variables(), max_to_keep=FLAGS.num_checkpoints)


        # # Initialize all variables
        sess.run(tf.initialize_all_tables())

        # # Define each training step
        def train_step(x_batch, y_batch):
            """A single training step"""
            feed_dict = {cnn.input_x: x_batch,
                         cnn.input_y: y_batch,
                         cnn.dropout_keep_prob: FLAGS.dropout_keep_prob}
            _, step, summaries, loss, accuracy = sess.rum([train_op,
                                                           global_step,
                                                           train_summary_op,
                                                           cnn.loss,
                                                           cnn.accuracy],
                                                          feed_dict)
            time_str = datetime.datetime.now().isoformat()
            print("{}: step {}, loss {:g}, acc {:g}".format(time_str,
                                                            step,
                                                            loss,
                                                            accuracy))
            train_summary_writer(summaries, step)

        def dev_step(x_batch, y_batch, writer=None):
            """Evaluates model on a dev set"""
            feed_dict = {cnn.input_x: x_batch,
                         cnn.input_y: y_batch,
                         cnn.dropout_keep_prob: 1.0}
            step, summaries, loss, accuracy = sess.run([global_step,
                                                        dev_summary_op,
                                                        cnn.loss,
                                                        cnn.accuracy],
                                                       feed_dict)
            time_str = datetime.datetime.now().isoformat()
            print("{}: step {}, loss {:g}, acc {:g}".format(time_str,
                                                            step,
                                                            loss,
                                                            accuracy))
            if writer:
                writer.add_summary(summaries, step)

        # generate batches
        batches = data_helpers.batch_iter(data=list(zip(x_train, y_train)),
                                          batch_size=FLAGS.batch_size,
                                          num_epochs=FLAGS.num_epochs)
        # train loop (for each batch...)
        for batch in batches:
            x_batch, y_batch = zip(*batch)
            train_step(x_batch=x_batch,
                       y_batch=y_batch)
            current_step = tf.train.global_step(sess, global_step)
            if current_step % FLAGS.evaluate_every == 0:
                print('\nEvaluation:')
                dev_step(x_dev, y_dev, writer=dev_summary_writer)
                print("")
            if current_step %  FLAGS.checkpoint_every == 0:
                path = saver.save(sess, checkpoint_prefix, global_step=current_step)
                print("Saved model checkpoint to {}\n".format(path))
