from server.data_structure import getdata
from server.Helper_functions import get_user_from_token
from server.check_error import check_tokenlogin

def search(token, query_str):
    check_tokenlogin(token)
    channels = getdata()['channels']
    auser_dic = get_user_from_token(token)
    auid = auser_dic['u_id']

    collection = []
    for channel in channels:
    # firstly search fot all the channels the user is in
        if auid in channel['all_members']:
            for message in channel['messages']:
            #then search for all the messages this user sent in a channel
                if query_str in message['message']:
                # lastly append the message to the collection
                    collection.append(message)

    return {'messages' : collection}
