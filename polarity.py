from textblob import TextBlob
from textblob import Word
from alchemyapi_python.alchemyapi import AlchemyAPI
import json

alchemyapi = AlchemyAPI()

def main(review_phrase_dict_list, feature_set):

    feature_phrase_polarity={}
    phrase_polarity={}
    phrase_feature = {}

    for feature in feature_set:
        feature_phrase_polarity[feature] = []

    for row in review_phrase_dict_list:
        for phrase in row['phrases']:
            for feature in feature_set:
                if feature in phrase:

                    score = 0.0
                    response = alchemyapi.keywords('text', phrase, {'sentiment': 1})
                    count = 0
                    print "phrase ============= ", phrase
                    # print response
                    if "keywords" in response:
                        print "response keywords: ============ " , response["keywords"]
                        if len(response['keywords']) > 0:
                            for keyword in response['keywords']:
                                if "sentiment" in keyword and "score" in keyword['sentiment']:
                                    print "float(keyword['sentiment']['score']): ", float(keyword['sentiment']['score']) 
                                    if float(keyword['sentiment']['score']) == 0:
                                        score += zero_score(phrase)
                                        print "Alchemy: " , phrase
                                        print zero_score(phrase)
                                    else:
                                        print "1st elseeeeee: " , phrase
                                        print float(keyword['sentiment']['score'])
                                        score += float(keyword['sentiment']['score'])
                                else:
                                    print "2nd elseeeeee: " , phrase
                                    print zero_score(phrase)
                                    score += zero_score(phrase)
                        else:
                            score += zero_score(phrase)
                    else:
                        print "3rd elseeeeee: " , phrase
                        print zero_score(phrase)
                        score += zero_score(phrase)
                    count +=1
                    
                    # blob = TextBlob(phrase)
                    # polarity = blob.sentiment.polarity
                    feature_phrase_polarity[feature].append({"opinion" : phrase , "polarity" : score / count})
                    phrase_polarity[phrase] = score / count
                    phrase_feature[phrase] = feature
                    break
    return feature_phrase_polarity, phrase_polarity, phrase_feature

def final_polarity(feature_phrase_polarity):
    final_polarity = {}
    for feature in feature_phrase_polarity.iteritems():
        polarity = 0
        difference = 100
        display_phrase  = feature[0]
        if len(feature[1]) >= 1:
            for row in feature[1]:
                polarity += row['polarity']
            polarity = polarity / len(feature[1])
            for row in feature[1]:
                # print row
                current_diff = abs(polarity - row['polarity'])
                if current_diff <= difference:
                    difference = current_diff
                    display_phrase = row['opinion']

            final_polarity[display_phrase] = polarity 
    return final_polarity

def zero_score(phrase):
    blob = TextBlob(phrase)
    return float(blob.sentiment.polarity)
