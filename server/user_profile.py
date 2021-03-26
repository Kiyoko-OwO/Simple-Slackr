import os
import urllib.request
from PIL import Image
from server.data_structure import getdata
from server.Helper_functions import get_user_from_token
from server.Helper_functions import get_user_from_uid
from server.auth_helper import handle_is_unique
from server.check_error import check_validuid
from server.check_error import check_validhandle
from server.check_error import check_validname
from server.check_error import check_validemail
from server.check_error import check_tokenlogin
from server.user_profile_helper import helper_check_HTTPstatus
from server.user_profile_helper import helper_check_validdimensions
from server.error import ValueError


################################## user profile functions ##################################

def user_profile(token, u_id):
    check_tokenlogin(token)

    user_dic = get_user_from_uid(u_id)

    check_validuid(user_dic)

    #initialize the user dic
    profile_dic = {
        'u_id' : user_dic['u_id'],
        'email' : user_dic['email'],
        'name_first' : user_dic['name_first'],
        'name_last' : user_dic['name_last'],
        'handle_str' : user_dic['handle'],
        'profile_img_url' : user_dic['profile_img_url']
    }

    return profile_dic


def user_profile_setname(token, name_first, name_last):
    check_tokenlogin(token)
    # check the validation of the token

    auser_dic = get_user_from_token(token)

    # check if the name is valid
    check_validname(name_first, name_last)

    auser_dic['name_first'] = name_first
    auser_dic['name_last'] = name_last

    return {}


def user_profile_setemail(token, email):
    check_tokenlogin(token)

    users = getdata()['users']

    auser_dic = get_user_from_token(token)

    check_validemail(email)
    # check if the email is valid

    for user in users:
        if user['email'] == email:
            raise ValueError("email has been used.")

    if auser_dic['email'] == email:
        raise ValueError('No new email entered')

    auser_dic['email'] = email

    return {}


def user_profile_sethandle(token, handle_str):
    check_tokenlogin(token)

    auser_dic = get_user_from_token(token)
    check_validhandle(handle_str)
    # the handle should be valid

    if not handle_is_unique(handle_str):
    # this handle has been used
        raise ValueError('handle is already used by another user')

    auser_dic['handle'] = handle_str
    return {}

def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end, port):
    auser_dic = get_user_from_token(token)
    if not helper_check_HTTPstatus(img_url):
        raise ValueError("img_url is returns an HTTP status other than 200.")

    # check whether exists this folder
    path = "static/images/"
    # if not exists path, then mkdir
    if not os.path.isdir(path):
        os.mkdir(path)

    filename = str(auser_dic['handle'] + ".jpg")
    urllib.request.urlretrieve(img_url, path+filename)

    if img_url.rsplit('.', 1)[1].lower() != "jpg" and img_url.rsplit('.', 1)[1].lower() != "jpeg":
    # the photo uploaded should be jpg
        raise ValueError("Image uploaded is not a JPG.")

    image = Image.open(path+filename)
    if not helper_check_validdimensions(path+filename, x_start, y_start, x_end, y_end):
        # x_start, y_start, x_end, y_end should be within the dimensions of the image
        raise ValueError("any of x_start, y_start, x_end, y_end are not within the dimensions of the image at the URL.")

    cropped = image.crop((x_start, y_start, x_end, y_end))
    cropped.save(path+filename)
    auser_dic['profile_img_url'] = "http://localhost:" + str(port) + "/static/images/" + filename
    # update the user profile
    print(path + filename)
    return {}

def users_all(token):
    check_tokenlogin(token)

    users = getdata()['users']

    users_profile = []

    for user in users:
        # do not get the uid 0 user, cause the first user with uid -1 just a sample
        if user['u_id'] == 0:
            continue

        this_profile = user_profile(token, user['u_id'])
        users_profile.append(this_profile)

    return {'users' : users_profile}
