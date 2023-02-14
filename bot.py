import datetime as dt
import time as t
import config as cfg
import db 
import auth
import discord
from discord.ext import commands
import logging
from discord import app_commands
import colorama as c

WELCOME = """🎉 WELCOME TO TRADING PRICE ALERT BOT!!! 🤖

"""

USAGE = """🔧 USAGE: 

ℹ️ INFO: <> is used for passing an argument to the command

/set_alert <asset> <price> => CREATE A NEW ALERT. <asset> is one of the assets in the belove list. <price> is the target price of the alarm. EXAMPLE => /set_alert BTCUSDT 100000

/get_alert => SHOWS ACTIVE ALERTS

/delete_alert <index> => DELETE ONE OF THE ACTIVE ALERTS. type /get_alert to show active alerts and then /delete_alert <index> to delete the alert. EXAMPLE => /delete_alert 1

/get_price <asset> => GETS THE CURRENT PRICE OF THE ASSET. EXAMPLE => /get_price BTCUSDT

🪙 AVAILABLE ASSETS 🪣: 
- BTCUSDT
- ETHUSDT
- DOGEUSDT
- SOLUSDT
- BNBUSDT
- EURUSD
- GBPUSD
- EURGBP

ℹ️ FX PRICES ARE AVAILABLE WITH 4 DECIMALS => 1.2345

🌕 SEE YOU ON THE MOON 🚀"""

NOT_AUTH = """⛔ U ARE NOT AUTHENTICATED :(. U MUST ASK THE PASSWORD TO @uomo_succo ❌"""

ASSETS = """🪙 AVAILABLE ASSETS 🪣: 
- BTCUSDT
- ETHUSDT
- DOGEUSDT
- SOLUSDT
- BNBUSDT
- EURUSD
- GBPUSD
- EURGBP"""

ALERT_DB = db.DB()


def main() -> None:
    FORMAT = f'{c.Back.CYAN}%(asctime)s{c.Back.RESET} - {c.Back.YELLOW}BOT{c.Back.RESET} - {c.Back.MAGENTA}%(levelname)s{c.Back.RESET} - %(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT)
    intents = discord.Intents.all()
    intents.members = True
    intents.message_content = True
    client = commands.Bot(command_prefix='/', intents=intents)
    assets  = [app_commands.Choice(name=el, value=el) for el in cfg.ASSETS]

    @client.event
    async def on_ready():        
        logging.info('BOT READY')
        try:
            synced = await client.tree.sync()
            logging.info(f'SYNCED {len(synced)} commands!')
        except Exception as e:
            logging.error(e)

    
    # print(assets)
 
    @client.tree.command(name='set_alert', description='SET AN ALERT AT THE TARGET PRICE FOR THE CHOSEN ASSET 🎯')
    @app_commands.choices(asset=assets)
    @app_commands.describe(price = 'Price of the alert. For fx pairs available only 4 decimals.')
    async def set_alert(interaction : discord.Interaction, asset : app_commands.Choice[str], price : str):
        user_id = interaction.user.id
        user = interaction.user
        # print(asset)
        try:
            price = abs(float(price))
        except (ValueError, IndexError):
            await interaction.response.send_message(f'⚠️ PRICE NOT VALID ❌')
            return
        if asset.value not in cfg.ASSETS:
            await interaction.response.send_message("⚠️ ASSET NOT AVAILABLE ❌ WRITE TO @uomo_succo IF U WANNA ADD IT :)")
            return
        with open(f'./prices/{asset.value}.txt', 'r') as f:
            current_price = f.read()
        alert_o = dict(
            open_price=float(current_price),
            target_price=price,
            open_date=dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            assett_tag=asset.value,
            user_id=user_id
        )
        ALERT_DB.add_alert(alert=alert_o)
        logging.info(f'ALERT SET SUCCESFULLY! ASSETT => {asset.value} - PRICE => {price} - ID => {user_id} - USER => {user}')

        await interaction.response.send_message(f"🎯 ALERT SET SUCCESSFULLY! ✅")

    @client.tree.command(name='get_alerts', description='SEE CURRENT ACTIVE ALERTS ✅')
    async def get_alerts(interaction : discord.Interaction):
        user_id = interaction.user.id
        user = interaction.user
        
        alerts = ALERT_DB.get_alerts(user_id=user_id)
        logging.info(f'ALERTS REQUESTED FROM USER => {user}')
        mex = '🎯 CURRENT ACTIVE ALERTS 🪙\n\n'
        for ind, alert in enumerate(alerts):
            mex += f'🚨 ALERT {ind}\n🪙 ASSETT => {alert["assett_tag"]} \n🎯 TARGET => {alert["target_price"]}\n⏲️ DATE => {alert["open_date"]}\n\n'
        if mex == '':
            await interaction.response.send_message('🛌 NO ACTIVE ALERTS AT THE MOMENT :(')
            return
        await interaction.response.send_message(mex)

    @client.tree.command(name='get_price', description='SEE THE CURRENT PRICE OF AVAILABLE ASSETS 🚀')
    @app_commands.choices(asset=assets)
    async def get_price(interaction : discord.Interaction, asset : app_commands.Choice[str]):        
        with open(f'./prices/{asset.value}.txt', 'r') as f:
            current_price = f.read()
        await interaction.response.send_message(f'🪙 ASSET {asset.value} 💵 PRICE => {current_price}')

    @client.tree.command(name='delete_alert', description='DELETES THE SELECTED ALERT ❌') 
    async def delete_alert(interaction : discord.Interaction):
        user_id = interaction.user.id
        user = interaction.user
        
        class delView(discord.ui.View):
            alerts = ALERT_DB.get_alerts(user_id=user_id)
            opts = [discord.SelectOption(label=ind, description=f"{al['assett_tag']} | {al['target_price']} | {al['open_date']}") for ind, al in enumerate(alerts)]
            @discord.ui.select(
                placeholder='WHICH ALERT DO YOU WANT TO DELETE? ❌',
                min_values=0,
                max_values=1,
                options=opts
            )
            async def del_callback(self, interaction, select):
                # print(select.values[0])
                date = str(select.options[int(select.values[0])]).split('| ')[2]
                # print(date)
                # print(select.options[int(select.values[0])])
                ALERT_DB.delete_alert(user_id=user_id, open_date=date)
                await interaction.response.send_message('🎯 ALERT DELETED SUCCESFULLY ❌')
        
        await interaction.response.send_message('WHICH ALERT DO YOU WANT TO DELETE? ❌', view=delView())
        

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        # logging.info(f'{str(message.author)} - {str(client.user)}')
        await message.channel.send(USAGE)

    client.run(cfg.TOKEN, log_handler=None)

    
if __name__ == '__main__':
    main()