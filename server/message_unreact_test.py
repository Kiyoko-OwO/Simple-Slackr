import pytest
from server.auth import auth_register
from server.auth import auth_login
from server.auth import auth_logout
from server.channel import channels_create
from server.channel import channel_join
from server.message import message_react
from server.message import message_unreact
from server.message import message_send
from server.error import ValueError
from server.data_structure import reset_data


def test_message_unreact():
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
    authRegisterDict4 = auth_register('carmen@gmail.com', '123456', 'Carmen', 'Davis')
    auth_login('carmen@gmail.com', '123456')
    token4 = authRegisterDict4['token']

    channelidDict1 = channels_create(token1, 'channel_1', True)
    channel_id1 = channelidDict1['channel_id']

    channel_join(token2, channel_id1)

    messages_dic1 = message_send(token1, channel_id1, "hello")
    message_id1 = messages_dic1['message_id']

    # SETUP END

    # The right example

    # Assume reactid 1 is valid
    message_react(token1, message_id1, 1)
    assert message_unreact(token1, message_id1, 1) == {}


    message_react(token1, message_id1, 1)
    with pytest.raises(ValueError):
        # assume message_id 2 is not a valid message
        message_unreact(token1, 10, 1)

    with pytest.raises(ValueError):
        # assume react_id 3 is not a valid React ID
        message_unreact(token1, message_id1, 3)

    with pytest.raises(ValueError):
        # message_id1 does not contain an active React with react_id 4
        message_unreact(token1, message_id1, 4)


    # logout
    auth_logout(token1)
    auth_logout(token2)
    auth_logout(token3)
    auth_logout(token4)
    reset_data()
