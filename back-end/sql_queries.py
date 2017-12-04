
from flask import Flask
import MySQLdb
import configparser

# mysql = None

class sql_queries():
	#TODO move this shit to ram

	@staticmethod
	def get_user(username, password):
		data_base = sql_queries.mysql_connection()
		cursor = data_base.cursor()
		to_execute = "SELECT * from USER where username = '{0}' and password = '{1}'".format(username, password)
		cursor.execute(to_execute)
		data_get = cursor.fetchone()
		data_base.commit()
		return data_get

	@staticmethod
	def username_available(username):
		data_base = sql_queries.mysql_connection()
		cursor = data_base.cursor()
		to_execute = "SELECT * from USER where username = '{0}'".format(username)
		cursor.execute(to_execute)
		data_get = cursor.fetchone()
		data_base.commit()
		return data_get is None

	@staticmethod
	def register_user(username, password, isAdmin):
		data_base = sql_queries.mysql_connection()
		cursor = data_base.cursor()
		to_execute = "INSERT into USER values ('{0}','{1}',{2})".format(username, password, isAdmin)
		cursor.execute(to_execute)
		data_get = cursor.fetchone()
		data_base.commit()
		return data_get is None

	@staticmethod
	def register_passenger(username, email):
		data_base = sql_queries.mysql_connection()
		cursor = data_base.cursor()
		to_execute = "INSERT into PASSENGER values ('{0}','{1}')".format(username, email)
		cursor.execute(to_execute)
		data_get = cursor.fetchone()
		data_base.commit()

	@staticmethod
	def add_station(stopid, fare, isopen, station_name, isbus):
		data_base = sql_queries.mysql_connection()
		cursor = data_base.cursor()
		isopen = int(isopen)
		isbus = int(isbus)
		to_execute = "INSERT into STATION values ('{0}','{1}', '{2}', '{3}', '{4}')".format(
			stopid, fare, isopen, station_name, isbus)
		cursor.execute(to_execute)
		data_get = cursor.fetchone()
		data_base.commit()

	@staticmethod
	def add_nearest_intersection(stopid, roads):
		data_base = sql_queries.mysql_connection()
		cursor = data_base.cursor()
		to_execute = "INSERT into INTERSECTION values ('{0}','{1}')".format(
			stopid, roads)
		cursor.execute(to_execute)
		data_get = cursor.fetchone()
		data_base.commit()

	@staticmethod
	def get_stations():
		data_base = sql_queries.mysql_connection()
		cursor = data_base.cursor()
		to_execute = "SELECT STATION.StopID, EntryFare, IsOpenFlagI, StationName, IsBusFlag, Roads from STATION left join INTERSECTION on STATION.StopID = INTERSECTION.StopID"
		cursor.execute(to_execute)
		data_get = cursor.fetchall()
		data_base.commit()
		return data_get

	@staticmethod
	def update_station(stopid, fare, isopen):
		data_base = sql_queries.mysql_connection()
		cursor = data_base.cursor()
		to_execute = "UPDATE STATION SET EntryFare = '{0}', IsOpenFlagI = '{1}' WHERE StopID = '{2}' ".format(fare,isopen,stopid)
		cursor.execute(to_execute)
		data_get = cursor.fetchall()
		data_base.commit()
		return data_get

	@staticmethod
	def is_username_taken(username):
		data_base = sql_queries.mysql_connection()
		cursor = data_base.cursor()
		to_execute = "SELECT * FROM USER where UserName = '{0}'".format(username)
		cursor.execute(to_execute)
		data_get = cursor.fetchone()
		data_base.commit()
		return data_get is not None

	@staticmethod
	def is_email_taken(email):
		data_base = sql_queries.mysql_connection()
		cursor = data_base.cursor()
		to_execute = "SELECT * FROM PASSENGER where email = '{0}'".format(email)
		cursor.execute(to_execute)
		data_get = cursor.fetchone()
		data_base.commit()
		return data_get is not None

	@staticmethod
	def is_admin(username):
		data_base = sql_queries.mysql_connection()
		cursor = data_base.cursor()
		to_execute = "SELECT isAdminFlag FROM USER where username = '{0}'".format(username)
		cursor.execute(to_execute)
		data_get, = cursor.fetchone()
		data_base.commit()
		return data_get == True

	@staticmethod
	def add_conflict(UName, CardID):
		data_base = sql_queries.mysql_connection()
		cursor = data_base.cursor()
		to_execute = "INSERT into CONFLICT values ('{0}', '{1}', CURRENT_TIMESTAMP)".format(UName, CardID)
		cursor.execute(to_execute)
		data_get = cursor.fetchall()
		data_base.commit()
		return data_get

	@staticmethod
	def get_conflicts():
		data_base = sql_queries.mysql_connection()
		cursor = data_base.cursor()
		to_execute = "SELECT CONFLICT.UName, CONFLICT.CardID, EventDT, Value, BREEZECARD.UName from CONFLICT inner join BREEZECARD on BREEZECARD.CardID = CONFLICT.CardID;"
		cursor.execute(to_execute)
		data_get = cursor.fetchall()
		data_base.commit()
		return data_get

	@staticmethod
	def check_conflict(breeze_id):
		data_base = sql_queries.mysql_connection()
		cursor = data_base.cursor()
		to_execute = "SELECT UName from BREEZECARD where CardID = '{0}'".format(breeze_id)
		cursor.execute(to_execute)
		data_get = cursor.fetchone()
		data_base.commit()
		return data_get

	@staticmethod
	def remove_conflict(uname, card_id):
		data_base = sql_queries.mysql_connection()
		cursor = data_base.cursor()
		to_execute = "DELETE from CONFLICT where CardID = '{0}' and UName = '{1}'".format(card_id, uname)
		cursor.execute(to_execute)
		data_get = cursor.fetchone()
		data_base.commit()
		return data_get

	@staticmethod
	def update_card_owner(new_owner, card_id):
		data_base = sql_queries.mysql_connection()
		cursor = data_base.cursor()
		to_execute = "UPDATE BREEZECARD set UName = '{0}' where CardID = '{1}'".format(new_owner, card_id)
		cursor.execute(to_execute)
		data_get = cursor.fetchone()
		data_base.commit()
		return data_get

	@staticmethod
	def make_new_card(owner, value, card_id):
		data_base = sql_queries.mysql_connection()
		cursor = data_base.cursor()
		to_execute = "INSERT INTO BREEZECARD VALUES ('{0}', {1}, '{2}');".format(card_id, value, owner)
		cursor.execute(to_execute)
		data_get = cursor.fetchone()
		data_base.commit()
		return data_get

	@staticmethod
	def update_card_value(new_value, card_id):
		data_base = sql_queries.mysql_connection()
		cursor = data_base.cursor()
		to_execute = "UPDATE BREEZECARD set Value = '{0}' where CardID = '{1}'".format(new_value, card_id)
		cursor.execute(to_execute)
		data_get = cursor.fetchone()
		data_base.commit()
		return data_get

	@staticmethod
	def get_breezecards():
		data_base = sql_queries.mysql_connection()
		cursor = data_base.cursor()
		to_execute = "SELECT CardID, Value, UName FROM BREEZECARD;"
		cursor.execute(to_execute)
		data_get = cursor.fetchall()
		data_base.commit()
		return data_get

	@staticmethod
	def get_user_breezecards(owner):
		data_base = sql_queries.mysql_connection()
		cursor = data_base.cursor()
		to_execute = "SELECT CardID, Value, UName FROM BREEZECARD where UName = '{0}';".format(owner)
		cursor.execute(to_execute)
		data_get = cursor.fetchall()
		data_base.commit()
		return data_get

	@staticmethod
	def get_flow_report(start_date, end_date):
		data_base = sql_queries.mysql_connection()
		cursor = data_base.cursor()
		to_execute = " SELECT StationName, (select count(*) from TRIP where StartStopID = STATION.StopID and StartTime > '{0}' and StartTime < '{1}') as pass_in, (select count(*) from TRIP  where EndStopID = STATION.StopID and StartTime > '{0}' and StartTime < '{1}') as pass_out, (select pass_in) - (select pass_out) as flow, (select ifnull(sum(TripFare),0) from TRIP where StartStopID = STATION.StopID and StartTime > '{0}' and StartTime < '{1}') as revenue from STATION;";
		to_execute = to_execute.format(start_date,end_date)
		cursor.execute(to_execute)
		data_get = cursor.fetchall()
		data_base.commit()
		return data_get

	@staticmethod
	def trip_history(card_id):
		data_base = sql_queries.mysql_connection()
		cursor = data_base.cursor()
		to_execute = "SELECT StartTime, StartStopID, TripFare, EndStopID FROM TRIP where CardID = '{0}' and IsDoneFlag = true;".format(card_id)
		cursor.execute(to_execute)
		data_get = cursor.fetchall()
		data_base.commit()
		return data_get

	@staticmethod
	def start_trip(card_id, startstopid, trip_fare):
		data_base = sql_queries.mysql_connection()
		cursor = data_base.cursor()
		to_execute = "INSERT INTO TRIP values ('{0}', CURRENT_TIMESTAMP, '{1}', '{2}', 0, Null);".format(card_id, startstopid, trip_fare)
		cursor.execute(to_execute)
		data_get = cursor.fetchall()
		data_base.commit()
		return data_get

	@staticmethod
	def end_trip(card_id, endstopid):
		data_base = sql_queries.mysql_connection()
		cursor = data_base.cursor()
		to_execute = "UPDATE TRIP set IsDoneFlag = 1, EndStopID = '{0}' where CardID = '{1}' and IsDoneFlag = 0".format(endstopid, card_id)
		cursor.execute(to_execute)
		data_get = cursor.fetchall()
		data_base.commit()
		return data_get

	@staticmethod
	def get_current_trip(card_id):
		data_base = sql_queries.mysql_connection()
		cursor = data_base.cursor()
		to_execute = "SELECT StartStopID, TripFare from TRIP where IsDoneFlag = 0 and CardID='{0}'".format(card_id)
		cursor.execute(to_execute)
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

