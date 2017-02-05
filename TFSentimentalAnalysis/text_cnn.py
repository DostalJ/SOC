import tensorflow as tf
import numpy as np

class TextCNN(object):
    """
    A CNN for text classification.
    Uses an embedding layer, followed by a convolutional, max-pooling and
    softmax layer.
    """
    def __init__(self, sequence_length, num_classes, vocab_size, embedding_size,
                 filter_sizes, num_filters, l2_reg_lambda=0.0):
        """
        sequence_length: length of our sentences (we padd all sentences to have
                         the same length)
        num_classes: number of classes in the output layer (2: positive/negative)
        vocab_size: size of our vocabulary (needed to define embedding layer, that
                    have shape [vocab_size, embedding_size])
        embedding_size: the dimensionality of our embedings
        filter_sizes: the numbers of words we want our conv filters to cover,
                      for example [3,4,5]
        num_filters: number of filters per filter size
        l2_reg_lambda: regularization constant
        """
        # placeholders for input, output and dropout
        self.input_x = tf.placeholder(dtype=tf.int32,
                                      shape=[None, sequence_length], # none means it could be anything (in our case its batch size)
                                      name="input_x")
        self.input_y = tf.placeholder(dtype=tf.float32,
                                      shape=[None, num_classes],
                                      name='input_y')
        self.dropout_keep_prob = tf.placeholder(dtype=tf.float32, # we disable dropout during testing
                                                name="dropout_keep_prob")

        # Keeping track of l2 regularization loss (optional)
        l2_loss = tf.constant(0.0)

        # embedding layer
        with tf.name_scope('embeding'): # to show in TensorBoard
            W = tf.Variable(initial_value=tf.random_uniform(shape=[vocab_size, embedding_size],
                                                            minval=-1.0,
                                                            maxval=1.0),
                            name='W')
            # actual embedding operation, result has shape [None, sequence_length, embedding_size]
            self.embedded_chars = tf.nn.embedding_lookup(params=W,
                                                         ids=self.input_x)
            # manually add dimension for conv2d
            # conv2d requires [barch, width, height, channel]
            # [None, sequence_length, embedding_size, 1]
            self.embedded_chars_expanded = tf.expand_dims(input=self.embedded_chars,
                                                          dim=-1)

        # convolutional and max-pooling layers
        # Because each convolution produces tensors of different shapes we need
        # to iterate through them, create a layer for each of them, and then
        # merge the results into one big feature vector.
        pooled_outputs = []
        for i, filter_size in enumerate(filter_sizes):
            with tf.name_scope('conv-maxpool-{}'.format(filter_size)):
                # convolution layer
                filter_shape = [filter_size, embedding_size, 1, num_filters]
                W = tf.Variable(initial_value=tf.truncated_normal(shape=filter_shape,
                                                                  stddev=0.1),
                                name='W')
                b = tf.Variable(initial_value=tf.constant(value=0.1,
                                                          shape=[num_filters]),
                                name='b')
                conv = tf.nn.conv2d(input=self.embedded_chars_expanded,
                                    filter=W,
                                    strides=[1,1,1,1],
                                    padding="VALID",
                                    name='conv')
                # apply nonlinearity
                h = tf.nn.relu(tf.nn.bias_add(conv, b), name='relu')

                # max-pooling over the outputs
                # Performing max-pooling over the output of a specific filter
                # size leaves us with a tensor of shape [batch_size, 1, 1, num_filters]
                pooled = tf.nn.max_pool(value=h,
                                        ksize=[1, sequence_length - filter_size + 1, 1, 1], # Because we dont slide over the edge
                                        strides=[1,1,1,1],
                                        padding="VALID",
                                        name='pool')
                pooled_outputs.append(pooled)

        # combine all the pooled features
        num_filters_total = num_filters * len(filter_sizes)
        # Once we have all the pooled output tensors from each filter size we
        # combine them into one long feature vector of shape [batch_size, num_filters_total]
        self.h_pool = tf.concat(concat_dim=3,
                                values=pooled_outputs)
        # Using -1 in tf.reshape tells TensorFlow to flatten the dimension when possible.
        self.h_pool_flat = tf.reshape(tensor=self.h_pool,
                                      shape=[-1, num_filters_total])

        # dropout layer
        with tf.name_scope('dropout'):
            self.h_drop = tf.nn.dropout(x=self.h_pool_flat,
                                        keep_prob=self.dropout_keep_prob)

        # scores and predictions
        with tf.name_scope('output'):
            W = tf.Variable(initial_value=tf.truncated_normal(shape=[num_filters_total, num_classes],
                                                              stddev=0.1),
                            name='W')
            b = tf.Variable(initial_value=tf.constant(value=0.1,
                                                      shape=[num_classes]),
                            name='b')
            l2_loss += tf.nn.l2_loss(W)
            l2_loss += tf.nn.l2_loss(b)
            self.scores = tf.nn.xw_plus_b(x=self.h_drop,
                                          weights=W,
                                          biases=b,
                                          name='scores')
            self.predictions = tf.argmax(input=self.scores,
                                         dimension=1,
                                         name='predictions')

        # loss and accuracy
        with tf.name_scope('loss'):
            losses = tf.nn.softmax_cross_entropy_with_logits(logits=self.scores,
                                                             labels=self.input_y)
            self.loss = tf.reduce_mean(losses) + l2_reg_lambda * l2_loss

        # accuracy
        with tf.name_scope('accuracy'):
            correct_predictions = tf.equal(x=self.predictions,
                                           y = tf.argmax(input=self.input_y,
                                                         dimension=1))
            self.accuracy = tf.reduce_mean(tf.cast(x=correct_predictions,
                                                   DstT='float'),
                                           name='accuracy')
