import requests
import config as cfg
import logging
import colorama as c

class DiscordDM:
    def __init__(self) -> None:
        FORMAT = f'{c.Back.CYAN}%(asctime)s{c.Back.RESET} - {c.Back.YELLOW}DISCORD DM{c.Back.RESET} - {c.Back.MAGENTA}%(levelname)s{c.Back.RESET} - %(message)s'
        logging.basicConfig(level=logging.INFO, format=FORMAT)

    def send(self, id : int, mex : str):

        url = "https://discord.com/api/v6/users/@me/channels"

        payload = {
            "content": f"{mex}",
            "recipient_id": id
        }
        headers = {
            "cookie": "__dcfduid=298c8c58abe811eda131a6b157386236; __sdcfduid=298c8c58abe811eda131a6b157386236c925dd2fb04aa830bf6c44dabc540e4ec8598bf28564ea8a54f1a3c989e0b276; __cfruid=69ee92b96f39f7eddeeee5b9029ce901c4ab4154-1676324913",
            "Content-Type": "application/json",
            "Authorization": f"Bot {cfg.TOKEN}"
        }

        response = requests.request("POST", url, json=payload, headers=headers)
    
        ch_id = response.json()['id']

        url = f"https://discord.com/api/v6/channels/{ch_id}/messages"

        payload = {"content": f"{mex}"}
        headers = {
            "cookie": "__dcfduid=298c8c58abe811eda131a6b157386236; __sdcfduid=298c8c58abe811eda131a6b157386236c925dd2fb04aa830bf6c44dabc540e4ec8598bf28564ea8a54f1a3c989e0b276; __cfruid=69ee92b96f39f7eddeeee5b9029ce901c4ab4154-1676324913",
            "Authorization": f"Bot {cfg.TOKEN}",
            "Content-Type": "application/json"
        }

        response = requests.request("POST", url, json=payload, headers=headers)

    