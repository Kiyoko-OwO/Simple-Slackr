import pytest
from server.auth import auth_register
from server.auth import auth_login
from server.auth import auth_logout
from server.user_profile import user_profile_sethandle
from server.data_structure import reset_data
from server.error import ValueError


def test_user_profile_sethandle():
    reset_data()
    #SETUP Begin
    authRegDict1 = auth_register("john@gmail.com", "qwerty", "John", "Smith")
    token1 = authRegDict1['token']
    auth_login("john@gmail.com", "qwerty")

    authRegDict2 = auth_register("john1@gmail.com", "qwerty1", "Johnn", "Smithh")
    token2 = authRegDict2['token']
    auth_login("john1@gmail.com", "qwerty1")
    #SETUP End

    #Test Case 1: Successful update of user's display name
    user_profile_sethandle(token1, "jsmith")

    #Test Case 2: Unsuccessful update of user's display name due to exceeding of character limit
    with pytest.raises(ValueError, match='Display name exceeds character limit'):
        user_profile_sethandle(token1, 'jsmith12345678dfghnmdfghj90qwerty')

    #Test Case 3: Unsuccessful update of user's display name because the handle is too short
    with pytest.raises(ValueError):
        user_profile_sethandle(token1, 'j')


    #Test Case 4: Unsuccessful update of user's display name due to it containing an offensive word
    with pytest.raises(ValueError):
        user_profile_sethandle(token2, 'jsmith') #User accidentally includes offensive word

    auth_logout(token1)
    auth_logout(token2)

    reset_data()
