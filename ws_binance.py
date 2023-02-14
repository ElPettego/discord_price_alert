import websocket
import sys
import json
import logging
import colorama as c


TAG = sys.argv[1] #'BTCUSDT'

def on_open(ws):
    pass

def on_error(ws, error : str):
    print(error)

def on_message(ws, message : str):
    mex_j = json.loads(message)
    price = round(float(mex_j['k']['c']), 7)
    with open(f'./prices/{TAG}.txt', 'w') as f:
        f.write(str(price))

def on_close(ws):
    pass

def main():
    url = str(sys.argv[2])
    FORMAT = f'{c.Back.CYAN}%(asctime)s{c.Back.RESET} - {c.Back.YELLOW}WSS {TAG}{c.Back.RESET} - {c.Back.MAGENTA}%(levelname)s{c.Back.RESET} - %(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT)
    
    ws = websocket.WebSocketApp(
        url=url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )        

    ws.run_forever()

if __name__ == '__main__':
    main()
