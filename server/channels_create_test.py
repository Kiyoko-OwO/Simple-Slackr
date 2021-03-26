import pytest
from server.auth import auth_register
from server.auth import auth_login
from server.auth import auth_logout
from server.channel import channels_create
from server.data_structure import reset_data
from server.error import ValueError

'''
assume registered users stay between functions
the other data(like channels, messages) is reset
'''


def test_channels_create():
    reset_data()
    # SETUP BEGIN
    # Assume all users have registered in function: test_channel_invite()
    auth_dic1 = auth_register("valid1@gmail.com", "123456", "firstone", "lastone")
    auth_dic1 = auth_login("valid1@gmail.com", "123456")
    token1 = auth_dic1['token']

    auth_dic2 = auth_register("valid2@gmail.com", "123456", "firstone", "lastone")
    auth_dic2 = auth_login("valid2@gmail.com", "123456")
    token2 = auth_dic2['token']
    # SETUP END

    # successful test
    # assume the channelid is 1
    assert channels_create(token1, "channel 1", True) == {'channel_id': 0}

    with pytest.raises(ValueError):
        # Name is more than 20 characters long
        channels_create(token1, "qwertyuiopasdfghjklzxcvbnmqwertyuiop", True)

    # logout
    auth_logout(token1)
    auth_logout(token2)

    reset_data()
