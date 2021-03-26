from flask import send_from_directory
from server.error import APP

@APP.route("/server/images/<filename>", methods=['GET'])
def send_image(path, filename):
    return send_from_directory(path, filename)
