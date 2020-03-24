import tempfile
import base64
import os

from app import app
from flask import request
from api import google_query


@app.route('/')
@app.route('/index')
def index():
    return "Test"


@app.route('/box', methods=['POST'])
def get_boxes():
    if request.mimetype != "image/jpeg":
        return "Unexprected MIME type: expected `image/jpeg`, got `{}`".format(request.mimetype)

    with tempfile.TemporaryDirectory("box-session") as tmpdir:
        imgpath = os.path.join(tmpdir, "data.jpeg")
        with open(imgpath, "wb") as imgfile:
            imgfile.write(request.get_data())
        return google_query.get_boxes(imgpath)


@app.route('/crop', methods=['POST'])
def get_crops():
    if request.mimetype != "image/jpeg":
        return "Unexprected MIME type: expected `image/jpeg`, got `{}`".format(request.mimetype)

    with tempfile.TemporaryDirectory("crop-session") as tmpdir:
        imgpath = os.path.join(tmpdir, "data.jpeg")
        with open(imgpath, "wb") as imgfile:
            imgfile.write(request.get_data())
        return google_query.get_crops(imgpath)


# @app.route('/bgrm', methods=['POST'])
# def get_boxes():
#     if request.mimetype != "image/jpeg":
#         return "Error: expected image/jpeg, got `{}`".format(request.mimetype)

#     with tempfile.TemporaryDirectory("box-session") as tmpdir:
#         imgpath = os.path.join(tmpdir, "data.jpeg")
#         with open(imgpath, "wb") as imgfile:
#             imgfile.write(request.get_data())
#         return google_query.get_boxes(imgpath)
