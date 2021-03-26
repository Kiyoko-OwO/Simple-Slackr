import pytest
from server.auth import auth_register
from server.auth import auth_login
from server.auth import auth_logout
from server.user_profile import user_profile_setemail
from server.data_structure import reset_data
from server.error import ValueError

def test_user_profile_setemail():
    reset_data()
    #SETUP Begin
    authRegDict1 = auth_register("john@gmail.com", "qwerty", "John", "Smith")
    auth_login("john@gmail.com", "qwerty")
    token1 = authRegDict1['token']

    auth_register("john1@gmail.com", "qwerty", "John", "Smith")
    #SETUP End

    #Test Case 1: Successful update of user's email
    user_profile_setemail(token1, "john@hotmail.com")

    #Test Case 2: Unsuccessful update of user email because the email not change
    with pytest.raises(ValueError):
        user_profile_setemail(token1, "john@hotmail.com")

    #Test Case 3: Unsuccessful update of user email due to conflict with existing email
    with pytest.raises(ValueError):
        user_profile_setemail(token1, "jim.gmail.com")

    #Test Case 3: Unsuccessful update of user email because the email has been used
    with pytest.raises(ValueError):
        user_profile_setemail(token1, "john1@gmail.com")

    auth_logout(token1)

    reset_data()
