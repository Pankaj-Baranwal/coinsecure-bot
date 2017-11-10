from API import BOT_TOKEN # contains BOT_TOKEN
import telegram as tgram # pip install telegram-send

CHAT_ID = -195455600 # chat id for the BTC telegram group

bot = tgram.Bot(token=BOT_TOKEN)

def sendMessage(message):
	bot.send_message(chat_id = CHAT_ID, text = message)

# sendMessage("sup bitches testing 123")