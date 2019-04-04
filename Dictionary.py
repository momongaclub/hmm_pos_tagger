DICT_DELIMITER = '\t'
WORD_POS_SEPARATOR = '/'


class Dictionary():

    def __init__(self):
        self.dictionary = {}


class Bigram_prob_dictionary(Dictionary):

    def load_bigram_prob_dictionary(self, fname):
        bigram_prob = {}
        with open(fname, 'r') as fp:
            for line in fp:
                line = line.rstrip()
                bigram, prob = line.split(DICT_DELIMITER)
                bigram_prob[bigram] = float(prob)
        self.dictionary = bigram_prob


class Lex_prob_dictionary(Dictionary):

    def load_lex_prob_dictionary(self, fname, sentences):
        lex_prob = {'F': {'F': 1.0}}
        with open(fname, 'r') as fp:
            for line in fp:
                line = line.rstrip()
                word_pos, prob = line.split(DICT_DELIMITER)
                word, pos = word_pos.split(WORD_POS_SEPARATOR)
                dic = lex_prob.get(word)
                if dic == None:
                    lex_prob[word] = {pos: float(prob)}
                else:
                    lex_prob[word].update({pos: float(prob)})

        for sentence in sentences:
            for word in sentence:
                if word == 'a' or word == 'an':
                    pos = 'DT'
                elif word[0].isupper() == True:
                    pos = 'N'
                else:
                    pos = 'V'
                lex_prob[word] = lex_prob.get(word, {pos:0.01})
        self.dictionary = lex_prob

