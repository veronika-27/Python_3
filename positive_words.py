punctuation_chars = ["'", '"', ",", ".", "!", ":", ";", '#', '@']

def strip_punctuation(string):
    for el in punctuation_chars:
        if el in string:
            string=string.replace(el, "")
    return string

# list of positive words to use
positive_words = []
with open("positive_words.txt") as pos_f:
    for lin in pos_f:
        if lin[0] != ';' and lin[0] != '\n':
            positive_words.append(lin.strip())

def get_pos(string):
    sent=string.split()
    count_p_w=0
    for word in sent:
        word_l=word.lower()
        word_n= strip_punctuation(word_l)
        if word_n in positive_words:
            print(word_n)
            count_p_w+=1
    return(count_p_w)

negative_words = []
with open("negative_words.txt") as pos_f:
    for lin in pos_f:
        if lin[0] != ';' and lin[0] != '\n':
            negative_words.append(lin.strip())
#fhand=open("negative_words.txt", "r")
#print(fhand.read())

def get_neg(string):
    sent=string.split()
    count_n_w=0
    for word in sent:
        word_l=word.lower()
        word_n= strip_punctuation(word_l)
        if word_n in negative_words:
            print(word_n)
            count_n_w+=1
    return(count_n_w)


fhand=open("project_twitter_data.csv", "r")
tweets_data= fhand.readlines() [1:]

outfile = open('resulting_data.csv','w')
# output the header row
outfile.write('Number of Retweets, Number of Replies, Positive Score, Negative Score, Net Score')
outfile.write('\n')

# output each of the rows:
for el in tweets_data:
    tweet=el.split(",")
    re_tw=tweet[1]
    repl_tw=tweet[2].strip("\n")
    pos_tw=get_pos(tweet[0])
    neg_tw=get_neg(tweet[0])
    net_sc= (pos_tw-neg_tw)


    row_string = '{},{},{},{},{}'.format(re_tw, repl_tw, pos_tw, neg_tw, net_sc)
    print(row_string)
    outfile.write(row_string)
    outfile.write('\n')
outfile.close()
