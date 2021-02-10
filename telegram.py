import time
import schedule
import requests
import configparser
import yfinance as yf

# GET CREDENTIAL FROM CONFIG
config = configparser.ConfigParser()
config.read('config.ini')

# SET UP THE STOCK PROFILE CONSTANT
STOCKS = ['VOO', 'AMD', 'VNQI']


# GET MOVING AVERAGE ACTION BASED ON YAHOO FINANCE
def get_stock(stock_name):
    stock = yf.Ticker(stock_name)

    # get historical market data
    hist = stock.history(period="max")

    cur_value = hist['Close'][-1]

    rolling_200 = hist['Close'].rolling(200).mean()[-1]

    if cur_value > rolling_200 * 1.01:
        return f"You should buy in the stock {stock_name}"
    elif cur_value < rolling_200 * 0.99:
        return f"You should sell the stock {stock_name}"
    else:
        return f"You should hold for the stock {stock_name}"


def telegram_bot_sendtext(bot_message):
    bot_token = config['TELEGRAM']['ACCESS_TOKEN']
    bot_chatID = config['USER']['id']
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()


def report():
    # Sending the main message
    telegram_bot_sendtext(f'There are {len(STOCKS)} stocks in your curent profiles. {STOCKS}')
    telegram_bot_sendtext('Below are the suggested sell and buy action based on 200 days moving average')
    for stock_name in STOCKS:
        message = get_stock(stock_name)
        telegram_bot_sendtext(message)


schedule.every(7).days.at("13:00").do(report)

while True:
    schedule.run_pending()
    time.sleep(1)
