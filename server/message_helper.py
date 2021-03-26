from datetime import datetime
from threading import Timer
################################ helper function for message and standup #########################

class CustomTimer(Timer):
    def __init__(self, interval, function, args=[], kwargs={}):
        self._original_function = function
        super(CustomTimer, self).__init__(
            interval, self._do_execute, args, kwargs)

    def _do_execute(self, *a, **kw):
        self.result = self._original_function(*a, **kw)

    def join(self):
        super(CustomTimer, self).join()
        return self.result


 # convert timestamp into datetime
def convert_date(timestamp):
    utc_date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return datetime.strptime(utc_date, '%Y-%m-%d %H:%M:%S')

def helper_is_the_user_reacted(message, uid):
# check from the u_id if the user has reacted
    if message['u_id'] == uid:
        return True
    return False

def helper_check_react_exists(reacts, react_id):
    for react in reacts:
        if react_id == react['react_id']:
            return react
    return False

def helper_send_message(message_list, message, auid):
    m_id = 0
    # initalize the id to be 1
    if len(message_list) == 0:
        m_id = 1
    else:
    # the id will be automaticlly updated and once a message is sent,
    # it will be appended into the message list of the channel.
        m_id = message_list[len(message_list) - 1]['message_id'] + 1
    message_list.append({
        'message_id' : m_id,
        'u_id' : auid,
        'message' : message,
        'time_created' : datetime.timestamp(datetime.utcnow()),
        'reacts' : [],
        'is_pinned' : False
    })
    return m_id

def helper_standup(channel_dic, auid):
    # send the standup message and make the initialize channel standup
    channel_dic['standup_is_active'] = False
    helper_send_message(channel_dic['messages'], channel_dic['standup_messages'], auid)
    channel_dic['standup_messages'] = ''
    channel_dic['standup_time_finish'] = None
