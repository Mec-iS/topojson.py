import io
from json import load, dump

from topojson.topology import topology


def convert(geojson, topojson=None, object_name=False, *args, **kwargs):
    """
    High-level interface function to convert a GeoJSON dictionary or file
    """
    if isinstance(geojson, dict): input_dict = geojson
    else: raise ValueError('Accept only dictionaries at the moment')

    if not _validate(geojson): raise ValueError('Dictionayr is not a GeoJSON')

    output_dict = topology(input_dict, *args, **kwargs)

    return output_dict


def _validate(geoj):
    """
    Check that a dictionary is a GeoJSON properly formatted.
     
    :param geoj: 
    :return: 
    """
    from geojson.codec import dumps
    from geojson.validation import is_valid

    return is_valid(dumps(geoj))