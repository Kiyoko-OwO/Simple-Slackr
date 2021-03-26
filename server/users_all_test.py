from server.auth import auth_register
from server.auth import auth_login
from server.auth import auth_logout
from server.user_profile import users_all
from server.data_structure import reset_data

def test_users_all():
    reset_data()
    authRegDict1 = auth_register("john@gmail.com", "qwerty", "John", "Smith")
    token1 = authRegDict1['token']
    auth_login("john@gmail.com", "qwerty")
    # successful test
    users_all(token1)

    auth_logout(token1)
    reset_data()
