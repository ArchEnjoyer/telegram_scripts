import telebot
import logging

# Токен вашего бота
TOKEN = ''
# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

## Обработчик команды /start
#@bot.message_handler(commands=['start'])
#def handle_start(message):
#    logger.info(f"Пользователь {message.from_user.full_name} запустил команду /start")
#    bot.reply_to(message, "Привет! Я бот, который читает все сообщения.")

# Обработчик всех текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    text = message.text
    logger.info(f"Пользователь {user_name} (ID: {user_id}) написал: {text}")

    ## Ответить пользователю
    #bot.reply_to(message, f"Вы написали: {text}")

# Запуск бота
if __name__ == '__main__':
    logger.info("Бот запущен и ожидает сообщений...")
    bot.polling(none_stop=True)
