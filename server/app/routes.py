import base64
import json
import flask
import re
import PIL

from flask import request
from PIL import Image
from io import BytesIO
from server.app import app
from server.api import google_query
from server.api import segmentation_queries
from server.api import depth_queries


@app.route('/')
@app.route('/index')
def index():
    return "Test"


@app.route('/detection', methods=['POST'])
def detection():
    if request.mimetype == "image/jpeg" or request.mimetype == "image/png":
        image_data = request.get_data()
    elif request.mimetype == "application/json":
        json_data = json.loads(request.get_data())
        image_data = base64.decodebytes(json_data["data"].encode())
        _extension = json_data["type"]
    else:
        return "Unsupported MIME type: `{}`".format(request.mimetype)

    return flask.jsonify(google_query.get_boxes(image_data))


@app.route('/crop-gcloud', methods=['POST'])
def crop_gcloud():
    aspect_ratio = 3/4
    if request.mimetype == "image/jpeg" or request.mimetype == "image/png":
        image_data = request.get_data()
    elif request.mimetype == "application/json":
        json_data = json.loads(request.get_data())
        image_data = base64.b64decode(json_data["data"])
        _extension = json_data["type"]
        if "aspect_ratio" in json_data:
            aspect_ratio_str = json_data["aspect_ratio"]
            try:
                match = re.match(r"(\d+)/(\d+)", aspect_ratio_str)
                if match:
                    aspect_ratio = float(match.group(1)) / float(match.group(2))
                else:
                    aspect_ratio = float(aspect_ratio_str)
            except ValueError:
                return "Cannot parse aspect_ratio value: `{}`".format(aspect_ratio_str)
    else:
        return "Unsupported MIME type: `{}`".format(request.mimetype)
        
    return flask.jsonify(google_query.get_crops(image_data, aspect_ratio))


# @app.route('/bgrm', methods=['POST'])
# def get_boxes():
#     if request.mimetype != "image/jpeg":
#         return "Error: expected image/jpeg, got `{}`".format(request.mimetype)

#     with tempfile.TemporaryDirectory("box-session") as tmpdir:
#         imgpath = os.path.join(tmpdir, "data.jpeg")
#         with open(imgpath, "wb") as imgfile:
#             imgfile.write(request.get_data())
#         return google_query.get_boxes(imgpath)

# @app.route('/test', methods=['POST'])
# def test():
#     image_data = request.get_data()
#     # json_data = json.loads(request.get_data())
#     res = segmentation_queries.crop_objects_query(base64.b64decode(image_data))
#     print(len(res))
#     return ""

# @app.route('/test', methods=['POST'])
# def test():
#     image_data = request.get_data()
#     # json_data = json.loads(request.get_data())
#     res = segmentation_queries.colormap_query(image_data_b64=image_data)
#     # print(res)
#     return res

# @app.route('/test', methods=['POST'])
# def test():
#     image_data = request.get_data()
#     # json_data = json.loads(request.get_data())
#     res = depth_queries.depthmap_query(image_data_b64=image_data.decode())
#     # print(res)
#     return res
