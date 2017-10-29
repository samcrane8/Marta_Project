
from flask import Flask
import MySQLdb
import configparser

# mysql = None

class sql_queries():
    #TODO move this shit to ram


    @staticmethod
    def is_valid_login(username, password):
    	data_base = sql_queries.mysql_connection()
        cursor = data_base.cursor()

        cursor.execute(
            "SELECT * from USER where username = \"%s\" and password = \"%s\" " % username, password)
        data_get = cursor.fetchone()
        data_base.commit()
        return data_get




    @staticmethod
    def readConfig(option):

        # try catch
        if option == "MySQL":
            Config = configparser.ConfigParser()
            Config.read("config")
            MySQLhost = Config.get("MySQL Settings", "host")
            MySQLusername = Config.get("MySQL Settings", "username")
            MySQLpassword = Config.get("MySQL Settings", "password")
            database = Config.get("MySQL Settings", "database")
            return MySQLdb.connect(MySQLhost, MySQLusername, MySQLpassword, database)

        elif option == "save_path":
            Config = configparser.ConfigParser()
            Config.read("config")
            path = Config.get("File", "save_path")
            return path
        else:
            return None

    @staticmethod
    def mysql_connection():
        return sql_queries.readConfig("MySQL")
        # MySQLhost = "localhost"
        # MySQLusername = "python_backend"
        # MySQLpassword = "Secur1ty_1s_sexy"
        # database = "waterapp"
        # return MySQLdb.connect(MySQLhost, MySQLusername, MySQLpassword, database)

    @staticmethod
    def get_device_requests(device_id):
        data_base = sql_queries.mysql_connection()
        cursor = data_base.cursor()

        cursor.execute(
            "SELECT requests, created_at, status from device_requests where device_id = \"%s\" " % device_id)
        data_get = cursor.fetchone()
        data_base.commit()
        return data_get

    @staticmethod
    def owner_exist(owner):
        data_base = sql_queries.mysql_connection()
        cursor = data_base.cursor()

        cursor.execute("SELECT username FROM users where username = \"%s\" " % owner)
        data_get = cursor.fetchone()
        data_base.commit()

        if data_get is None:
            return False
        else:
            return True
