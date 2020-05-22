import base64
import json
import warnings
import requests
import server.app

from PIL import Image
from io import BytesIO
from server.api import google_query


SEGMENTATION_TIMEOUT = 10.0


def crop_objects_query(image_data, blur_radius=2.0, border_extension=2, score_border=0.8):
    boxes = google_query.get_boxes(image_data)
    result = []
    with Image.open(BytesIO(image_data), "r") as image:
        for box in boxes: #TODO: filter known classes
            name = box["name"].lower()

            if box["score"] > score_border:
                coords = box["box"]
                coords_abs = (coords[0][0] * image.size[0], \
                        coords[0][1] * image.size[1], \
                        coords[2][0] * image.size[0], \
                        coords[2][1] * image.size[1])

                cropped_data = BytesIO()
                image.crop(coords_abs).save(cropped_data, format="png")

                payload = {}
                payload["data"] = base64.b64encode(cropped_data.getvalue()).decode("utf-8").replace("\n", "")
                payload["type"] = "png"
                payload["name"] = name
                payload["blur_radius"] = blur_radius
                payload["border_extension"] = border_extension

                try:
                    request = requests.post(server.app.config.segmentation_addr, json=payload, timeout=SEGMENTATION_TIMEOUT)
                except requests.exceptions.Timeout as e:
                    warnings.warn("Request timeout: {}".format(e))
                    continue
                
                if request.status_code != 200:
                    warnings.warn("Warning: received {} status code with response:\n`{}`".format(request.text, RuntimeWarning))
                    continue

                response = request.json()
                result.append((base64.b64decode(response["image"]), name))
    return result


def colormap_query(image_data=None, image_data_b64=None, image_type=None):
    if (image_data is None) == (image_data_b64 is None):
        raise ValueError("Only one of arguments `image_data` and `image_data_b64` should be specified")
    if image_data_b64 is None:
        image_data_b64 = base64.b64encode(image_data).decode("utf-8").replace("\n", "")

    payload = {}
    payload["data"] = image_data_b64
    if image_type is not None:
        payload["image_type"] = image_type

    # Throws requests.exceptions.Timeout
    request = requests.post(server.app.config.colormap_addr, json=payload, timeout=SEGMENTATION_TIMEOUT)
    
    if request.status_code != 200:
        raise RuntimeError("Error: received {} status code with response:\n`{}`".format(request.status_code, request.text))

    return request.json()
