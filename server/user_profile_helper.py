from PIL import Image
import requests


def helper_check_validdimensions(file_name, x_start, y_start, x_end, y_end):
    # check the length and the width of the image are valid
    image = Image.open(file_name)
    width, height = image.size
    if x_end <= x_start or y_end <= y_start:
        return False
    if x_start < 0 or y_start < 0:
        return False
    if x_end > width or y_end > height:
        return False

    return True


def helper_check_HTTPstatus(img_url):
    response = requests.get(img_url)
    if response.status_code != 200:
        return False
    return True
