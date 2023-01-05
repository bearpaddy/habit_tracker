import requests
import datetime as dt
import os

class User:

    def create_pixela_account():
    
        pixela_endpoint = "https://pixe.la/v1/users"
        user_params = {
            "token": "fjdhakcdv1likj",
            "username": "jkim",
            "agreeTermsOfService": "yes",
            "notMinor": "yes"
        }
        response = requests.post(pixela_endpoint, json=user_params)
        return response.status_code

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