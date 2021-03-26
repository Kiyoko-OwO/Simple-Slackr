import random
import string
import jwt
from server.data_structure import getdata

###################### helper function for auth ###############################

# use jwt to generate the token
def generateToken(user):
    token = jwt.encode(user, 'H13A-HelloWorld', algorithm='HS256')
    return token.decode("utf-8")

# use jwt to encode the password
def encode(password):
    encode_jwt = jwt.encode(password, 'H13A-HelloWorld', algorithm='HS256')
    return encode_jwt

# get the handle of user
def creatHandle(first_name, last_name):
    max_length = 20
    handle = first_name.lower() + last_name.lower()
    # check the handle, if length of handle is bigger than 20, cutoff at 20 characters
    if len(handle) > max_length:
        handle = handle[:max_length]

    count_max = 10
    count_min = 0
    count = 0
    length = 0
    # check if the handle is unique
    # if it is not unique, modify the handle to make it unique
    # by adding the number at tail of the handle to modify the handle until it is the unique
    while not handle_is_unique(handle):
        if count == count_min:
            length = length + 1

        if len(handle) == max_length:
            handle = handle[:max_length-length]
            handle = handle_helper(length, handle)
        else:
            handle = handle_helper(length, handle)
            handle = handle + str(count)

        count = count + 1
        if count == count_max:
            count = count_min

    return handle

# if it need more than one number to make the handle unique
def handle_helper(length, handle):
    counter = 1
    if counter < length:
        handle = handle + str(9)
        counter = counter + 1
    return handle


# helper functions to check if handle is the unique
def handle_is_unique(handle):
    data = getdata()
    for user in data['users']:
        if user['handle'] == handle:
            return False
    return True

# to get a reset Code
def generaterestcode(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
