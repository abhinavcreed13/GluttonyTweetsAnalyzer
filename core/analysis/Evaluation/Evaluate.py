#
# Team 13, Melbourne
# Abhinav Sharma, 1009225
# Benjamin Frengley, 1050642
# Kabir Manandhar Shrestha, 1059431
# Rohit Kumar Gupta, 1023418
# Jan Knížek, 1052305
#
def evaluate(tweets,places):
    """
    add tweets to the place objects if they are right
    :param tweets: tweet objects
    :param places: place objects
    """
    for tweet in tweets:
        for place in places:
            if tweet.coordinates[0] >= place.bounding_box[0] and tweet.coordinates[0] <= place.bounding_box[2]:
                place.tweet_counts+=1

# def getCounts(places):
#     total_tweet_counts = 0
#     total_obesity_count = 0
#     total_HBP_count = 0
#     total_diabetes_count = 0
#     total_heart_disease_count = 0
#     for place in places:
#         total_tweet_counts += place.tweet_counts
#         total_obesity_count += place.obesity_count
#         total_heart_disease_count += place.heart_disease_count
#         total_HBP_count += place.HBP_count
#         total_diabetes_count += place.diabetes_count
#     return (total_tweet_counts,total_obesity_count,total_heart_disease_count,total_HBP_count,total_diabetes_count)

def getReducedPlaces(places):
    """
    extract only those place objects which have tweets of gluttnoy present
    :param places: place objects
    :return: reduced places
    """
    reduced_places=[]
    for place in places:
        if place.tweet_counts>0:
            reduced_places.append(place)
    return reduced_places





