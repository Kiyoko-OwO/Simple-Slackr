import pytest
from server.auth import auth_register
from server.auth import auth_login
from server.auth import auth_logout
from server.channel import channels_create
from server.channel import channel_invite
from server.data_structure import reset_data
from server.error import ValueError
from server.error import AccessError

'''
assume registered users stay between functions
the other data(like channels, messages) is reset
'''

def test_channel_invite():
    reset_data()
    # SETUP BEGIN
    auth_dic1 = auth_register("valid1@gmail.com", "123456", "firstone", "lastone")
    auth_dic1 = auth_login("valid1@gmail.com", "123456")
    token1 = auth_dic1['token']
    uid1 = auth_dic1['u_id']

    auth_dic2 = auth_register("valid2@gmail.com", "123456", "firstone", "lastone")
    auth_dic2 = auth_login("valid2@gmail.com", "123456")
    token2 = auth_dic2['token']
    uid2 = auth_dic2['u_id']

    auth_dic3 = auth_register("valid3@gmail.com", "123456", "firstone", "lastone")
    auth_dic3 = auth_login("valid3@gmail.com", "123456")
    token3 = auth_dic3['token']

    channelid_dic1 = channels_create(token1, "channel 1", True)
    channel_id1 = channelid_dic1['channel_id']

    channelid_dic2 = channels_create(token1, "channel 2", True)
    channel_id2 = channelid_dic2['channel_id']
    # SETUP END

    # successful test
    assert channel_invite(token1, channel_id1, uid2) == {}

    # error test
    with pytest.raises(ValueError):
        # the channel if does not exist
        channel_invite(token1, 10, uid2)

    with pytest.raises(AccessError):
        # channel_id does not refer to a valid channel that the authorised user is part of.
        channel_invite(token3, channel_id2, uid2)

    with pytest.raises(ValueError):
        # u_id does not refer to a valid user
        # assume u_id 5 does not refer to a valid user
        channel_invite(token1, channel_id1, 10)

    with pytest.raises(ValueError):
        # u_id does not refer to a valid user
        # invite the user that is in channel (by calling function above, uid2 is in channel)
        channel_invite(token2, channel_id1, uid1)

    # logout
    auth_logout(token1)
    auth_logout(token2)
    auth_logout(token3)

    reset_data()
