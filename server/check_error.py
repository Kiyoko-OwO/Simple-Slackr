# check error helper functions
# some of the errors which only user for once will be written in the corresponding file
import re
from server.error import AccessError
from server.error import ValueError
from server.Helper_functions import helper_check_user_admin
from server.Helper_functions import get_user_from_token
# function to check email
regex = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"

def check(email):
    if re.match(regex, email):
        return True
    return False

# check if the email is valid
def check_validemail(email):
    if not check(email):
        raise ValueError("Invalid email")

# check if the password is valid
def check_validpassword(password):
    password_length = 6
    if len(password) < password_length:
        raise ValueError("Invalid password")

# check if the name is valie
def check_validname(firstname, lastname):
    namelen_min = 1
    namelen_max = 50
    len_first = len(firstname)
    if  len_first < namelen_min or len_first > namelen_max:
        raise ValueError("Invalid first name length")

    len_last = len(lastname)
    if len_last < namelen_min or len_last > namelen_max:
        raise ValueError("Invalid last name length")

def check_tokenlogin(token):
    userdic = get_user_from_token(token)
    if not userdic:
        raise ValueError("token not exists")
    if not userdic['is_log_in']:
        raise AccessError("the authorised user did not login")


# check if the channel is valid
def check_validchannel(channel):
    if not channel:
        raise ValueError("channel_id not valid")

# check if the uid is valid
def check_validuid(user):
    if not user:
        raise ValueError("not a valid u_id")

# check if the auser is in channel
# if the auser not in channel, raise error
def check_auser_not_in_channel(uid, channel_member):
    if uid not in channel_member:
        raise AccessError("authorised user not a member of this channel")

# check if the auser is in channel
# if the auser in channel, raise error
def check_auser_in_channel(uid, channel_member):
    if uid in channel_member:
        raise ValueError("authorised user is already a member of this channel")

# when the authorised user is not an owner of the slackr
# or an owner of this channel, raise AccessError
def check_auser_permission_of_channel(user, channel):
    if user['u_id'] not in channel['owner_members'] and not helper_check_user_admin(user):
        raise AccessError("authorised user not a owner of this channel")

# if uid not in channel, raise valueerror
def check_uid_not_in_channel(uid, channel):
    if uid not in channel['all_members']:
        raise ValueError("The user with uid is not in channel.")

# if there is only one owner in the channel
# raise Valueerror
def check_only_owner(channel):
    if len(channel['owner_members']) == 1:
        raise ValueError("There is only one owner in channel, cannot remove.")

def check_message_length(message):
    max_length = 1000
    if len(message) > max_length:
        raise ValueError("Message is more than 1000 characters.")

def check_validmessage(message):
    if not message:
        raise ValueError("Message (based on ID) no longer exists.")

def check_permission_of_message(message_dic, channel_dic, u_id):
    if message_dic['u_id'] != u_id and u_id not in channel_dic['owner_members']:
        raise AccessError("The authorised user is not valid.")

def check_validreact(react_id):
    valid_react = 1
    if react_id != valid_react:
        raise ValueError("The react_id is not a valid React ID.")

def check_user_admin(user):
    if not helper_check_user_admin(user):
        raise ValueError("The authorised user is not an admin.")

def check_validhandle(handle_str):
    if len(handle_str) > 20:
        raise ValueError('Display name exceeds character limit')
    if len(handle_str) < 3:
        raise ValueError('Display name is too short')
