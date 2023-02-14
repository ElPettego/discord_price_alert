import db 
import time as t
import alert


ALERT_DB = db.DB()

def main():
    while True:
        # print('CHECKING ALERTS...')
        alerts = ALERT_DB.get_alerts()
        # print(type(alerts))
        for al in alerts:

            curr_alert = alert.Alert(
                current_price=al['open_price'],
                target_price=al['target_price'],
                current_date=al['open_date'],
                assett_tag=al['assett_tag'],
                chat_id=al['user_id'])
            curr_alert.check_alert()
        t.sleep(30)

if __name__ == '__main__':
    main()