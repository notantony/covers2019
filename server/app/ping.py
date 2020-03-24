from app import app
# import flask

@app.route("/ping", methods=['GET'])
def ping():
    return "pong"
