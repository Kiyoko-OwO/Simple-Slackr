from server.data_structure import getdata
from server.data_structure import get_permission_ids

#some helper functions which only be used for once will be written in the corresponding files
##########################AUTH##################################################
def get_user_from_token(token):
# search the user using their token
    data = getdata()
    for user in data['users']:
        if user['token'] == token:
            return user
    return False

def get_user_from_email(email):
# search the user using their email
    data = getdata()
    for user in data['users']:
        if user['email'] == email:
            return user
    return False

def get_user_from_uid(uid):
# search the user using their u_id
    data = getdata()
    for user in data['users']:
        if user['u_id'] == uid:
            return user
    return False

################################CHANNEL#########################################
def get_channel_from_cid(channel_id):
    data = getdata()
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return channel
    return False

def helper_check_user_admin(user):
    permission_ids_dic = get_permission_ids()
    owner_id = permission_ids_dic['Owner']
    admin_id = permission_ids_dic['Admin']
    if user['permission_id'] == owner_id or user['permission_id'] == admin_id:
        return True
    return False

####################################MESSAGE#####################################
def get_message_from_mid(message_id):
    data = getdata()
    for channel in data['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                return {'message_dic' : message, "channel_dic": channel}
    return False

def helper_check_channel_standup(channel_dic):
    if channel_dic['standup_is_active']:
        return True
    return False
