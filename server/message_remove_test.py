import pytest
from server.auth import auth_register
from server.auth import auth_login
from server.auth import auth_logout
from server.channel import channels_create
from server.channel import channel_join
from server.channel import channel_addowner
from server.message import message_remove
from server.message import message_send
from server.error import AccessError
from server.error import ValueError
from server.data_structure import reset_data

def test_message_remove():
    reset_data()

    # SETUP BEGIN
    authRegisterDict1 = auth_register('hayden@gmail.com', '123456', 'hayden', 'Diego')
    auth_login('hayden@gmail.com', '123456')
    token1 = authRegisterDict1['token']
    authRegisterDict2 = auth_register('sally@gmail.com', '123456', 'sally', 'Juan')
    auth_login('sally@gmail.com', '123456')
    token2 = authRegisterDict2['token']
    uid2 = authRegisterDict2['u_id']
    authRegisterDict3 = auth_register('nena@gmail.com', '123456', 'Nena', 'Smith')
    auth_login('nena@gmail.com', '123456')
    token3 = authRegisterDict3['token']
    authRegisterDict4 = auth_register('carmen@gmail.com', '123456', 'Carmen', 'Davis')
    auth_login('carmen@gmail.com', '123456')
    token4 = authRegisterDict4['token']

    channelidDict1 = channels_create(token1, 'channel_1', True)
    channel_id1 = channelidDict1['channel_id']

    channel_join(token2, channel_id1)
    channel_addowner(token1, channel_id1, uid2)

    channel_join(token3, channel_id1)

    messages_dic1 = message_send(token1, channel_id1, "hello")
    message_id = messages_dic1['message_id']

    # SETUP END

    # The right example
    # the message_id is a valid message for user1
    assert message_remove(token1, message_id) == {}

    # send again
    messages_dic1 = message_send(token1, channel_id1, "hello")
    message_id = messages_dic1['message_id']
    # the right example
    # Message_id was not sent by the authorised user token2,
    # but the token2 is a owner of this channel
    assert message_remove(token2, message_id) == {}

    # send again
    messages_dic1 = message_send(token1, channel_id1, "hello")
    message_id = messages_dic1['message_id']
    with pytest.raises(ValueError):
        # assume Message id 2 no longer exists
        message_remove(token1, 10)

    with pytest.raises(AccessError):
        # assume token3 is not an owner of this channel that contain message_id
        message_remove(token3, message_id)

    with pytest.raises(AccessError):
        # assume token4 is not an admin or owner of the slack
        message_remove(token4, message_id)

    # logout
    auth_logout(token1)
    auth_logout(token2)
    auth_logout(token3)
    auth_logout(token4)
