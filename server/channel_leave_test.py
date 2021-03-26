import pytest
from server.auth import auth_register
from server.auth import auth_login
from server.auth import auth_logout
from server.channel import channels_create
from server.channel import channel_join
from server.channel import channel_leave
from server.data_structure import reset_data
from server.error import AccessError
from server.error import ValueError


'''
assume registered users stay between functions
the other data(like channels, messages) is reset
'''
def test_channel_leave():
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

    channel_join(token2, channel_id1)
    # SETUP END

    # successful test
    assert channel_leave(token2, channel_id1) == {}

    # error test
    with pytest.raises(AccessError):
        # if the user is not a member of channel with channel id
        channel_leave(token2, channel_id1)

    # assume if no one in the channel, the channel will does not exist
    with pytest.raises(ValueError):
        # Channel (based on ID) does not exist
        channel_leave(token1, 10)

    # if there is only one owner in the channel, cannot remove
    with pytest.raises(ValueError):
        channel_leave(token1, channel_id1)

    # logout
    auth_logout(token1)
    auth_logout(token2)

    reset_data()
