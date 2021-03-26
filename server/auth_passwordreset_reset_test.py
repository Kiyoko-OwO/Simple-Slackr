import pytest
from server.auth import auth_passwordreset_reset
from server.data_structure import reset_data
from server.error import ValueError


def test_auth_passwordreset_reset():

    '''
    assumption:
        1.good@email.com is the only registered email.
        2.all the value errors have been modified into specfic words.
        3.there is a reset code which is '12345' in the email dic.
        4.the old password of good@email.com is 1q2w3e4r.
    '''
    reset_data()
    #successful test:
    # hard to test the successful test,cause we cannot get the resetcode

    #test1: reset_code is not a valid reset code (hard to test, cuz we do not know reset_code

    with pytest.raises(ValueError):
        auth_passwordreset_reset('54321', 'r4e3w2q1')

    #test2: Password entered is not a valid password
    with pytest.raises(ValueError):
        auth_passwordreset_reset('12345', '1')

    reset_data()
