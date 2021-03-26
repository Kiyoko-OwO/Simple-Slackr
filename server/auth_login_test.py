import pytest
from server.auth import auth_register
from server.auth import auth_login
from server.auth import auth_logout
from server.data_structure import reset_data
from server.error import ValueError

def test_auth_login():

    '''
    assumption:
        1.goood@email.com is the only registered email.
        2.all the value errors have been modified into specfic words.
    '''
    reset_data()
    #successful test
    user_dic = auth_register('good@email.com', '1q2w3e4r', 'HAHA', 'JIANG')
    login_dic = auth_login('good@email.com', '1q2w3e4r')
    assert user_dic['u_id'] == login_dic['u_id']
    token = login_dic['token']

    #test1: login with invalid email:
    with pytest.raises(ValueError, match=r'Invalid email'):
        auth_login('wrongemail.com', '1q2w3e4r')

    #test2: login with email which doesn't belong to a user:
    with pytest.raises(ValueError, match=r'Email entered does not belong to a user'):
        auth_login("notuser@eamil.com", "123456")

    #test3: login with a user's email but the password is wrong:
    with pytest.raises(ValueError, match=r'Password incorrect'):
        auth_login('good@email.com', 'wrongpassword')

    auth_logout(token)
    reset_data()
