from json import dumps
from flask import request
from str2bool import str2bool
from server.flask_helper import get_args
from server.auth import auth_login
from server.auth import auth_logout
from server.auth import auth_register
from server.auth import auth_passwordreset_request
from server.auth import auth_passwordreset_reset
from server.channel import channel_invite
from server.channel import channel_details
from server.channel import channel_messages
from server.channel import channel_leave
from server.channel import channel_join
from server.channel import channel_addowner
from server.channel import channel_removeowner
from server.channel import channels_list
from server.channel import channels_listall
from server.channel import channels_create
from server.message import message_sendlater
from server.message import message_send
from server.message import message_remove
from server.message import message_edit
from server.message import message_react
from server.message import message_unreact
from server.message import message_pin
from server.message import message_unpin
from server.user_profile import user_profile
from server.user_profile import user_profile_setname
from server.user_profile import user_profile_setemail
from server.user_profile import user_profile_sethandle
from server.user_profile import user_profiles_uploadphoto
from server.user_profile import users_all
from server.search import search
from server.admin_userpermission_change import admin_userpermission_change
from server.standup import standup_start
from server.standup import standup_send
from server.standup import standup_active
from server.error import APP



@APP.route('/echo/get', methods=['GET'])
def echo1():
    """ Description of function """
    return dumps({
        'echo': request.form.get('echo'),
    })


@APP.route('/echo/post', methods=['POST'])
def echo2():
    """ Description of function """
    return dumps({
        'echo': request.form.get('echo'),
    })

###############################AUTH############################################


@APP.route('/auth/register', methods=['POST'])
def app_auth_register():
    email = get_args("email")
    password = get_args('password')
    name_first = get_args('name_first')
    name_last = get_args('name_last')
    return dumps(auth_register(email, password, name_first, name_last))


@APP.route('/auth/login', methods=['POST'])
def app_auth_login():
    email = get_args('email')
    password = get_args('password')
    return dumps(auth_login(email, password))


@APP.route('/auth/logout', methods=['POST'])
def app_auth_logout():
    token = get_args('token')
    return dumps(auth_logout(token))


@APP.route('/auth/passwordreset/request', methods=['POST'])
def app_auth_passwordreset_request():
    user_email = get_args('email')
    return dumps(auth_passwordreset_request(user_email))


@APP.route('/auth/passwordreset/reset', methods=['POST'])
def app_auth_password_reset():
    reset_code = get_args('reset_code')
    new_password = get_args('new_password')
    return dumps(auth_passwordreset_reset(reset_code, new_password))

################################CHANNEL########################################


@APP.route('/channel/invite', methods=['POST'])
def app_channel_invite():
    channel_id = int(get_args('channel_id'))
    token = get_args('token')
    u_id = int(get_args('u_id'))
    return dumps(channel_invite(token, channel_id, u_id))


@APP.route('/channel/details', methods=['GET'])
def app_channel_details():
    token = get_args('token')
    channel_id = int(get_args('channel_id'))
    return dumps(channel_details(token, channel_id))


@APP.route('/channel/messages', methods=['GET'])
def app_channel_messages():
    token = get_args('token')
    channel_id = int(get_args('channel_id'))
    start = int(get_args('start'))

    return dumps(channel_messages(token, channel_id, start))


@APP.route('/channels/create', methods=['POST'])
def app_channels_create():
    token = get_args('token')
    name = get_args('name')
    is_public = str2bool(get_args('is_public'))

    return dumps(channels_create(token, name, is_public))


@APP.route('/channels/listall', methods=['GET'])
def app_channel_listall():
    token = get_args('token')

    return dumps(channels_listall(token))


@APP.route('/channels/list', methods=['GET'])
def app_channels_list():
    token = get_args('token')

    return dumps(channels_list(token))


@APP.route('/channel/join', methods=['POST'])
def app_channel_join():
    token = get_args('token')
    channel_id = int(get_args('channel_id'))

    return dumps(channel_join(token, channel_id))


@APP.route('/channel/leave', methods=['POST'])
def app_channel_leave():
    token = get_args('token')
    channel_id = int(get_args('channel_id'))

    return dumps(channel_leave(token, channel_id))


@APP.route('/channel/addowner', methods=['POST'])
def app_channel_addowner():
    token = get_args('token')
    channel_id = int(get_args('channel_id'))
    u_id = int(get_args('u_id'))

    return dumps(channel_addowner(token, channel_id, u_id))


