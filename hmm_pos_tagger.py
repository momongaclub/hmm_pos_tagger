import sys
import re
import argparse

ratis = []
DICT_DELIMITER = '\t'
WORD_POS_SEPARATOR = '/'


def parse():

    parser = argparse.ArgumentParser()
    parser.add_argument('bigram_prob_dict',
                        help = 'bigram Probability dictionaly')
    parser.add_argument('lex_prob_dict',
                        help = 'Lexical Generation Probability dictionary')
    parser.add_argument('corpus',
                        help = 'corpus')

    args = parser.parse_args()

    return args


def load_bigram2prob(fname):

    bigram2prob = {}

    with open(fname, 'r') as fp:
        for line in fp:
            line = line.rstrip()
            bigram, prob = line.split(DICT_DELIMITER)
            bigram2prob[bigram] = float(prob)

    return bigram2prob


def load_lex2prob(fname):

    lex2prob = {'F': {'F': 1.0}} # it has to insert first token before a sentence

    with open(fname, 'r') as fp:
        for line in fp:
            line = line.rstrip()
            word_pos, prob = line.split(DICT_DELIMITER)
            word, pos = word_pos.split(WORD_POS_SEPARATOR)
            dic = lex2prob.get(word)
            if dic == None:
                lex2prob[word] = {pos: float(prob)}
            else:
                lex2prob[word].update({pos: float(prob)})

    return lex2prob


def load_sentences(fname):

    sentences = []

    with open(fname, 'r') as fp:
        for sentence in fp:
            sentence = sentence.rstrip()
            words = sentence.split()
            words.insert(0, 'F') # it has to insert first token before a sentence
            sentences.append(words)

    return sentences


def update_ratis(max_prob, word, before_word):

    ratis.append([max_prob, word, before_word])

    return 0


def back(ratis, max_word_class):

    answer = []

    for ratis_element in reversed(ratis):
        if ratis_element[1] == max_word_class:
            answer.append(ratis_element[1])
            max_word_class = ratis_element[2]

    return list(reversed(answer))


def calc(sentence, lex_prob, bigram_prob):
    words = sentence
    for i in range(1, len(words)):
        for word_class in lex_prob[words[i]]:
            max_prob = -1
            max_word_class = ''
            for before_word_class in lex_prob[words[i-1]]:
                bigram_name = before_word_class+'-'+word_class
                value = 0
                tmp = lex_prob[words[i-1]]
                if bigram_prob.get(bigram_name):
                    value = bigram_prob[bigram_name] * \
                            tmp[before_word_class] * \
                            lex_prob[words[i]][word_class]
                else:
                    value = 0

                if max_prob <= value:
                    max_prob = value
                    max_word_class = before_word_class
                    max_now_word_class = word_class

            lex_prob[words[i]][word_class] = max_prob
            update_ratis(max_prob, words[i]+'/'+word_class,
                        words[i-1]+'/'+max_word_class)
    return words[i]+'/'+max_now_word_class


def main():
    args = parse()
    lex2prob = load_lex2prob(args.lex_prob_dict)
    bigram2prob = load_bigram2prob(args.bigram_prob_dict)
    sentences = load_sentences(args.corpus)
    
    for sentence in sentences:
        max_word_class = calc(sentence, lex2prob, bigram2prob)
        answer = back(ratis, max_word_class)
        print('-----answer-----')
        print(answer)
    return 0

main()
