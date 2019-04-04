import argparse
import Dictionary

DICT_DELIMITER = '\t'
WORD_POS_SEPARATOR = '/'


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('bigram_prob_dict',
                        help = 'bigram Probability dictionaly')
    parser.add_argument('lex_prob_dict',
                        help = 'Lexical Generation Probability dictionary')
    parser.add_argument('input_file',
                        help = 'input_sentences')
    args = parser.parse_args()
    return args


def load_input_file(fname):
    sentences = []
    with open(fname, 'r') as fp:
        for sentence in fp:
            sentence = sentence.rstrip('\n')
            sentence = sentence.split(' ')
            sentence.insert(0, 'F')
            sentences.append(sentence)
    return sentences


class Hmm_pos_tagger():

    def __init__(self):
        self.lattice = []
        self.lex2prob = {}
        self.bigram2prob = {}
        self.sentences = []
        self.max_word = ""
        self.answer = []

    def viterbi_algo(self, sentence, lex_prob, bigram_prob):
        self.lattice = []
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
                self.lattice.append([max_prob, words[i]+'/'+word_class, words[i-1]+'/'+max_word_class])
        self.max_word = words[i]+'/'+max_now_word_class


    def search_best_path(self):
        answer = []
        for part in reversed(self.lattice):
            if part[1] == self.max_word:
                answer.append(part[1])
                self.max_word = part[2]
        self.answer = list(reversed(answer))

    def __str__(self):
        return "answer:" + str(self.answer)


def main():
    args = parse()
    sentences = load_input_file(args.input_file)
    lex_prob = Dictionary.Lex_prob_dictionary()
    lex_prob.load_lex_prob_dictionary(args.lex_prob_dict, sentences)
    bigram_prob = Dictionary.Bigram_prob_dictionary()
    bigram_prob.load_bigram_prob_dictionary(args.bigram_prob_dict)
    hmm_pos_tagger = Hmm_pos_tagger()
    
    for sentence in sentences:
        hmm_pos_tagger.viterbi_algo(sentence, lex_prob.dictionary, bigram_prob.dictionary)
        hmm_pos_tagger.search_best_path()
        print(hmm_pos_tagger)

if __name__ == '__main__':
    main()
