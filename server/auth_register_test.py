import pytest
from server.auth import auth_register
from server.auth import auth_login
from server.auth import auth_logout
from server.data_structure import reset_data
from server.error import ValueError

def test_auth_register():

    '''
    assumption:
        1.goood@email.com is the only registered email for now.
        2.all the value errors have been modified into specfic words.
        3.the frog@email.com is a valid email which hasn't been registered.
    '''
    reset_data()

    #successful test
    register_dic = auth_register('good@email.com', 'q1w2e3r4', 'BEAR', 'XI')
    login_dic1 = auth_login('good@email.com', 'q1w2e3r4')
    token = login_dic1['token']
    assert register_dic['u_id'] == login_dic1['u_id']

    #test1: register with an invalid email
    with pytest.raises(ValueError, match=r'Invalid email'):
        auth_register('wrongemail.com', '1q2w3e4r', 'HAHA', 'JIANG')

    #test2: the email has been registered
    with pytest.raises(ValueError, match=r'email has been used'):
        auth_register('good@email.com', '1q2w3e4r', 'HHAHA', 'JJIANG')

    #test3: the password used for registering with wrong format
    with pytest.raises(ValueError, match=r'Invalid password'):
        auth_register('good@email.com', '123', 'HAHA', 'JIANG')

    #test4: the user's first name is too long
    with pytest.raises(ValueError, match=r'Invalid first name length'):
        auth_register('frog@email.com', '123456', 'HAHA'*13, 'JIANG')

    #test5: the user's last name is too long
    with pytest.raises(ValueError, match=r'Invalid last name length'):
        auth_register('frog@email.com', '123456', 'HAHA', 'JIANG'*11)

    auth_logout(token)

    reset_data()
