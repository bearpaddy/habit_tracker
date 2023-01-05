import requests
import datetime as dt
import os

class User:

    def __init__(self, username:str, token:str) -> None:
        self.default_url = os.environ.get("PIXELA_ENDPOINT")
        self.username = username
        self.token = token
        self.request_params = self.create_request_arguments()
    
    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        if isinstance(value, str):
            self._username = value
        else:
            raise ValueError("Username must be string")
    
    @property
    def token(self):
        return self._token
    
    @token.setter
    def token(self, value):
        if isinstance(value, str) and 10 < len(value) < 30:
            self._token = value
        else:
            raise ValueError("Token must be string and between 10-20 characters")


    def create_request_arguments(self):
        user_params = {
            "token": self.token,
            "username": self.username,
            "agreeTermsOfService": "yes",
            "notMinor": "yes"
        }
        return user_params
    

    def create_new_user(self) -> bool:
        response = requests.post(self.default_url, json=self.request_params)
        is_successful = True if response.status_code == 404 else False
        return is_successful

class Habit:

    def __init__(self, id:str, name:str, unit:str, color:str, type:str = 'int') -> None:
        self.id = id
        self.name = name
        self.unit = unit
        self.type = type #TODO : type is default to int, boolean attribute that checks if type is int or float
        self.color = color
        self.default_url = os.environ.get("PIXELA_ENDPOINT")
        self.today = dt.datetime.now().strftime("%Y%m%d")

        self.header = self.create_http_request_header()

    def create_graph_endpoint_url(self) -> None:
        self.graph_url = self.default_url + f"/{self.name}/graphs/{self.name}"

    
    def create_graph_config(self) -> dict:
        json = {
            "id": self.id,
            "name": self.name,
            "unit": self.unit,
            "type": self.type,
            "color": self.color
        }
        return json

    def create_http_request_header(self)-> dict:
        header = {
            "X-USER-TOKEN": os.environ.get("TOKEN")
        }
        return header
        

    def create_new_graph(self) -> bool:
        graph_url = self.create_graph_endpoint_url()
        graph_params = self.create_graph_config()
        response = requests.post(url=graph_url, json= graph_params, headers=self.header)
        response.status_code
        return response.status_code == 404 


    def record_new_entry(self, quantity:float, is_today:bool = True) -> bool:

        def _create_update_json(quantity, is_today) -> dict:
            
            date = self.today if is_today else None
            quantity = str(quantity) if self.type == "float" else str(int(float))

            entry = {
                "date": date,
                "quantity": quantity
            }
            return entry

        json = _create_update_json()
        response = requests.post(url=self.graph_url, json=json, headers=self.header)