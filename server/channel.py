from server.data_structure import getdata
from server.Helper_functions import get_channel_from_cid
from server.Helper_functions import get_user_from_token
from server.Helper_functions import get_user_from_uid
from server.Helper_functions import helper_check_user_admin
from server.check_error import check_validchannel
from server.check_error import check_validuid
from server.check_error import check_auser_in_channel
from server.check_error import check_auser_not_in_channel
from server.check_error import check_auser_permission_of_channel
from server.check_error import check_uid_not_in_channel
from server.check_error import check_only_owner
from server.check_error import check_tokenlogin
from server.error import AccessError
from server.error import ValueError

###################### helper function for channel ###############################
def get_members_details(members):
    members_dic = []

    for uid in members:
        uid_dic = get_user_from_uid(uid)
        members_dic.append({
            'u_id' : uid,
            'name_first' : uid_dic['name_first'],
            'name_last' : uid_dic['name_last'],
            'profile_img_url' : uid_dic['profile_img_url']
        })

    return members_dic

######################### channel functions ########################################

def channel_invite(token, channel_id, u_id):
    check_tokenlogin(token)

    channel_dic = get_channel_from_cid(channel_id)
    auser_dic = get_user_from_token(token)

    check_validchannel(channel_dic)

    members = channel_dic['all_members']
    check_auser_not_in_channel(auser_dic['u_id'], members)


    uid_dic = get_user_from_uid(u_id)
    # add this user in the channel if this user is not a member of the channel
    check_validuid(uid_dic)
    if u_id in members:
        raise ValueError("the invited user already in channel")
    members.append(u_id)
    return {}


def channel_details(token, channel_id):
    check_tokenlogin(token)

    channel_dic = get_channel_from_cid(channel_id)

    check_validchannel(channel_dic)
    # check_auser_not_in_channel (auser_dic['u_id'], channel_dic['all_members'])

    name = channel_dic['name']
    owner_members = get_members_details(channel_dic['owner_members'])
    all_members = get_members_details(channel_dic['all_members'])

    return {'name' : name, 'owner_members' : owner_members, 'all_members' : all_members}


def channel_messages(token, channel_id, start):
    check_tokenlogin(token)

    #set up the initial value
    max = 50
    returned_least_recent = -1

    channel_dic = get_channel_from_cid(channel_id)
    auser_dic = get_user_from_token(token)

    check_validchannel(channel_dic)
    check_auser_not_in_channel(auser_dic['u_id'], channel_dic['all_members'])

    # check if the start is valid
    total_messages = len(channel_dic['messages'])
    return_messages = []

    if total_messages == 0:
        return {'messages': return_messages, 'start': start, 'end': -1}

    if start > total_messages:
        raise ValueError('Start is greater than the total number of messages in the channel')


    counter = start
    end = start + max

    # get the messages between start and end
    # if end > total, just get the messages between start and last message
    while counter < end and counter < total_messages:
        return_messages.append(channel_dic['messages'][counter])
        counter = counter + 1

    # if this function has returned the least recent messages in the channel
    # returns -1 in "end" to indicate there are no more messages to load after this return.
    if start == total_messages:
        end = returned_least_recent

    # else return the counter of last message in the list of returned messages
    else:
        end = counter

    return {'messages': return_messages, 'start': start, 'end': end}



def channel_leave(token, channel_id):
    check_tokenlogin(token)

    channel_dic = get_channel_from_cid(channel_id)
    auser_dic = get_user_from_token(token)

    # check error
    check_validchannel(channel_dic)

    auser_uid = auser_dic['u_id']
    channel_all_members = channel_dic['all_members']
    check_auser_not_in_channel(auser_uid, channel_all_members)

    # the auser leave the channel
    channel_all_members.remove(auser_uid)
    owners = channel_dic['owner_members']
    # if auser is a owner of channel, remove auser from owner list of this channel
    if auser_uid in owners:
        check_only_owner(channel_dic)
        owners.remove(auser_uid)

    return {}


def channel_join(token, channel_id):
    check_tokenlogin(token)

    channel_dic = get_channel_from_cid(channel_id)
    auser_dic = get_user_from_token(token)

    # check error
    check_validchannel(channel_dic)

    auid = auser_dic['u_id']
    check_auser_in_channel(auid, channel_dic['all_members'])


    # when channel_id refers to a channel that is private
    # when the authorised user is not an admin
    if not channel_dic['is_public'] and not helper_check_user_admin(auser_dic):
        raise AccessError("channel is private")

    # add the auser to channel
    channel_dic['all_members'].append(auid)

    return {}


def channel_addowner(token, channel_id, u_id):
    check_tokenlogin(token)

    channel_dic = get_channel_from_cid(channel_id)
    auser_dic = get_user_from_token(token)

    check_validchannel(channel_dic)

    check_auser_permission_of_channel(auser_dic, channel_dic)

    check_uid_not_in_channel(u_id, channel_dic)

    if u_id in channel_dic['owner_members']:
        raise ValueError("The user with uid is already a owner of this channel")

    # add uid to the owner of the channel
    channel_dic['owner_members'].append(u_id)
    return {}


def channel_removeowner(token, channel_id, u_id):
    check_tokenlogin(token)

    channel_dic = get_channel_from_cid(channel_id)
    auser_dic = get_user_from_token(token)

    check_validchannel(channel_dic)

    check_auser_permission_of_channel(auser_dic, channel_dic)
    # only the owner can remove an owner, remove oneself is okay
    if u_id not in channel_dic['owner_members']:
        raise ValueError("The user with uid is not a owner of this channel")

    check_only_owner(channel_dic)


    # add uid to the owner of the channel
    channel_dic['owner_members'].remove(u_id)
    return {}


def channels_list(token):
    check_tokenlogin(token)

    data = getdata()
    auser_dic = get_user_from_token(token)
    auid = auser_dic['u_id']

    channels = []
    # get the list of channels, which the token user in
    for channel in data['channels']:
        if auid in channel['all_members']:
            channels.append({
                'channel_id' : channel['channel_id'],
                'name' : channel['name']
            })


    return {'channels' : channels}

def channels_listall(token):
    check_tokenlogin(token)

    data = getdata()
    channels = []

    # get list of all channels
    # do not include the first channel in channel list
    # because in data structure, the first on is just a model
    first = True
    for channel in data['channels']:
        if not first:
            channels.append({
                'channel_id': channel['channel_id'],
                'name' : channel['name']
            })
        first = False

    return {'channels' : channels}


def channels_create(token, name, is_public):
    check_tokenlogin(token)

    data = getdata()
    auser_dic = get_user_from_token(token)
    auid = auser_dic['u_id']

    # check if the channel name valid
    if len(name) > 20:
        raise ValueError('channel name not valid')

    channel_id = -1
    for channel in data['channels']:
        channel_id = channel['channel_id']

    # channel id will be automaticlly updated with every creation
    channel_id = channel_id + 1

    channel_dic = {
        'channel_id': channel_id,
        'name' : name,
        'is_public' : is_public,
        'standup_messages': '',
        'standup_is_active': False,
        'standup_time_finish':None,
        'owner_members':[auid],
        'all_members':[auid],
        # the one who created this channel will be the owner of the channel
        'messages' : []
    }

    # channel will be added into the channels list after creation
    data['channels'].append(channel_dic)


    return {'channel_id' : channel_id}
