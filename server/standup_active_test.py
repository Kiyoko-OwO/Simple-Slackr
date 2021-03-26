import pytest
from server.data_structure import reset_data
from server.error import AccessError
from server.error import ValueError
from server.auth import auth_register
from server.auth import auth_logout
from server.channel import channels_create
from server.standup import standup_start
from server.standup import standup_active

def test_standup_active():
    reset_data()
    #SETUP Begin
    authRegDict1 = auth_register("john@gmail.com", "qwerty", "John", "Smith")
    token1 = authRegDict1['token']
    channelCreateDict1 = channels_create(token1, 'New Channel', True)
    channel_id1 = channelCreateDict1['channel_id']

    authRegDict2 = auth_register("jim@gmail.com", "asdfgh", "Jim", "Smith")
    token2 = authRegDict2['token']


    assert standup_active(token1, channel_id1) == {'is_active' : False, 'time_finish' : None}
    standup_start(token1, channel_id1, 5)
    standup_dic = standup_active(token1, channel_id1)
    assert standup_dic['is_active']

    with pytest.raises(ValueError):
        standup_active(token1, 10)

    with pytest.raises(AccessError):
        standup_active(token2, channel_id1)

    auth_logout(token1)
    auth_logout(token2)
