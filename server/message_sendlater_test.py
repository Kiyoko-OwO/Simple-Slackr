import datetime
import pytest
from server.auth import auth_register
from server.auth import auth_login
from server.auth import auth_logout
from server.channel import channels_create
from server.message import message_sendlater
from server.error import AccessError
from server.error import ValueError
from server.data_structure import reset_data


def test_message_sendlater():
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
    '''
    later_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=50)
    str_later_time = later_time.strftime("%Y-%m-%d %H:%M:%S")
    timeArray = time.strptime(str_later_time, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(timeArray)
    print(timestamp)
    '''
    timestamp = int(datetime.datetime.now().strftime("%s")) + 3
    mid = message_sendlater(token1, channel_id1, 'hello', timestamp)
    assert mid['message_id'] == 1

    # error example
    with pytest.raises(ValueError):
        # Message is more than 1000 characters
        message_sendlater(token1, channel_id1, 'a'*1001, 1603066156)

    with pytest.raises(ValueError):
        # Assume Channel channel_id 3 does not exist (not valid channel)
        message_sendlater(token1, 3, 'hello', 1603066156)

    with pytest.raises(ValueError):
        # Assume Time 2018-10-01 00:09:06 is a time in the past (1538352546 in Timestamp)
        message_sendlater(token1, channel_id1, 'hello', 1538352546)

    with pytest.raises(AccessError):
        # token1 has not joined Channel channel_id2
        message_sendlater(token1, channel_id2, 'hello', 1603066156)

    # logout
    auth_logout(token1)
    auth_logout(token2)
    reset_data()
