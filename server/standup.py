import datetime
from server.error import ValueError
from server.Helper_functions import get_user_from_token
from server.Helper_functions import get_channel_from_cid
from server.message_helper import helper_standup
from server.message_helper import CustomTimer
from server.check_error import check_validchannel
from server.check_error import check_auser_not_in_channel
from server.check_error import check_message_length


def standup_start(token, channel_id, length):
    # 1. the authorised user should be in this channel
    # 2. the channel should be valid
    # 3. there can be only one standup at the same time in one channel
    auser_dic = get_user_from_token(token)
    auid = auser_dic['u_id']
    channel_dic = get_channel_from_cid(channel_id)

    check_validchannel(channel_dic)
    check_auser_not_in_channel(auid, channel_dic['all_members'])

    if channel_dic['standup_is_active']:
        raise ValueError("An active standup is currently running in this channel")

    channel_dic['standup_is_active'] = True

    finish_time = int(datetime.datetime.now().strftime("%s")) + length
    channel_dic['standup_time_finish'] = finish_time
    timer = CustomTimer(length, helper_standup, (channel_dic, auid))
    timer.start()

    return {'time_finish' : finish_time}

def standup_active(token, channel_id):
    # 1. the channel should be valid
    # 2. authorised user should be in the channel
    auser_dic = get_user_from_token(token)
    auid = auser_dic['u_id']
    channel_dic = get_channel_from_cid(channel_id)

    check_validchannel(channel_dic)
    check_auser_not_in_channel(auid, channel_dic['all_members'])

    if not channel_dic['standup_is_active']:
        return {'is_active' : False, 'time_finish' : None}

    return {'is_active' : True, 'time_finish' : channel_dic['standup_time_finish']}



def standup_send(token, channel_id, message):
    # 1. the channel should be valid
    # 2. authorised user should be in the channel
    # 3. the message should be valid
    auser_dic = get_user_from_token(token)
    auid = auser_dic['u_id']
    auser_firstname = auser_dic['name_first']

    channel_dic = get_channel_from_cid(channel_id)

    check_message_length(message)
    check_validchannel(channel_dic)
    check_auser_not_in_channel(auid, channel_dic['all_members'])

    if not channel_dic['standup_is_active']:
        raise ValueError("An active standup is not currently running in this channel")

    channel_dic['standup_messages'] = str(channel_dic['standup_messages']) + str(auser_firstname) + " : " + str(message) + "\n"

    return {}
