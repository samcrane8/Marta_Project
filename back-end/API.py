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
			isAdmin = sql_queries.is_admin(request.authorization.username)

			dict_local = {'code': 200, 'isAdmin': isAdmin}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string 
		else:
			#not a good cookie and no login.
			dict_local = {'code': 31, 'message': "login failed"}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string	

	@staticmethod
	def register_admin():
		if API.is_valid_user(request.authorization):
			#then we've already logged on.

			parsed_json = request.get_json()

			username = parsed_json["username"]
			password = parsed_json["password"]
			isAdmin = True

			if not sql_queries.username_available(username):
				#then we tell them this won't work
				dict_local = {'code': 31, 'message': "Username is taken."}
				return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
				return return_string 

			sql_queries.register_user(username, password, isAdmin)

			dict_local = {'code': 200}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string 
		else:
			#not a good cookie and no login.
			dict_local = {'code': 31, 'message': "login failed"}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string

	@staticmethod
	def register_passenger():
		#registers passenger
		#creates new breezecard if not using an old one.

		parsed_json = request.get_json()

		username = parsed_json["username"]
		password = parsed_json["password"]
		email = parsed_json["email"]
		breeze_id = parsed_json["breezeID"]

		make_conflict = False

		if breeze_id == "NEW_CARD":
			card_id = str(uuid.uuid4())
		else:
			#not a new card.
			card_id = parsed_json["breezeID"]
			#could possibly cause conflict.
			if sql_queries.check_conflict(card_id) is not None:
				#then it's a conflict
				make_conflict = True

		isAdmin = False

		if sql_queries.is_username_taken(username):
			dict_local = {'code': 50}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string

		if sql_queries.is_email_taken(email):
			dict_local = {'code': 51}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string

		sql_queries.register_user(username, password, isAdmin)
		sql_queries.register_passenger(username, email)

		if make_conflict:
			sql_queries.add_conflict(username, card_id)

		dict_local = {'code': 200}
		return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
		return return_string 

	@staticmethod
	def get_conflicts():
		conflicts = sql_queries.get_conflicts()

		array_local = []

		for conflict in conflicts:
			new_owner, card_id, date_suspended, value, old_owner = conflict
			c={}
			c["new_owner"] = new_owner
			c["card_id"] =card_id
			c["date_suspended"] = str(date_suspended)
			c["value"] = float(value)
			c["old_owner"] = old_owner
			array_local += [c]

		return_string = json.dumps(array_local, sort_keys=True, indent=4, separators=(',', ': '))
		return return_string 

	@staticmethod
	def resolve_conflict():
		parsed_json = request.get_json()

		card_id = parsed_json["card_id"]
		uname = parsed_json["uname"]
		resolve_to_new = parsed_json["resolve_to_new"]

		if not resolve_to_new:
			#then it's easy!
			#just delete the conflict.
			sql_queries.remove_conflict(uname, card_id)
		else:
			#yeah... harder.
			sql_queries.update_card_owner(uname, card_id)
			sql_queries.remove_conflict(uname, card_id)

		dict_local = {'code': 200}
		return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
		return return_string

	@staticmethod
	def get_breezecards():
		breezecards = sql_queries.get_breezecards()

		array_local = []

		for breezecard in breezecards:
			card_id, value, uname = breezecard
			b={}
			b["card_id"] =card_id
			b["value"] = float(value)
			b["owner"] = uname
			array_local += [b]

		return_string = json.dumps(array_local, sort_keys=True, indent=4, separators=(',', ': '))
		return return_string 

	@staticmethod
	def get_flow_report():

		parsed_json = request.get_json()

		start_date = parsed_json["start_date"]
		end_date = parsed_json["end_date"]

		flows = sql_queries.get_flow_report(start_date, end_date)

		array_local = []

		for flow in flows:
			station_name, pass_in, pass_out, flow, revenue = flow
			f={}
			f["station_name"] =station_name
			f["pass_in"] = pass_in
			f["pass_out"] = pass_out
			f["flow"] = flow
			f["revenue"] = float(revenue)
			array_local += [f]

		return_string = json.dumps(array_local, sort_keys=True, indent=4, separators=(',', ': '))
		return return_string 

	@staticmethod
	def update_card():
		parsed_json = request.get_json()

		card_id = parsed_json["card_id"]
		value = parsed_json["value"]
		owner = parsed_json["owner"]

		sql_queries.update_card_value(value, card_id)
		sql_queries.update_card_owner(owner, card_id)

		dict_local = {'code': 200}
		return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
		return return_string

	@staticmethod
	def is_valid_user(auth):
		if auth is None or auth.username is None or auth.password is None:
			return False
		data_get = sql_queries.get_user(auth.username, auth.password)
		if data_get is not None:
			return True
		else:
			return False

	@staticmethod
	def get_stations():
		stations = sql_queries.get_stations()
		array_local = []

		for station in stations:
			s={}
			StopID, EntryFare, IsOpenFlagI, StationName, IsBusFlag, roads = station
			s["station_name"] = StationName
			s["stop_id"] = StopID
			s["fare"] = float(EntryFare)
			if roads is None:
				roads = ''
			s["nearest_intersection"] = roads
			if IsOpenFlagI == 1:
				IsOpenFlagI = "OPEN"
			else:
				IsOpenFlagI = "CLOSED"
			s["isopen"] = IsOpenFlagI
			if IsBusFlag == 1:
				IsBusFlag = True
			else:
				IsBusFlag = False
			s["isBus"] = IsBusFlag

			array_local += [s]

		return_string = json.dumps(array_local, sort_keys=True, indent=4, separators=(',', ': '))
		return return_string

	@staticmethod
	def add_station():
		parsed_json = request.get_json()

		stopid = parsed_json["stopid"]
		isopen = parsed_json["isopen"]
		fare = parsed_json["fare"]
		nearest_intersection = parsed_json["nearest_intersection"]

		sql_queries.add_station(stopid, fare, isopen, parsed_json["station_name"], parsed_json["isbus"])
		sql_queries.add_nearest_intersection(stopid, nearest_intersection)
		dict_local = {'code': 200}
		return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
		return return_string

	@staticmethod
	def update_station():
		parsed_json = request.get_json()

		stopid = parsed_json["stop_id"]
		isopen = parsed_json["isopen"]

		if isopen:
			isopen = 1
		else:
			isopen = 0

		updated_fare = parsed_json["updated_fare"]

		sql_queries.update_station(stopid, updated_fare, isopen)
		dict_local = {'code': 200}
		return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
		return return_string


app.add_url_rule('/login', 'login', API.login, methods=['GET'])
app.add_url_rule('/get_conflicts', 'get_conflicts', API.get_conflicts, methods=['GET'])
app.add_url_rule('/get_breezecards', 'get_breezecards', API.get_breezecards, methods=['GET'])
app.add_url_rule('/get_flow_report', 'get_flow_report', API.get_flow_report, methods=['POST'])
app.add_url_rule('/resolve_conflict', 'resolve_conflict', API.resolve_conflict, methods=['POST'])
app.add_url_rule('/update_card', 'update_card', API.update_card, methods=['POST'])
# app.add_url_rule('/logoff', 'logoff', User.logoff, methods=['GET'])
app.add_url_rule('/get_stations', 'get_stations', API.get_stations, methods=['GET'])
app.add_url_rule('/add_station', 'add_station', API.add_station, methods=['POST'])
app.add_url_rule('/update_station', 'update_station', API.update_station, methods=['POST'])
app.add_url_rule('/register_admin', 'register_admin', API.register_admin, methods=['POST'])
app.add_url_rule('/register_passenger', 'register_passenger', API.register_passenger, methods=['POST'])
