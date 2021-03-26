import pytest
from server.auth import auth_register
from server.auth import auth_login
from server.auth import auth_logout
from server.user_profile import user_profile_setname
from server.data_structure import reset_data
from server.error import ValueError

def test_user_profile_setname():
    reset_data()
    #SETUP Begin
    authRegDict1 = auth_register("john@gmail.com", "qwerty", "John", "Smith")
    auth_login("john@gmail.com", "qwerty")
    token1 = authRegDict1['token']
    #SETUP End

    #Test Case 1: successful update of authorised user's first and last name
    user_profile_setname(token1, "Jim", "Smiths")

    #Test Case 2: Successful update of user's first and last name
    # containing allowed non-alphabetical character
    user_profile_setname(token1, "Karl-Anthony", "Towns")

    #Test Case 3 Unsuccessful update of user's first and last name
    # due to first name exceeding character limit
    with pytest.raises(ValueError, match='Invalid first name length'):
        user_profile_setname(token1, "a"*51, "Smith")

    #Test Case 4: Unsuccessful update of first and last name due to last name exceeding limit
    with pytest.raises(ValueError, match='Invalid last name length'):
        user_profile_setname(token1, "John", "a"*51)

    auth_logout(token1)

    reset_data()
