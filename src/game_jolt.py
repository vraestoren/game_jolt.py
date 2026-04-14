from hashlib import md5
from requests import Session
from urllib.parse import urlencode

class GameJolt:
	def __init__(self, game_id: int, username: str, user_token: str, private_key: str) -> None:
		self.api = "https://api.gamejolt.com/api/game/v1_2"
		self.session = Session()
		self.session.headers = {
			"User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G9880 Build/RP1A.2007201.012; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36"
		}
		self.game_id = game_id
		self.username = username
		self.user_token = user_token
		self.private_key = private_key

	def _get(
			self, endpoint: str, params: dict = None, include_user: bool = True) -> dict:
		payload = {
			"game_id": self.game_id
		}
		if include_user and not (params and params.get("guest")):
			payload.update({
				"username": self.username,
				"user_token": self.user_token
			})
		
		if params:
			payload.update({
				key: value for key, value in params.items() if value is not None
			})
		
		query = urlencode(payload)
		path = f"{endpoint}?{query}" if query else endpoint
		signature = md5(f"{self.api}{path}{self.private_key}".encode()).hexdigest()
		return self.session.get(
			f"{self.api}{path}&signature={signature}").json()

	def get_user(self) -> dict:
		params = {
			"username": self.username
		}
		return self._get("/users/", params)

	def authenticate_user(self) -> dict:
		return self._get("/users/auth/")

	def open_session(self) -> dict:
		return self._get("/sessions/open/")

	def ping_session(self, status: str = "active") -> dict:
		params = {
			"status": status
		}
		return self._get("/sessions/ping/", params)

	def check_session(self) -> dict:
		return self._get("/sessions/check/")

	def close_session(self) -> dict:
		return self._get("/sessions/close/")

	def get_scores(
			self,
			limit: int = None,
			table_id: int = None,
			guest: str = None,
			better_than: int = None,
			worse_than: int = None) -> dict:
		params = {
			"limit": limit,
			"table_id": table_id,
			"guest": guest,
			"better_than": better_than,
			"worse_than": worse_than,
		}
		return self._get("/scores/", params)

	def get_score_tables(self) -> dict:
		return self._get("/scores/tables/")

	def add_scores(
			self,
			score: str,
			sort: int,
			table_id: int = None,
			extra_data: str = None,
			guest: str = None) -> dict:
		params = {
			"score": score,
			"sort": sort,
			"table_id": table_id,
			"extra_data": extra_data,
			"guest": guest
		}
		return self._get("/scores/add/", params)

	def get_score_rank(self, sort: int, table_id: int = None) -> dict:
		params = {
			"sort": sort,
			"table_id": table_id
		}
		return self._get("/scores/get-rank/", params)

	def get_trophy(self, trophy_id: int = None, achieved: bool = False) -> dict:
		params = {
			"trophy_id": trophy_id,
			"achieved": str(achieved).lower()
		}
		return self._get("/trophies/", params)

	def add_achieved(self, trophy_id: int) -> dict:
		params = {
			"trophy_id": trophy_id
		}
		return self._get("/trophies/add-achieved/", params)

	def remove_achieved(self, trophy_id: int) -> dict:
		params = {
			"trophy_id": trophy_id
		}
		return self._get("/trophies/remove-achieved/", params)

	def set_data(
			self, key: str, data: str, user_info_only: bool = False) -> dict:
		params = {
			"key": key,
			"data": data
		}
		return self._get("/data-store/set/", params, user_info_only)

	def update_data(self, key: str, operation: str, value: int, user_info_only: bool = False) -> dict:
		params = {
			"key": key,
			"operation": operation,
			"value": value
		}
		return self._get("/data-store/update/", params, user_info_only)

	def remove_data(self, key: str, user_info_only: bool = False) -> dict:
		params = {
			"key": key
		}
		return self._get("/data-store/remove/", params, user_info_only)

	def get_data(self, key: str, user_info_only: bool = False) -> dict:
		params = {
			"key": key
		}
		return self._get("/data-store/", params, user_info_only)

	def get_keys(self, user_info_only: bool = False) -> dict:
		return self._get("/data-store/get-keys/", {}, user_info_only)

	def get_friends_list(self) -> dict:
		return self._get("/friends/")

	def get_server_time(self) -> dict:
		return self._get("/time/")
