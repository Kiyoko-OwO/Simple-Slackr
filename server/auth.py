from server.data_structure import getdata
from server.data_structure import get_permission_ids
from server.Helper_functions import get_user_from_email
from server.send_email import send_mail
from server.auth_helper import generateToken
from server.auth_helper import encode
from server.auth_helper import creatHandle
from server.auth_helper import generaterestcode
from server.check_error import check_validemail
from server.check_error import check_validpassword
from server.check_error import check_validname
from server.check_error import check_tokenlogin
from server.error import ValueError

######################### auth functions ########################################
def auth_register(email, password, name_first, name_last):
    #set up the initial value
    data = getdata()
    permission_ids_dic = get_permission_ids()
    owner = permission_ids_dic['Owner']
    member = permission_ids_dic['Member']
    uid = 0

    # argument checking
    # check password
    check_validpassword(password)

    # check email
    check_validemail(email)

    # check firstname, lastname
    check_validname(name_first, name_last)

    # get a new u_id for new user, and check whether the email has been used
    for user in data['users']:
        uid = user['u_id']
        if user['email'] == email:
            raise ValueError("email has been used.")
    uid = uid + 1

    # if uid = 1, which means this is the first one to register the slackr
    # this user is the owner of slackr
    # else the user is just a member
    if uid == owner:
        permissionid = owner
    else:
        permissionid = member

    handle = creatHandle(name_first, name_last)
    userdic = {
        'email': email,
        'password': str(encode({'password': password})),
        'u_id': uid,
        'name_first': name_first,
        'name_last': name_last,
        'is_log_in': True,
        'handle': handle,
        'permission_id':permissionid,
        'profile_img_url': None
    }

    token = generateToken(userdic)
    userdic.update({'token':token})

    data['users'].append(userdic)

    return {'u_id': uid, 'token': token}



def auth_login(email, password):
    password = str(encode({'password' : password}))

    check_validemail(email)

    user_dic = get_user_from_email(email)

    # if not find the email in the user, raise error
    if not user_dic:
        raise ValueError("Email entered does not belong to a user")

    # if find the user, and password correct
    if user_dic['password'] == password:
        user_dic['is_log_in'] = True
        return {'u_id': user_dic['u_id'], 'token': user_dic['token']}
    # if find the user, but password not correct
    raise ValueError("Password incorrect")



def auth_logout(token):
    # if the token is vaild
    # check if token login
    check_tokenlogin(token)
    return{'is_success' : True}


def auth_passwordreset_request(email):
    resetcode = generaterestcode()

    user_dic = get_user_from_email(email)
    if not user_dic:
        raise ValueError("Email not exists")

    user_dic.update({'resetCode': resetcode})
    send_mail(resetcode, email)
    return {}

def auth_passwordreset_reset(resetCode, newPassword):
    #verify if this user is the correct user then check the format of the new password
    #then update data
    data = getdata()
    check_validpassword(newPassword)
    newPassword = str(encode({'password': newPassword}))

    for user in data['users']:
        if user['resetCode'] == resetCode:
            user['password'] = newPassword
            return {}

    raise ValueError("not a vaild reset code")