@APP.route('/channel/removeowner', methods=['POST'])
def app_channel_removeowner():
    token = get_args('token')
    channel_id = int(get_args('channel_id'))
    u_id = int(get_args('u_id'))

    return dumps(channel_removeowner(token, channel_id, u_id))

###################################MESSAGE#####################################


@APP.route('/message/sendlater', methods=['POST'])
def sendlater():
    token = get_args('token')
    channel_id = int(get_args('channel_id'))
    message = get_args('message')
    time_send = int(get_args('time_sent'))
    return dumps(message_sendlater(token, channel_id, message, time_send))


@APP.route('/message/send', methods=['POST'])
def send():
    token = get_args('token')
    channel_id = int(get_args('channel_id'))
    message = get_args('message')
    return dumps(message_send(token, channel_id, message))


@APP.route('/message/remove', methods=['DELETE'])
def remove():
    token = get_args('token')
    message_id = int(get_args('message_id'))
    return dumps(message_remove(token, message_id))


@APP.route('/message/edit', methods=['PUT'])
def edit():
    token = get_args('token')
    message_id = int(get_args('message_id'))
    message = get_args('message')
    return dumps(message_edit(token, message_id, message))


@APP.route('/message/react', methods=['POST'])
def react():
    token = get_args('token')
    message_id = int(get_args('message_id'))
    react_id = int(get_args('react_id'))
    return dumps(message_react(token, message_id, react_id))


@APP.route('/message/unreact', methods=['POST'])
def unreact():
    token = get_args('token')
    message_id = int(get_args('message_id'))
    react_id = int(get_args('react_id'))
    return dumps(message_unreact(token, message_id, react_id))


@APP.route('/message/pin', methods=['POST'])
def pin():
    token = get_args('token')
    message_id = int(get_args('message_id'))
    return dumps(message_pin(token, message_id))


@APP.route('/message/unpin', methods=['POST'])
def unpin():
    token = get_args('token')
    message_id = int(get_args('message_id'))
    return dumps(message_unpin(token, message_id))


@APP.route('/user/profile', methods=['GET'])
def userprofile():
    token = get_args('token')
    u_id = int(get_args('u_id'))

    return dumps(user_profile(token, u_id))


@APP.route('/user/profile/setname', methods=['PUT'])
def userprofile_setname():
    token = get_args('token')
    name_first = get_args('name_first')
    name_last = get_args('name_last')

    return dumps(user_profile_setname(token, name_first, name_last))


@APP.route('/user/profile/setemail', methods=['PUT'])
def userprofile_setemail():
    token = get_args('token')
    email = get_args('email')

    return dumps(user_profile_setemail(token, email))


@APP.route('/user/profile/sethandle', methods=['PUT'])
def userprofile_sethandle():
    token = get_args('token')
    handle_str = get_args('handle_str')

    return dumps(user_profile_sethandle(token, handle_str))

@APP.route('/user/profiles/uploadphoto', methods=['POST'])
def userprofile_uploadphoto():
    token = get_args('token')
    img_url = get_args('img_url')
    x_start = int(get_args('x_start'))
    y_start = int(get_args('y_start'))
    x_end = int(get_args('x_end'))
    y_end = int(get_args('y_end'))
    return dumps(user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end, 5001))

@APP.route('/users/all', methods=['GET'])
def usersall():
    token = get_args('token')
    return dumps(users_all(token))


@APP.route('/standup/start', methods=['POST'])
def standupstart():
    token = get_args('token')
    channel_id = int(get_args('channel_id'))
    length = int(get_args('length'))

    return dumps(standup_start(token, channel_id, length))

@APP.route('/standup/active', methods=['GET'])
def standupactive():
    token = get_args('token')
    channel_id = int(get_args('channel_id'))

    return dumps(standup_active(token, channel_id))

@APP.route('/standup/send', methods=['POST'])
def standupsend():
    token = get_args('token')
    channel_id = int(get_args('channel_id'))
    message = get_args('message')

    return dumps(standup_send(token, channel_id, message))

@APP.route('/search', methods=['GET'])
def app_search():
    token = get_args('token')
    query_str = get_args('query_str')
    return dumps(search(token, query_str))

@APP.route('/admin/userpermission/change', methods=['POST'])
def app_admin_userpermission_change():
    token = get_args('token')
    u_id = int(get_args('u_id'))
    permission_id = int(get_args('permission_id'))
    return dumps(admin_userpermission_change(token, u_id, permission_id))



if __name__ == '__main__':
    APP.run(debug=True, port=5001)
