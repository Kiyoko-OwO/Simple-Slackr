import pytest
from server.auth import auth_register
from server.auth import auth_login
from server.auth import auth_logout
from server.channel import channels_create
from server.channel import channel_details
from server.data_structure import reset_data
from server.error import ValueError

'''
assume registered users stay between functions
the other data(like channels, messages) is reset
'''
def test_channel_details():
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

    # SETUP END

    # successful test
    # assume channel_details function return the channel name
    # and the uid of the owner_members/members
    channel_dic = channel_details(token1, channel_id1)
    assert channel_dic['name'] == "channel 1"

    # error test
    with pytest.raises(ValueError):
        # Channel (based on ID) does not exist
        # assume channel ID 2 does not exist
        channel_details(token1, 10)
    '''
    with pytest.raises(AccessError):
        # Authorised user is not a member of channel with channel_id    
        # user2 is not a member of channel1
        channel_details(token2, channel_id1)
    '''
    # logout
    auth_logout(token1)
    auth_logout(token2)

    reset_data()
