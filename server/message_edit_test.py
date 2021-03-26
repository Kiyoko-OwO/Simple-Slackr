import pytest
from server.auth import auth_register
from server.auth import auth_login
from server.auth import auth_logout
from server.channel import channels_create
from server.channel import channel_join
from server.message import message_edit
from server.message import message_send
from server.error import AccessError
from server.error import ValueError
from server.data_structure import reset_data



def test_message_edit():
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
    # Assume the message id 1 is a valid id for user1
    assert message_edit(token1, message_id1, 'hello') == {}

    with pytest.raises(ValueError):
        # Assume Message id 2 does not exist
        message_edit(token1, 10, 'hello')

    with pytest.raises(ValueError):
        # Message is more than 1000 characters
        message_edit(token1, message_id1, 'a'*1001)

    with pytest.raises(AccessError):
        # message_id1 was not sent by the authorised user token2 making this request
        message_edit(token2, message_id1, 'hello')

    with pytest.raises(AccessError):
        # token3 is not an owner of this channel 
        message_edit(token3, message_id1, 'hello')

    with pytest.raises(AccessError):
        # token4 is not an admin or owner of the slack
        message_edit(token4, message_id1, 'hello')


    # logout
    auth_logout(token1)
    auth_logout(token2)
    auth_logout(token3)
    auth_logout(token4)
    reset_data()
