from server.data_structure import get_permission_ids
from server.Helper_functions import get_user_from_uid
from server.Helper_functions import get_user_from_token
from server.Helper_functions import helper_check_user_admin
from server.check_error import check_tokenlogin
from server.check_error import check_validuid
from server.error import AccessError
from server.error import ValueError


def admin_userpermission_change(token, u_id, permission_id):
    check_tokenlogin(token)
    permission_ids = get_permission_ids()
    auser_dic = get_user_from_token(token)
    user_dic = get_user_from_uid(u_id)

    check_validuid(user_dic)

    # 3 types of permissions: 1. owner  2. admin  3. member
    # only 1 and 2 can change permission
    owner_id = permission_ids['Owner']
    admin_id = permission_ids['Admin']
    member_id = permission_ids['Member']

    if permission_id not in (owner_id, admin_id, member_id):
        raise ValueError("permission_id does not refer to a value permission")

    if not helper_check_user_admin(auser_dic):
        raise AccessError("the authorised user is not an admin or owner")

    user_dic['permission_id'] = permission_id

    return {}
