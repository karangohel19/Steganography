import requests
import json

#signup function
def signup(json_data):
    signup_request=requests.post("https://python-backend-server.herokuapp.com/user/signup",json=json_data,verify=True)
    text=signup_request.json()
    return {
          'message':text['message'],
          'status':signup_request.status_code
    }


#login function
def login(json_data):
    login_request=requests.post("https://python-backend-server.herokuapp.com/user/login",json=json_data,verify=True)
    text=login_request.json()
    return {
         'message':text['message'],
         'status':login_request.status_code
    }
    