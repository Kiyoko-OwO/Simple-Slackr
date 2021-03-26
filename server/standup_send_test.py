import pytest
from server.data_structure import reset_data
from server.error import AccessError
from server.error import ValueError
from server.auth import auth_register
from server.auth import auth_logout
from server.channel import channels_create
from server.standup import standup_send
from server.standup import standup_start



def test_standup_send():
    reset_data()
    #SETUP Begin
    authRegDict1 = auth_register("john@gmail.com", "qwerty", "John", "Smith")
    token1 = authRegDict1['token']
    channelCreateDict1 = channels_create(token1, 'New Channel', True)
    channel_id1 = channelCreateDict1['channel_id']

    authRegDict2 = auth_register("jim@gmail.com", "asdfgh", "Jim", "Smith")
    token2 = authRegDict2['token']

    channelCreateDict2 = channels_create(token2, 'New Channel2', True)
    channel_id2 = channelCreateDict2['channel_id']

    standup_start(token1, channel_id1, 7)
    #User 2 has not joined the 'New Channel' created by user 1
    #SETUP End

    #Test Case 1: Successful message sent to get bufferred in the standup queue
    assert standup_send(token1, channel_id1, 'Hello') == {}

    #Test Case 2: Unsuccessful message due to channel not existing
    with pytest.raises(ValueError):
        standup_send(token1, 10, 'Hello') #Invalid channel ID hence the unsuccessful message

    #Test Case 3: Unsuccessful message due to message being more than 1000 characters
    with pytest.raises(ValueError):
        standup_send(token1, channel_id1, 'a'*1001)

    #Test Case 4: Unsuccessful message due to user not being a member of the channel
    with pytest.raises(AccessError):
        #user 2 has not joined the channel created by user 1 so the message is Unsuccessful
        standup_send(token2, channel_id1, 'Hello')

    #Test Case 5: Unsuccessful standup message due to standup not being active
    with pytest.raises(ValueError):
        standup_send(token2, channel_id2, 'Hello')

    auth_logout(token1)
    auth_logout(token2)

    reset_data()
