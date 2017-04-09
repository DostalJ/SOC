data = open('twitter_labeled.txt', 'r', encoding='utf8')
pos = open('positive.txt', 'w', encoding='utf8')
neg = open('negative.txt', 'w', encoding='utf8')

# 1 == positive
# 0 == negative
for line in data:
    if line[0] == '1':
        pos.write(line[2:])
    elif line[0] == '0':
        neg.write(line[2:])
