import pytest
from server.auth import auth_register
from server.auth import auth_login
from server.auth import auth_logout
from server.channel import channels_create
from server.channel import channel_join
from server.data_structure import reset_data
from server.error import AccessError
from server.error import ValueError

'''
assume registered users stay between functions
the other data(like channels, messages) is reset
'''

def test_channel_join():
    reset_data()
    # SETUP BEGIN
    # Assume all users have registered in function: test_channel_invite()
    auth_dic1 = auth_register("valid1@gmail.com", "123456", "firstone", "lastone")
    auth_dic1 = auth_login("valid1@gmail.com", "123456")
    token1 = auth_dic1['token']

    auth_dic2 = auth_register("valid2@gmail.com", "123456", "firstone", "lastone")
    auth_dic2 = auth_login("valid2@gmail.com", "123456")
    token2 = auth_dic2['token']

    channelid_dic1 = channels_create(token1, "channel 1", True)
    channel_id1 = channelid_dic1['channel_id']

    # create a private channel
    channelid_dic2 = channels_create(token1, "channel 2", False)
    channel_id2 = channelid_dic2['channel_id']

    # SETUP END

    # successful test
    assert channel_join(token2, channel_id1) == {}

    # error test
    with pytest.raises(ValueError):
        # Channel (based on ID) does not exist
        # assume channel id 3 does not exist
        channel_join(token1, 10)

    with pytest.raises(ValueError):
        # if token is already a member in this channel
        channel_join(token2, channel_id1)

    with pytest.raises(AccessError):
        # channel_id refers to a channel that is private (when the authorised user is not an admin)
        channel_join(token2, channel_id2)

    # logout
    auth_logout(token1)
    auth_logout(token2)

    reset_data()
