#
# Team 13, Melbourne
# Abhinav Sharma, 1009225
# Benjamin Frengley, 1050642
# Kabir Manandhar Shrestha, 1059431
# Rohit Kumar Gupta, 1023418
# Jan Knížek, 1052305
#
class Place:
    def __init__(self,code,name,heart_diseases_count,diabetes_count,obesity_count,HBP_count,coordinates,tweet_counts=0):
        """
        :param code: sla_code
        :param name: sla_name
        :param estimate: sla_estimate
        :param bounding_box: sla_bounding_coordinates
        """

        self.code=code
        self.name=name
        self.heart_disease_count=heart_diseases_count
        self.diabetes_count=diabetes_count
        self.obesity_count=obesity_count
        self.HBP_count=HBP_count
        self.bounding_box=coordinates
        self.tweet_counts=tweet_counts
