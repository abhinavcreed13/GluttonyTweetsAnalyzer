#
# Team 13, Melbourne
# Abhinav Sharma, 1009225
# Benjamin Frengley, 1050642
# Kabir Manandhar Shrestha, 1059431
# Rohit Kumar Gupta, 1023418
# Jan Knížek, 1052305
#
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


class POSTagger(object):
    def __init__(self):
        pass

    def pos_tag(self,sentences):
        """
        input format: list of lists of words
            e.g.: [['this', 'is', 'a', 'sentence'], ['this', 'is', 'another', 'one']]
        output format: list of lists of tagged tokens. Each tagged tokens has a
        form, a lemma, and a list of tags
            e.g: [[('this', 'this', ['DT']), ('is', 'be', ['VB']), ('a', 'a', ['DT']), ('sentence', 'sentence', ['NN'])],
                    [('this', 'this', ['DT']), ('is', 'be', ['VB']), ('another', 'another', ['DT']), ('one', 'one', ['CARD'])]]
        """
        stop_words = set(stopwords.words('english'))-set(list(dict.fromkeys(open("core/analysis/Resources/inverse.txt", 'r').read().split(','))))
        porter=PorterStemmer()
        pos = [nltk.pos_tag(sentence) for sentence in sentences]
        pos = [[(word, porter.stem(word), [postag]) for (word, postag) in sentence if word not in stop_words] for sentence in pos]
        return pos
