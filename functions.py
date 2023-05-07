import variables
import requests
import re


def escape_markdown(text):
    return re.sub(r'([_*[\]()~`>#+\-=|{}.!])', r'\\\1', text)

def CheckCookie(cookie):
    user_id = ""
    try:
        proxy_protocol = GetCurrentProxy()  # Anti Rate-Limit
        proxy = proxy_protocol[0]
        protocol = proxy_protocol[1]
        user_id = requests.get("https://users.roblox.com/v1/users/authenticated", cookies={".ROBLOSECURITY": cookie},
                        proxies={f'{protocol}': "http://" + proxy}).json()["id"]
    except Exception as e:
        ###print(e)
        return ""
    return user_id

def GetCurrentProxy():
    if variables.CURRENT_PROXY_USES < variables.MAX_PROXY_LIMIT:  # сли прокси не "израсходован", то добавляем ему "расход"
        variables.CURRENT_PROXY_USES += 1
    else:  # сли прокси "израсходован", то меняем на новый
        variables.CURRENT_PROXY = next(variables.PROXY_POOL)
        variables.CURRENT_PROXY_USES = 1
    return variables.CURRENT_PROXY

def AdaptiveMarkdown(text):
    return text.replace(":", "\:").replace(".", "\.").replace("(", "\(").replace(")", "\)").replace("-", "\-").replace("!", "\!")

def FindInListFromIncludeValue(search_value, my_list):
    return list(filter(lambda x: x[0] == search_value, my_list))