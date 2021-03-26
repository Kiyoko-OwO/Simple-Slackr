import datetime
import pytest
from server.data_structure import reset_data
from server.error import AccessError
from server.error import ValueError
from server.auth import auth_register
from server.auth import auth_logout
from server.channel import channels_create
from server.standup import standup_start


def test_standup_start():
    reset_data()
    #SETUP Begin
    authRegDict1 = auth_register("john@gmail.com", "qwerty", "John", "Smith")
    token1 = authRegDict1['token']
    channelCreateDict1 = channels_create(token1, 'New Channel', True)
    channel_id1 = channelCreateDict1['channel_id']

    authRegDict2 = auth_register("jim@gmail.com", "asdfgh", "Jim", "Smith")
    token2 = authRegDict2['token']
    #User 2 has not joined the 'New Channel' created by user 1
    #SETUP End
    #Test Case 1: Successful test case
    timestamp = int(datetime.datetime.now().strftime("%s")) + 5
    finish = standup_start(token1, channel_id1, 5)['time_finish']
    assert finish == timestamp
    # Successful test case should return datetime of current time + 5 minutes

    #Test Case 2: Unsuccessful test case where channel does not exist
    with pytest.raises(ValueError):
        standup_start(token1, 10, 5) #channel ID is invalid hence the unsuccessful function call

    #Test Case 3: Unsuccessful start of standup
    # due to user not being a member of the channel he/she is trying to send the message in
    with pytest.raises(AccessError):
        standup_start(token2, channel_id1, 5)

    #Test Case 3: Unsuccessful start of standup
    # because An active standup is currently running in this channel
    with pytest.raises(ValueError):
        standup_start(token1, channel_id1, 5)

    auth_logout(token1)
    auth_logout(token2)
    reset_data()
