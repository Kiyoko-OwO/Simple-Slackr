import pytest
from server.auth import auth_register
from server.auth import auth_passwordreset_request
from server.data_structure import reset_data
from server.error import ValueError

def test_auth_passwordreset_request():

    '''
    assumption:
        1.goood@email.com is the only registered email.
        2.all the value errors have been modified into specfic words.
        3.assume the reset code is 12345
    '''
    reset_data()
    auth_register('sherryqwq4@gmail.com', '1q2w3e4r', 'HAHA', 'JIANG')
    #successful test:
    # hard to test
    assert (auth_passwordreset_request("sherryqwq4@gmail.com") == {})

    #test1: email hasn't been resgitered.
    with pytest.raises(ValueError):
        auth_passwordreset_request('frog@email.com')

    reset_data()
