import base64
import requests
import server.app
import warnings

from PIL import Image
from io import BytesIO


DEPTH_TIMEOUT = 10.0
DEPTHMAP_SIZE = (640, 480)


def depthmap_query(image_data=None, image_data_b64=None, image_type=None, preresize=True):
    if (image_data is None) == (image_data_b64 is None):
        raise ValueError("Only one of arguments `image_data` and `image_data_b64` should be specified")

    if preresize:
        if image_data is None:
            image_data = base64.b64decode(image_data_b64)
        image = Image.open(BytesIO(image_data)).resize((640, 480), Image.BICUBIC)
        img_stream = BytesIO()
        image.save(img_stream, format="png")
        image_data = img_stream.getvalue()
        image_data_b64 = None

    if image_data_b64 is None:
        image_data_b64 = base64.b64encode(image_data).decode("utf-8").replace("\n", "")

    payload = {}
    payload["data"] = image_data_b64
    if image_type is not None:
        payload["image_type"] = image_type

    # Throws requests.exceptions.Timeout 
    request = requests.post(server.app.config.depthmap_addr, json=payload, timeout=DEPTH_TIMEOUT)
    
    if request.status_code != 200:
        raise RuntimeError("Error: received {} status code with response:\n`{}`".format(request.status_code, request.text))

    return request.json()
