data = {
    'users': [{
        'email' : '',
        'password' : '',
        'u_id' : 0,
        'token' : '',
        'name_first' : '',
        'name_last' : '',
        'is_log_in' : False,
        'handle': '',
        'permission_id': '',
        'resetCode' : '',
        'profile_img_url': ''
    }],

    'channels': [{
        'channel_id':-1,
        'name':'',
        'is_public':'',
        'standup_messages': '',
        'standup_is_active':'',
        'standup_time_finish':'',
        'owner_members':[],     #uids
        'all_members':[],       #uids
        'messages': [{
            'message_id' : '',
            'u_id' : '',
            'message' : '',
            'time_created' : '',
            'reacts' : [{
                'react_id' : '',
                'u_ids' : [],
                'is_this_user_reacted' : ''
                }],
            'is_pinned' : ''
        }]

    }]


}

# permission id
permission_ids = {
    'Owner' : 1,
    'Admin' : 2,
    'Member' : 3
}


def getdata():
    global data
    return data

def get_permission_ids():
    global permission_ids
    return permission_ids
###############################################################################
# this reset_data function is used for reseting all the data after every pytest
def reset_data():
    global data
    data = {
        'users': [{
            'email' : '',
            'password' : '',
            'u_id' : 0,
            'token' : '',
            'name_first' : '',
            'name_last' : '',
            'is_log_in' : False,
            'handle': '',
            'permission_id': '',
            'resetCode' : '',
            'profile_img_url': ''
        }],

        'channels': [{
            'channel_id':-1,
            'name':'',
            'is_public':'',
            'standup_messages': [],
            'standup_is_active':'',
            'standup_time_finish':'',
            'owner_members':[],  #uids
            'all_members':[],  # uids

            'messages': [{
                'message_id' : '',
                'u_id' : '',
                'message' : '',
                'time_created' : '',
                'reacts' : [{
                    'react_id' : '',
                    'u_ids' : [],
                    'is_this_user_reacted' : ''
                    }],
                'is_pinned' : ''
            }]

        }]

    }
