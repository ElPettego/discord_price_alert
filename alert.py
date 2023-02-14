import requests 
import config as cfg
import db
import discord_dm
import logging
import colorama as c


class Alert:
    def __init__(self, current_price, target_price, current_date, assett_tag, chat_id):
        self.chat_id = int(chat_id)
        self.assett_tag = assett_tag
        self.open_date = current_date
        self.open_price = float(current_price)
        self.target_price = float(target_price)
        self.db = db.DB()
        self.dm = discord_dm.DiscordDM()
        FORMAT = f'{c.Back.CYAN}%(asctime)s{c.Back.RESET} - {c.Back.YELLOW}ALERT {self.chat_id}{c.Back.RESET} - {c.Back.MAGENTA}%(levelname)s{c.Back.RESET} - %(message)s'
        logging.basicConfig(level=logging.INFO, format=FORMAT)

    def send_message(self) -> None:
        message = f"""🚨 ALERT 🚨
🎯 TARGET REACHED ✅
        
🪙 ASSETT => {self.assett_tag}
💸 TARGET PRICE => {self.target_price}
💰 CURRENT PRICE => {self.current_price}
⏲️ ALERT OPEN DATE => {self.open_date}"""
        # url = f"https://api.telegram.org/bot{cfg.BOT_TOKEN}/sendMessage?chat_id={self.chat_id}&text={message}"
        # requests.get(url)
        self.dm.send(id=self.chat_id, mex=message)

    def check_alert(self) -> None:
        try:
            with open(f'./prices/{self.assett_tag}.txt', 'r') as f:
                self.current_price = float(f.read())
        except ValueError:
            return
        if self.target_price <= self.open_price and self.current_price <= self.target_price:
            logging.info(f'TARGET REACHED. USER => {self.chat_id}')
            self.send_message()
            self.db.delete_alert(user_id=self.chat_id, open_date=self.open_date)
            return
        if self.target_price >= self.open_price and self.current_price >= self.target_price:
            logging.info(f'TARGET REACHED. USER => {self.chat_id}')
            self.send_message()
            self.db.delete_alert(user_id=self.chat_id, open_date=self.open_date)
            return