#
# Team 13, Melbourne
# Abhinav Sharma, 1009225
# Benjamin Frengley, 1050642
# Kabir Manandhar Shrestha, 1059431
# Rohit Kumar Gupta, 1023418
# Jan Knížek, 1052305
#
from core.analysis.WrathAnalysis.Splitter import Splitter
from core.analysis.WrathAnalysis.POSTagger import POSTagger
from functools import reduce
from nltk.stem import PorterStemmer
import operator
from textblob import TextBlob
from nltk.corpus import wordnet


def convertToLemma(list_of_words):
    """
    converts each word in the input list to stem words
    :param list_of_words
    :return: list_of_stem_words
    """
    porter=PorterStemmer()
    updated_list=[porter.stem(word) for word in list_of_words]
    return updated_list

def getResources():
    """
    :return: (postive,negative,decrease,increase,inverse)
    """
    return (convertToLemma(list(dict.fromkeys(open("core/analysis/Resources/positive.txt",'r').read().split(',')))),
            convertToLemma(list(dict.fromkeys(open("core/analysis/Resources/negative.txt",'r').read().split(',')))),
            convertToLemma(list(dict.fromkeys(open("core/analysis/Resources/decrease.txt",'r').read().split(',')))),
            convertToLemma(list(dict.fromkeys(open("core/analysis/Resources/increase.txt",'r').read().split(',')))),
            convertToLemma(list(dict.fromkeys(open("core/analysis/Resources/inverse.txt",'r').read().split(',')))))

def getRootEmotions():
    return ["happy","sad","anger","fear","shock"]
#
# def getScore(flatten_word_list,emotion):
#     for word in flatten_word_list:

def getLemma(word):
    synsets=wordnet.synsets(word)[0]
    return synsets

def getSimilarity(word, emotion):
    original_word=word[0]
    lemma_of_emotion=getLemma(emotion)
    lemma_of_word=getLemma(original_word)
    if lemma_of_word and lemma_of_emotion:
        return lemma_of_word[0].wup_similarity(lemma_of_emotion[0])
    else:
        return 0

def getScore(flatten_word_list,emotion):
    emotion_score=0
    # for i in range(len(flatten_word_list)):
    #     emotion_score+=getScore(flatten_word_list[i][1],emotion)
    for word in flatten_word_list:
        if getSimilarity(word,emotion):
            emotion_score+=getSimilarity(word,emotion)
    return emotion_score

def analyzeEmotion(flatten_word_list):
    value=(0,"")
    emotions=getRootEmotions()
    for emotion in emotions:
        score=getScore(flatten_word_list,emotion)
        print(score,emotion)
        if score>value[0]:
            value=(score,emotion)
        else:
            pass
    return value

def getWrathScore(flattened_word_list, wrath_positive, wrath_negative,decrease,increase,inverse,wrath_sentiment_score=0):
    """
    giving a wrath score to a list of words in a text
    :param flattened_word_list: words in a text in the format of (word, lemma, pos)
    :param wrath_positive: list of words denoting wrath
    :param wrath_negative: list of words denoting wrath-opposite
    :param decrease: words that decrease the value of the word after it
    :param increase: words that increase the value of the word after it
    :param inverse: words that reverses the meaning of the word
    :param wrath_sentiment_score: the score given to the text
    :return:
    """
    for i in range(len(flattened_word_list)):
        if flattened_word_list[i][1] in wrath_positive:
            if i!=0 and flattened_word_list[i-1][1] in increase:
                wrath_sentiment_score+=2
            elif i!=0 and flattened_word_list[i-1][1] in decrease:
                wrath_sentiment_score+=0.5
            elif i != 0 and flattened_word_list[i - 1][1] in inverse:
                wrath_sentiment_score-=1
            else:
                wrath_sentiment_score+=1

        elif flattened_word_list[i][1] in wrath_negative:
            if i != 0 and flattened_word_list[i - 1][1] in increase:
                wrath_sentiment_score -= 2
            elif i != 0 and flattened_word_list[i - 1][1] in decrease:
                wrath_sentiment_score -= 0.5
            elif i != 0 and flattened_word_list[i - 1][1] in inverse:
                wrath_sentiment_score+=1
            else:
                wrath_sentiment_score-=1
        else:
            pass
    return wrath_sentiment_score

def classifyText(flattened_word_list):
    """
    classifying a text if it is wrath or not
    :param flattened_word_list: words in a text in the format of (word, lemma, pos)
    :return: Boolean
    """
    resoruces=getResources()
    wrath_sentiment_score=getWrathScore(flattened_word_list,resoruces[0],resoruces[1],resoruces[2],resoruces[3],resoruces[4])
    if wrath_sentiment_score>0:
        return True
    else:
        return False

# def updatedSentimentAnalyzerEngine(text):
#     if TextBlob(text).sentiment.subjectivity > 0.3:
#         list_of_word=POSTagger().pos_tag(Splitter().split(text))
#         if list_of_word:
#             text_score=analyzeTextScore(reduce(operator.concat,list_of_word))


def updatedSentimentAnalyzerEngine(text):
    """
        analysis fo text
        :param text: text
        :return: Boolean
        """
    if TextBlob(text).sentiment.subjectivity > 0.3:
        list_word_info = POSTagger().pos_tag(Splitter().split(text))
        if list_word_info:
            return analyzeEmotion(reduce(operator.concat,list_word_info))[1]
    else:
        print("objective")

def sentimentAnalyzerEngine(text):
    """
    analysis fo text
    :param text: text
    :return: Boolean
    """
    if TextBlob(text).sentiment.subjectivity > 0.3:
        list_word_info=POSTagger().pos_tag(Splitter().split(text))
        if list_word_info:
            return classifyText(reduce(operator.concat,list_word_info))
    else:
        print("objective")


