import json
import uuid
from flaskapp import app
from flask import request, Response, send_file, send_from_directory, make_response
import datetime

from sql_queries import sql_queries

class API():

    @staticmethod
    def login():
        if API.is_valid_user(request.authorization):
            #then we've already logged on.
            dict_local = {'code': 200}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string 
        else:
            #not a good cookie and no login.
            dict_local = {'code': 31, 'message': "login failed"}
            return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
            return return_string	

    

    @staticmethod
    def is_valid_user(auth):
    	data_get = sql_queries.get_user(auth.username, auth.password)
    	if data_get is not None:
    		return True
    	else:
    		return False

app.add_url_rule('/login', 'login', API.login, methods=['GET'])
# app.add_url_rule('/logoff', 'logoff', User.logoff, methods=['GET'])
# app.add_url_rule('/list_all_users', 'list_all_users', User.list_all_users, methods=['GET'])
# app.add_url_rule('/register_user', 'register_user', User.register_user, methods=['POST'])
