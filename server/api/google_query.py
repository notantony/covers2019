import json

from google.cloud import vision
from google.cloud.vision import types


def get_boxes(image_data):
    client = vision.ImageAnnotatorClient()
    
    request = {
        'image': {
            'content': image_data,
        },
        'features': [
            {'type': vision.enums.Feature.Type.OBJECT_LOCALIZATION},
        ]
    }
    response = client.annotate_image(request)

    result = []
    for annotation in response.localized_object_annotations:
        entry = {}
        entry["name"] = annotation.name
        entry["score"] = annotation.score
        entry["box"] = [
            (vertex.x, vertex.y)
            for vertex in annotation.bounding_poly.normalized_vertices
        ]
        result.append(entry)

    return result


def get_crops(image_data, aspect_ratio, n_results=50):
    client = vision.ImageAnnotatorClient()

    response = client.crop_hints(
        image=types.Image(content=image_data),
        max_results=n_results,
        image_context=types.ImageContext(crop_hints_params={"aspect_ratios": [aspect_ratio]})
    )
    
    result = []
    for crop_hint in response.crop_hints_annotation.crop_hints:
        entry = {}
        entry["score"] = crop_hint.confidence
        entry["crop"] = [
            (vertex.x, vertex.y)
            for vertex in crop_hint.bounding_poly.vertices
        ]
        result.append(entry)

    return result
