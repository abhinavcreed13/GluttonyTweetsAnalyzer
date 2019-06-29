#
# Team 13, Melbourne
# Abhinav Sharma, 1009225
# Benjamin Frengley, 1050642
# Kabir Manandhar Shrestha, 1059431
# Rohit Kumar Gupta, 1023418
# Jan Knížek, 1052305
#
class Tweet():
    def __init__(self,id,text,coordinates,hashtags,author,authorId,time):
        """
        :param id: Id
        :param text: tweet text
        :param coordinates: coordinates
        :param hashtags: hashtags
        """
        self.id=id
        self.text=text
        self.coordinates=coordinates
        self.hashtags=hashtags
        self.author = author
        self.authorId = authorId
        self.time = time
