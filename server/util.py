import base64


def save_image(image_path, data):
    with open(image_path, "wb") as image_file:
        image_file.write(data)
