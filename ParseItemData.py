import functions
import requests
import json


def GetAssetImage(ID):
    s = requests.session()
    ret = s.post("https://thumbnails.roblox.com/v1/batch", json=[{"requestId": str(ID)+"::Asset:420x420:png:regular", "type": "Asset", "targetId": str(ID), "token": "", "format": "png", "size": "420x420"}])
    p = ret.text.split("imageUrl")[1].split("}")[0]
    url = p[3:-1]
    return url

def GetAssetInfo(ID):
    s = requests.session()
    GetAssetInfo.ret = ""
    attempts = 0
    while attempts < 10:
        try:
            url = f"https://catalog.roblox.com/v1/catalog/items/{ID}/details?itemType=Asset"

            proxy_protocol = functions.GetCurrentProxy()  # Anti Rate-Limit
            proxy = proxy_protocol[0]
            protocol = proxy_protocol[1]

            GetAssetInfo.ret = s.get(url, proxies={f'{protocol}':"http://"+proxy})
            print(GetAssetInfo.ret)
            if GetAssetInfo.ret.text == '{"errors":[{"code":0,"message":"Too many requests"}]}':  # если RateLimit
                proxy = functions.GetCurrentProxy()  # Anti Rate-Limit

            if GetAssetInfo.ret:
                break
        except Exception as e:
            print("Что-то пошло не так, повторяем попытку. Ошибка:"+str(e))
            attempts += 1

    json_ = json.loads(str(GetAssetInfo.ret.text))
    if json_.get("name", None) != None:
        name = str(json_["name"])
        itemType = str(json_["itemType"])
        return [name, itemType]
    return "ERROR: invalid data parsed"