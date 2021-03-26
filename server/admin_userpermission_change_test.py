import pytest
from server.auth import auth_register
from server.auth import auth_login
from server.auth import auth_logout
from server.admin_userpermission_change import admin_userpermission_change
from server.data_structure import reset_data
from server.error import AccessError
from server.error import ValueError

def test_admin_userpermission_change():

    '''
    assumption:
        1.goood@email.com is the only registered email for now.
        2.all the value errors have been modified into specfic words.
        3.there is a permission id dictionary which contains 3 different types of permission id.
        4.haha@email.com hasn't been registered.
    '''
    #successful test:
    reset_data()
    auth_dic1 = auth_register("valid1@gmail.com", "123456", "firstone", "lastone")
    auth_dic1 = auth_login("valid1@gmail.com", "123456")
    token1 = auth_dic1['token']
    uid1 = auth_dic1['u_id']

    auth_dic2 = auth_register("valid2@gmail.com", "123456", "firstone", "lastone")
    auth_dic2 = auth_login("valid2@gmail.com", "123456")
    token2 = auth_dic2['token']
    uid2 = auth_dic2['u_id']

    auth_dic3 = auth_register("valid3@gmail.com", "123456", "firstone", "lastone")
    auth_dic3 = auth_login("valid3@gmail.com", "123456")
    token3 = auth_dic3['token']

    assert admin_userpermission_change(token1, uid2, 1) == {}

    #test1:u_id does not refer to a valid user
    with pytest.raises(ValueError):
        admin_userpermission_change(token1, 10, 1)

    #test2:permission_id does not refer to a value permission
    with pytest.raises(ValueError, match=r'permission_id does not refer to a value permission'):
        admin_userpermission_change(token1, uid2, 10)

    #test3:The authorised user is not an admin or owner
    with pytest.raises(AccessError, match=r'the authorised user is not an admin or owner'):
        admin_userpermission_change(token3, uid1, 1)

    auth_logout(token1)
    auth_logout(token2)
    auth_logout(token3)

    reset_data()
