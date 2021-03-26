import pytest
from server.auth import auth_register
from server.auth import auth_login
from server.auth import auth_logout
from server.user_profile import user_profile
from server.data_structure import reset_data
from server.error import ValueError

def test_user_profile():
    reset_data()
    #SETUP Begin - initialisation of variables for calling the function
    authRegDict1 = auth_register("john@gmail.com", "qwerty", "John", "Smith")
    auth_login("john@gmail.com", "qwerty")
    token1 = authRegDict1['token']
    userId1 = authRegDict1['u_id']
    #SETUP End

    #Test Case 1: successful case where calling user_profile returns the desired result
    assert user_profile(token1, userId1)['email'] == "john@gmail.com"

    #Test Case 2: Unsuccessful case where an invalid user ID is provided
    with pytest.raises(ValueError, match='not a valid u_id'):
        # the uis 10 do not exist
        user_profile(token1, 10)

    auth_logout(token1)
    reset_data()
