import pytest
from server.auth import auth_register
from server.auth import auth_login
from server.auth import auth_logout
from server.user_profile import user_profiles_uploadphoto
from server.data_structure import reset_data
from server.error import ValueError



def test_user_profiles_uploadphoto():
    reset_data()
    #SETUP Begin - initialisation of variables for calling the function
    authRegDict1 = auth_register("john@gmail.com", "qwerty", "John", "Smith")
    auth_login("john@gmail.com", "qwerty")
    token1 = authRegDict1['token']

    # successful test
    user_profiles_uploadphoto(token1, "https://www.flowerglossary.com/wp-content/uploads/2019/04/blue-rose.jpg", 0, 0, 100, 100, 5001)

    # error test
    # Image uploaded is not a JPG.
    with pytest.raises(ValueError):
        user_profiles_uploadphoto(token1, "https://www.baidu.com", 0, 0, 10, 10, 5001)

    # any of x_start, y_start, x_end, y_end are not within the dimensions of the image at the URL.
    with pytest.raises(ValueError):
        user_profiles_uploadphoto(token1, "https://www.flowerglossary.com/wp-content/uploads/2019/04/blue-rose.jpg", 10, 10, 0, 0, 5001)

    auth_logout(token1)