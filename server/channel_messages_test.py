import pytest
from server.auth import auth_register
from server.auth import auth_login
from server.auth import auth_logout
from server.channel import channels_create
from server.channel import channel_messages
from server.message import message_send
from server.data_structure import reset_data
from server.error import AccessError
from server.error import ValueError


'''
assume registered users stay between functions
the other data(like channels, messages) is reset
'''


def test_channel_messages():
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
    # assume the total number of messages in the channel is 0
    # which means there is no message in the channel
    # assume the start number is 0

    # send a message to channel1
    message_send(token1, channel_id1, "hello")
    channel_messages(token1, channel_id1, 0)


    # error test
    with pytest.raises(ValueError):
        # Channel (based on ID) does not exist
        # assume the channel ID 2 does not exist
        channel_messages(token1, 10, 0)

    with pytest.raises(ValueError):
        # start is greater than the total number of messages in the channel
        # the total number of messages is 1, start is 2
        channel_messages(token1, channel_id1, 2)

    with pytest.raises(AccessError):
        # Authorised user is not a member of channel with channel_id
        channel_messages(token2, channel_id1, 0)

    # logout
    auth_logout(token1)
    auth_logout(token2)
    reset_data()
