import pytest
from server.auth import auth_register
from server.auth import auth_login
from server.auth import auth_logout
from server.channel import channels_create
from server.message import message_send
from server.error import AccessError
from server.error import ValueError
from server.data_structure import reset_data



def test_message_send():
    reset_data()
    # SETUP BEGIN
    authRegisterDict1 = auth_register('hayden@gmail.com', '123456', 'hayden', 'Diego')
    auth_login('hayden@gmail.com', '123456')
    token1 = authRegisterDict1['token']
    authRegisterDict2 = auth_register('sally@gmail.com', '123456', 'sally', 'Juan')
    auth_login('sally@gmail.com', '123456')
    token2 = authRegisterDict2['token']

    channelidDict1 = channels_create(token1, 'channel_1', True)
    channel_id1 = channelidDict1['channel_id']
    channelidDict2 = channels_create(token2, 'channel_8', True)
    channel_id2 = channelidDict2['channel_id']
    # SETUP END

    # The right example
    message_send(token1, channel_id1, 'hello')

    # error test
    with pytest.raises(ValueError):
        # Message is more than 1000 characters
        message_send(token1, channel_id1, 'a'*1001)

    with pytest.raises(AccessError):
        # token1 has not joined Channel channel_id2
        message_send(token1, channel_id2, 'hello')

    # logout
    auth_logout(token1)
    auth_logout(token2)
    reset_data()
