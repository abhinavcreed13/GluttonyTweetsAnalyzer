#
# Team 13, Melbourne
# Abhinav Sharma, 1009225
# Benjamin Frengley, 1050642
# Kabir Manandhar Shrestha, 1059431
# Rohit Kumar Gupta, 1023418
# Jan Knížek, 1052305
#
from nltk.corpus import wordnet

def get_list_of_words(fileName):
    return open(fileName,'r').read().split(",")

def getSynonymsInfo(word):
    return wordnet.synsets(word)

def getLemmas(synset):
    return synset.lemmas()

def getLemmaOfWord(lemma):
    return wordnet.synsets(lemma.name())[0]

def compareSimilarity(lemma_of_word,lemma_of_root,threshold):
    similarity=lemma_of_word.wup_similarity(lemma_of_root)
    if (similarity>threshold): return True
    else: return False

def populateLexicalResource(fileName,number_of_iterations,threshold):
    for x in range(0,number_of_iterations):
        list_of_words=get_list_of_words(fileName)
        root_word_1=list_of_words[0]
        file=open(fileName,'a')
        for word in list_of_words:
            for synset in getSynonymsInfo(word):
                for l in getLemmas(synset):
                    if str(l.name()).replace('_',' ') not in list_of_words:
                        lemma=getLemmaOfWord(l)
                        root_word_1_lemma=wordnet.synsets(root_word_1)[0]
                        if compareSimilarity(lemma,root_word_1_lemma,threshold):
                            file.write(","+str(l.name()).replace('_',' '))
        file.close()



