#
# Team 13, Melbourne
# Abhinav Sharma, 1009225
# Benjamin Frengley, 1050642
# Kabir Manandhar Shrestha, 1059431
# Rohit Kumar Gupta, 1023418
# Jan Knížek, 1052305
#
from core.analysis.Aurin.Place import Place

def formListPlaceObjects(health_dict, coordinates_dict):
    """
    extracting objects of Place from the aurin data
    :param aurin_data_dict: aurin data on people safety at night
    :return: List[Place(code, name, estimate, coordinates)]
    """
    list_place_objects=[]
    health_features=health_dict["features"]
    coordinates_features=coordinates_dict["features"]
    for health_feature in health_features:
        health_properties=health_feature["properties"]
        code=health_properties["lga_code"]
        name=health_properties["lga_name"]
        heart_diseases_count=health_properties["ppl_reporting_heart_disease_rank"]
        diabetes_count=health_properties["ppl_reporting_type_2_diabetes_rank"]
        obesity_count=health_properties["ppl_reporting_being_obese_rank"]
        HBP_count=health_properties["ppl_reporting_high_blood_pressure_rank"]
        for coordinates_feature in coordinates_features:
            coordinate_properties=coordinates_feature["properties"]
            if coordinate_properties["lga_code06"] == code:
                coordinates=coordinate_properties["boundedBy"]
        list_place_objects.append(Place(code,name,heart_diseases_count,diabetes_count,obesity_count,HBP_count,coordinates))
    return list_place_objects

