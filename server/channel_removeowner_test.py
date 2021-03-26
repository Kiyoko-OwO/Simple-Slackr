import pytest
from server.auth import auth_register
from server.auth import auth_login
from server.auth import auth_logout
from server.channel import channels_create
from server.channel import channel_join
from server.channel import channel_addowner
from server.channel import channel_removeowner
from server.data_structure import reset_data
from server.error import AccessError
from server.error import ValueError

'''
assume registered users stay between functions
the other data(like channels, messages) is reset
'''

def test_channel_removeowner():
    reset_data()
    # SETUP BEGIN
    # Assume all users have registered in function: test_channel_invite()
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
    uid3 = auth_dic3['u_id']

    channelid_dic1 = channels_create(token1, "channel 1", True)
    channel_id1 = channelid_dic1['channel_id']

    channel_join(token2, channel_id1)
    channel_addowner(token1, channel_id1, uid2)

    # create a private channel
    channelid_dic2 = channels_create(token2, "channel 2", True)
    channel_id2 = channelid_dic2['channel_id']
    channel_join(token3, channel_id2)
    channel_addowner(token2, channel_id2, uid3)

    # SETUP END

    # successful test
    assert channel_removeowner(token1, channel_id1, uid2) == {}
    assert channel_removeowner(token1, channel_id2, uid2) == {}

    # error test
    with pytest.raises(ValueError):
        # Channel (based on ID) does not exist
        # Assume the channel id 3 does not exist
        channel_removeowner(token1, 3, uid2)

    with pytest.raises(ValueError):
        # When user with user id u_id is not a member of the channel
        channel_removeowner(token1, channel_id1, uid3)

    with pytest.raises(ValueError):
        # When authorised user is the only owner in the channel
        # assume the user1 is the only owner of channel1
        channel_removeowner(token1, channel_id1, uid1)

    with pytest.raises(AccessError):
        # when the authorised user is not an owner of the slackr, or an owner of this channel
        channel_removeowner(token2, channel_id1, uid1)

    # logout
    auth_logout(token1)
    auth_logout(token2)
    auth_logout(token3)

    reset_data()
