from hashlib import md5
from requests import Session

class GameJolt:
	def __init__(
			self,
			game_id: int,
			username: str,
			user_token: str,
			private_key: str) -> None:
		self.api = "https://api.gamejolt.com/api/game/v1_2"
		self.session = Session()
		self.session.headers = {
			"User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G9880 Build/RP1A.2007201.012; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36"
		}
		self.game_id = game_id
		self.username = username
		self.user_token = user_token
		self.private_key = private_key

	def generate_signature(self, path: str) -> str:
		return md5(
			f"{self.api}{path}{self.private_key}".encode()).hexdigest()
	
	def get_user(self) -> dict:
		path = f"/users/?game_id={self.game_id}&username={self.username}"
		return self.session.get(
			f"{self.api}{path}&signature={self.generate_signature(path)}").json()
			
	def authenticate_user(self) -> dict:
		path = f"/users/auth/?game_id={self.game_id}&username={self.username}&user_token={self.user_token}"
		return self.session.get(
			f"{self.api}{path}&signature={self.generate_signature(path)}").json()
	
	def open_session(self) -> dict:
		path = f"/sessions/open/?game_id={self.game_id}&username={self.username}&user_token={self.user_token}"
		return self.session.get(
			f"{self.api}{path}&signature={self.generate_signature(path)}").json()

	def ping_session(self, status: str = "active") -> dict:
		path = f"/sessions/ping/?game_id={self.game_id}&username={self.username}&user_token={self.user_token}&status={status}"
		return self.session.get(
			f"{self.api}{path}&signature={self.generate_signature(path)}").json()
	
	def check_session(self) -> dict:
		path = f"/sessions/check/?game_id={self.game_id}&username={self.username}&user_token={self.user_token}"
		return self.session.get(
			f"{self.api}{path}&signature={self.generate_signature(path)}").json()
	
	def close_session(self) -> dict:
		path = f"/sessions/close/?game_id={self.game_id}&username={self.username}&user_token={self.user_token}"
		return self.session.get(
			f"{self.api}{path}&signature={self.generate_signature(path)}").json()
	
	def get_scores(
			self, 
			limit: int = None,
			table_id: int = None,
			guest: str = None,
			better_than: int = None,
			worse_than: int = None) -> dict:
		path = f"/scores/?game_id={self.game_id}&username={self.username}&user_token={self.user_token}"
		if limit:
			path += f"&limit={limit}"
		if table_id:
			path += f"&table_id={table_id}"
		if guest:
			path = f"/scores/?game_id={self.game_id}&guest={guest}"
		if better_than:
			path += f"&better_than={better_than}"
		if worse_than:
			path += f"&worse_than={worse_than}"
		return self.session.get(
			f"{self.api}{path}&signature={self.generate_signature(path)}").json()
	
	def get_score_tables(self) -> dict:
		path = f"/scores/tables/?game_id={self.game_id}"
		return self.session.get(
			f"{self.api}{path}&signature={self.generate_signature(path)}").json()
	
	def add_scores(
			self,
			score: str,
			sort: int,
			table_id: int = None,
			extra_data: str = None,
			guest: str = None) -> dict:
		path = f"/scores/add/?game_id={self.game_id}&username={self.username}&user_token={self.user_token}&score={score}&sort={sort}"
		if table_id:
			path += f"&table_id={table_id}"
		elif extra_data:
			path += f"&extra_data={extra_data}"
		elif guest:
			path = f"/scores/add/?game_id={self.game_id}&score={score}&sort={sort}&guest={guest}"
		return self.session.get(
			f"{self.api}{path}&signature={self.generate_signature(path)}").json()

	def get_score_rank(
			self,
			sort: int,
			table_id: int = None) -> dict:
		path = f"/scores/get-rank/?game_id={self.game_id}&sort={sort}"
		if table_id:
			path += f"&table_id={table_id}"
		return self.session.get(
			f"{self.api}{path}&signature={self.generate_signature(path)}").json()
	
	def get_trophy(
			self,
			trophy_id: int = None,
			achieved: bool = False) -> dict:
		path = f"/trophies/?game_id={self.game_id}&username={self.username}&user_token={self.user_token}&achieved={achieved}"
		if trophy_id:
			path += f"&trophy_id={trophy_id}"
		return self.session.get(
			f"{self.api}{path}&signature={self.generate_signature(path)}").json()
	
	def add_achieved(self, trophy_id: int) -> dict:
		path = f"/trophies/add-achieved/?game_id={game_id}&username={self.username}&user_token={self.user_token}&trophy_id={trophy_id}"
		return self.session.get(
			f"{self.api}{path}&signature={self.generate_signature(path)}").json()
	
	def remove_achieved(self, trophy_id: int) -> dict:
		path = f"/trophies/remove-achieved/?game_id={game_id}&username={self.username}&user_token={self.user_token}&trophy_id={trophy_id}"
		return self.session.get(
			f"{self.api}{path}&signature={self.generate_signature(path)}").json()
	
	def set_data(
			self,
			key: str,
			data: str,
			user_info_only: bool = False) -> dict:
		path = f"/data-store/set/?game_id={self.game_id}&key={key}&data={data}"
		if user_info_only:
			path += f"&username={self.username}&user_token={self.user_token}"
		return self.session.get(
			f"{self.api}{path}&signature={self.generate_signature(path)}").json()
	
	def update_data(
			self,
			key: str,
			operation: str,
			value: int,
			user_info_only: bool = False) -> dict:
		path = f"/data-store/update/?game_id={self.game_id}&key={key}&operation={operation}&value={value}"
		if user_info_only:
			path += f"&username={self.username}&user_token={self.user_token}"
		return self.session.get(
			f"{self.api}{path}&signature={self.generate_signature(path)}").json()
	
	def remove_data(self, key: str) -> dict:
		path = f"/data-store/remove/?game_id={self.game_id}&key={key}"
		return self.session.get(
			f"{self.api}{path}&signature={self.generate_signature(path)}").json()
		
	def get_data(
			self,
			key: str,
			user_info_only: bool = False) -> dict:
		path = f"/data-store/?game_id={self.game_id}&key={key}"
		if user_info_only:
			path += f"&username={self.username}&user_token={self.user_token}"
		return self.session.get(
			f"{self.api}{path}&signature={self.generate_signature(path)}").json()
	
	def get_keys(self) -> dict:
		path = f"/data-store/get-keys/?game_id={self.game_id}"
		return self.session.get(
			f"{self.api}{path}&signature={self.generate_signature(path)}").json()
	
	def get_friends_list(self) -> dict:
		path = f"/friends/?game_id={self.game_id}&username={self.username}&user_token={self.user_token}"
		return self.session.get(
			f"{self.api}{path}&signature={self.generate_signature(path)}").json()
	
	def get_server_time(self) -> dict:
		path = f"/time/?game_id={self.game_id}"
		return self.session.get(
			f"{self.api}{path}&signature={self.generate_signature(path)}").json()
