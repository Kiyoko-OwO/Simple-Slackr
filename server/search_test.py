from server.auth import auth_register
from server.auth import auth_login
from server.auth import auth_logout
from server.channel import channels_create
from server.message import message_send
from server.search import search
from server.data_structure import reset_data


def test_search():

    '''
    assumption:
        1.goood@email.com is the only registered email for now.
        2.all the value errors have been modified into specfic words.
        3.the channel called "channelname" hasn't been created
    '''

    #successful test:
    #login
    reset_data()
    auth_register('good@email.com', 'q1w2e3r4', 'BEAR', 'XI')
    login1_dic = auth_login('good@email.com', 'q1w2e3r4')
    token = login1_dic['token']
    #create a channel
    channelValue = channels_create(token, "channelname", True)
    channel_id = channelValue['channel_id']
    #sending a message
    message_send(token, channel_id, "1q2w3e4r")
    #search
    messages_dic = search(token, "1q")
    assert messages_dic['messages'][0]['message'] == "1q2w3e4r"
    #logout
    auth_logout(token)
    reset_data()
