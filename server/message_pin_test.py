import pytest
from server.auth import auth_register
from server.auth import auth_login
from server.auth import auth_logout
from server.channel import channels_create
from server.channel import channel_join
from server.message import message_pin
from server.message import message_send
from server.error import AccessError
from server.error import ValueError
from server.data_structure import reset_data

def test_message_pin():
    reset_data()
    # SETUP BEGIN
    authRegisterDict1 = auth_register('hayden@gmail.com', '123456', 'hayden', 'Diego')
    auth_login('hayden@gmail.com', '123456')
    token1 = authRegisterDict1['token']
    authRegisterDict2 = auth_register('sally@gmail.com', '123456', 'sally', 'Juan')
    auth_login('sally@gmail.com', '123456')
    token2 = authRegisterDict2['token']
    authRegisterDict3 = auth_register('nena@gmail.com', '123456', 'Nena', 'Smith')
    auth_login('nena@gmail.com', '123456')
    token3 = authRegisterDict3['token']


    channelidDict1 = channels_create(token1, 'channel_1', True)
    channel_id1 = channelidDict1['channel_id']


    channel_join(token2, channel_id1)

    messages_dic1 = message_send(token1, channel_id1, "hello")
    message_id1 = messages_dic1['message_id']

    messagedic2 = message_send(token1, channel_id1, "helloooo")
    message_id2 = messagedic2['message_id']
    # SETUP END

    # The right example
    # assume message id 1 is a valid message
    assert message_pin(token1, message_id1) == {}

    with pytest.raises(ValueError):
        # assume message_id 8 is not a valid message
        message_pin(token1, 8)

    with pytest.raises(ValueError):
        # The authorised user token2 is not an admin
        message_pin(token2, message_id2)

    with pytest.raises(ValueError):
        # Assume message_id 1 is already pinned
        message_pin(token1, message_id1)

    with pytest.raises(AccessError):
        # The authorised user is not a member of the channel that the message is within
        # assume user1 is not a member of the channel that the message id 3 is within
        message_pin(token3, message_id2)

    # logout
    auth_logout(token1)
    auth_logout(token2)
    auth_logout(token3)
    reset_data
