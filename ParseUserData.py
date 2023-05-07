import requests
import json


s = requests.session()
def GetUsername(id):
    ret = s.get(f"https://users.roblox.com/v1/users/{id}").text
    json_ = json.loads(str(ret))
    Name = json_["name"]
    DisplayName = json_["displayName"]
    return {"name": Name, "displayName": DisplayName}