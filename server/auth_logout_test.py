from server.auth import auth_register
from server.auth import auth_login
from server.auth import auth_logout
from server.data_structure import reset_data
def test_auth_logout():

    '''
    assumption:
        1.goood@email.com is the only registered email.
        2.all the value errors have been modified into specfic words.
    '''

    #successful test
    auth_register('good@email.com', 'q1w2e3r4', 'BEAR', 'XI')
    login_dic = auth_login('good@email.com', 'q1w2e3r4')
    assert auth_logout(login_dic['token']) == {'is_success' : True}

    reset_data()
