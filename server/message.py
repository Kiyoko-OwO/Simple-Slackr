from datetime import datetime
from server.Helper_functions import get_user_from_token
from server.Helper_functions import get_channel_from_cid
from server.Helper_functions import get_message_from_mid
from server.Helper_functions import helper_check_user_admin
from server.check_error import check_auser_not_in_channel
from server.check_error import check_validchannel
from server.check_error import check_message_length
from server.check_error import check_validmessage
from server.check_error import check_permission_of_message
from server.check_error import check_validreact
from server.check_error import check_uid_not_in_channel
from server.check_error import check_user_admin
from server.check_error import check_tokenlogin
from server.message_helper import CustomTimer
from server.message_helper import convert_date
from server.message_helper import helper_is_the_user_reacted
from server.message_helper import helper_check_react_exists
from server.message_helper import helper_send_message
from server.error import ValueError


################################## message functions ##################################
def message_send(token, channel_id, message):
# only the user who is in the channel can send message
    check_tokenlogin(token)

    channel_dic = get_channel_from_cid(channel_id)
    auser_dic = get_user_from_token(token)
    auid = auser_dic['u_id']

    check_validchannel(channel_dic)
    check_auser_not_in_channel(auid, channel_dic['all_members'])
    check_message_length(message)

    c_messages = channel_dic['messages']
    m_id = helper_send_message(c_messages, message, auid)
    # append the m_id into the message list after sending

    return{'message_id' : m_id}

def message_sendlater(token, channel_id, message, time_send):
    check_tokenlogin(token)

    channel_dic = get_channel_from_cid(channel_id)
    auser_dic = get_user_from_token(token)
    auid = auser_dic['u_id']

    check_validchannel(channel_dic)
    check_auser_not_in_channel(auid, channel_dic['all_members'])
    check_message_length(message)

    second = (convert_date(time_send) - datetime.utcnow()).total_seconds()
    if second < 0:
        raise ValueError("Time sent is a time in the past.")

    timer = CustomTimer(second, helper_send_message, (channel_dic['messages'], message, auid))
    # timer = threading.Timer(second, message_send(token, channel_id, message))
    timer.start()
    m_id = timer.join()
    print(m_id)
    return{'message_id' : m_id}

def message_remove(token, message_id):
    check_tokenlogin(token)

    auser_dic = get_user_from_token(token)

    m_c_dic = get_message_from_mid(message_id)
    check_validmessage(m_c_dic)
    message_dic = m_c_dic['message_dic']
    channel_dic = m_c_dic['channel_dic']

    if not helper_check_user_admin(auser_dic):
        check_permission_of_message(message_dic, channel_dic, auser_dic['u_id'])

    # remove the message
    channel_dic['messages'].remove(message_dic)

    return {}

def message_edit(token, message_id, message):
    check_tokenlogin(token)

    auser_dic = get_user_from_token(token)
    # only the user who sent this message can edit the message
    check_message_length(message)

    m_c_dic = get_message_from_mid(message_id)
    check_validmessage(m_c_dic)
    message_dic = m_c_dic['message_dic']
    channel_dic = m_c_dic['channel_dic']

    if not helper_check_user_admin(auser_dic):
        check_permission_of_message(message_dic, channel_dic, auser_dic['u_id'])

    # edit the message
    # if the message is empty, delete this message
    if message == '':
        channel_dic['messages'].remove(message_dic)
        return {}

    message_dic['message'] = message

    return {}


def message_react(token, message_id, react_id):
    # 1. authorise user should be in the channel
    # 2. the message should be valid
    # 3. the message should be unreacted
    check_tokenlogin(token)

    #get the information of the user
    auser_dic = get_user_from_token(token)
    auid = auser_dic['u_id']

    m_c_dic = get_message_from_mid(message_id)
    check_validmessage(m_c_dic)
    # check if the message is valid then get the message
    message_dic = m_c_dic['message_dic']
    channel_dic = m_c_dic['channel_dic']

    check_uid_not_in_channel(auid, channel_dic)
    check_validreact(react_id)

    m_reacts = message_dic['reacts']

    this_react = helper_check_react_exists(m_reacts, react_id)
    user_reacted = helper_is_the_user_reacted(message_dic, auid)
    # if there is no this react in the message
    # add a react
    if not this_react:
        m_reacts.append({
            'react_id' : react_id,
            'u_ids' : [auid],
            'is_this_user_reacted' : user_reacted
        })
        return {}

    # if there is this react in the message
    if auid in this_react['u_ids']:
        raise ValueError("Message already contains an active React with react_id from user.")

    this_react['u_ids'].append(auid)
    if not user_reacted:
        this_react['is_this_user_reacted'] = True

    return {}

def message_unreact(token, message_id, react_id):
    # 1. authorise user should be in the channel
    # 2. the message should be valid
    # 3. the message should be reacted
    check_tokenlogin(token)

    auser_dic = get_user_from_token(token)
    auid = auser_dic['u_id']

    m_c_dic = get_message_from_mid(message_id)
    check_validmessage(m_c_dic)

    message_dic = m_c_dic['message_dic']
    channel_dic = m_c_dic['channel_dic']

    # when the user not in this channel
    check_uid_not_in_channel(auid, channel_dic)
    check_validreact(react_id)

    m_reacts = message_dic['reacts']

    this_react = helper_check_react_exists(m_reacts, react_id)

    # when the user didn't react to this message
    if not this_react or auid not in this_react['u_ids']:
        raise ValueError("Message with message_id does not contain an active React with react_id from user.")

    user_reacted = helper_is_the_user_reacted(message_dic, auid)

    this_react['u_ids'].remove(auid)
    if not user_reacted:
        this_react['is_this_user_reacted'] = False

    return {}

def message_pin(token, message_id):
    # 1. authorise user should be in the channel
    # 2. the message should be valid
    # 3. the message should be unpinned
    check_tokenlogin(token)

    auser_dic = get_user_from_token(token)
    auid = auser_dic['u_id']

    m_c_dic = get_message_from_mid(message_id)
    check_validmessage(m_c_dic)
    message_dic = m_c_dic['message_dic']
    channel_dic = m_c_dic['channel_dic']

    #check if the authorise user is in the channel
    check_auser_not_in_channel(auid, channel_dic['all_members'])
    check_user_admin(auser_dic)

    # cannot pin the message which is pinned
    if message_dic['is_pinned']:
        raise ValueError("Message with ID message_id is already pinned.")

    message_dic['is_pinned'] = True

    return {}

def message_unpin(token, message_id):
    # 1. authorise user should be in the channel
    # 2. the message should be valid
    # 3. the message should be pinned
    check_tokenlogin(token)

    auser_dic = get_user_from_token(token)
    auid = auser_dic['u_id']

    m_c_dic = get_message_from_mid(message_id)
    check_validmessage(m_c_dic)
    message_dic = m_c_dic['message_dic']
    channel_dic = m_c_dic['channel_dic']

    check_auser_not_in_channel(auid, channel_dic['all_members'])
    check_user_admin(auser_dic)

    # cannot pin the message that is unpinned
    if not message_dic['is_pinned']:
        raise ValueError("Message with ID message_id is already unpinned.")

    message_dic['is_pinned'] = False

    return {}
