import telebot
import logging
import threading
import sys
import re
from telebot.types import Message

# Токен вашего бота
TOKEN = ''

# Настройка логов
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Хранилище последних чатов для быстрого ответа
last_chat_id = None
last_user_id = None
last_message_id = None

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global last_chat_id, last_user_id, last_message_id
    
    # Сохраняем последний чат, пользователя и сообщение
    last_chat_id = message.chat.id
    last_user_id = message.from_user.id
    last_message_id = message.message_id
    
    # Базовая информация
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    username = message.from_user.username or "Нет username"
    chat_id = message.chat.id
    chat_type = message.chat.type
    message_id = message.message_id
    date = message.date
    
    # Формируем базовый лог
    log_parts = [
        f"💬 Сообщение ID: {message_id}",
        f"📅 Дата: {date}",
        f"👤 Пользователь: {user_name} (@{username}, ID: {user_id})",
        f"💬 Чат: {chat_type} (ID: {chat_id})"
    ]
    
    # Проверка на пересланное сообщение
    if message.forward_from:
        log_parts.append(f"↩️ ПЕРЕСЛАНО от: {message.forward_from.full_name} (ID: {message.forward_from.id})")
    elif message.forward_from_chat:
        chat_name = message.forward_from_chat.title or "Чат"
        log_parts.append(f"↩️ ПЕРЕСЛАНО из: {chat_name} (ID: {message.forward_from_chat.id})")
    elif message.forward_date:
        log_parts.append(f"↩️ ПЕРЕСЛАНО (источник скрыт)")
    
    # Обработка разных типов контента
    content_info = []
    
    if message.text:
        content_info.append(f"📝 Текст: {message.text[:200]}{'...' if len(message.text) > 200 else ''}")
    else:
        # Если не текстовое, показываем тип
        content_info.append("📭 Не текстовое сообщение")
    
    if message.entities:
        for entity in message.entities:
            if entity.type == "bot_command":
                content_info.append(f"🤖 Команда: {message.text}")
    
    if message.photo:
        photo = message.photo[-1]
        content_info.append(f"🖼️ Фото (ID: {photo.file_id}, размер: {photo.width}x{photo.height})")
    
    if message.video:
        video = message.video
        content_info.append(f"🎬 Видео (ID: {video.file_id}, длительность: {video.duration}с, {video.width}x{video.height})")
    
    if message.document:
        doc = message.document
        file_size_mb = doc.file_size / (1024 * 1024) if doc.file_size else 0
        content_info.append(f"📄 Документ: {doc.file_name} (MIME: {doc.mime_type}, размер: {file_size_mb:.2f} MB, ID: {doc.file_id})")
    
    if message.voice:
        voice = message.voice
        content_info.append(f"🎤 Голосовое (длительность: {voice.duration}с, ID: {voice.file_id})")
    
    if message.audio:
        audio = message.audio
        content_info.append(f"🎵 Аудио: {audio.title} - {audio.performer} (длительность: {audio.duration}с)")
    
    if message.sticker:
        sticker = message.sticker
        content_info.append(f"🎨 Стикер: {sticker.emoji} (ID: {sticker.file_id}, набор: {sticker.set_name})")
    
    if message.animation:
        anim = message.animation
        content_info.append(f"🎞️ GIF-анимация (ID: {anim.file_id}, {anim.width}x{anim.height})")
    
    if message.video_note:
        vn = message.video_note
        content_info.append(f"🔄 Видео-сообщение (длительность: {vn.duration}с, ID: {vn.file_id})")
    
    if message.location:
        loc = message.location
        content_info.append(f"📍 Локация: {loc.latitude}, {loc.longitude}")
    
    if message.contact:
        contact = message.contact
        content_info.append(f"📇 Контакт: {contact.first_name} {contact.last_name or ''} (@{contact.username or 'нет username'})")
    
    if not content_info and not message.text:
        content_info.append("📭 Сообщение без содержимого (возможно, удалено или служебное)")
    
    # Вывод всей информации
    logger.info(" | ".join(log_parts))
    for info in content_info:
        logger.info(f"   {info}")
    
    # Подсказка в терминале
    print("\n" + "="*60)
    print(f"📩 Новое сообщение от {user_name} (Chat ID: {chat_id})")
    print(f"💬 Текст: {message.text if message.text else '(не текстовое)'}")
    print("="*60)
    print("📝 Команды для отправки сообщений:")
    print(f"   {chat_id} <текст>  - ответить в этот чат")
    print("   <chat_id> <текст>  - отправить в указанный чат")
    print("   /skip  - пропустить (не отвечать)")
    print("="*60)

def terminal_input_handler():
    """Функция для обработки ввода из терминала"""
    global last_chat_id
    
    while True:
        try:
            user_input = input().strip()
            if not user_input:
                continue
            
            # Команда /skip - пропустить
            if user_input.lower() == '/skip':
                print("⏭️ Пропущено")
                continue
            
            # Команда /help
            if user_input.lower() == '/help':
                print("\n📚 Доступные команды:")
                print("   <chat_id> <текст>  - отправить сообщение в указанный чат")
                print("   /skip              - пропустить (не отвечать)")
                print("   /help              - показать эту справку")
                print("   /exit              - выйти из программы")
                continue
            
            # Команда /exit
            if user_input.lower() == '/exit':
                print("👋 Выход...")
                sys.exit(0)
            
            # Парсим ввод: первый аргумент - chat_id, остальное - текст
            parts = user_input.split(maxsplit=1)
            
            if len(parts) < 2:
                print("❌ Неправильный формат. Используйте: <chat_id> <текст>")
                print("   Пример: 123456789 Привет, мир!")
                continue
            
            chat_id_str = parts[0]
            text = parts[1].strip()
            
            if not text:
                print("❌ Текст сообщения не может быть пустым")
                continue
            
            # Пробуем преобразовать chat_id в число
            try:
                chat_id = int(chat_id_str)
            except ValueError:
                print(f"❌ Неверный формат chat_id: {chat_id_str}")
                continue
            
            # Отправляем сообщение
            try:
                bot.send_message(chat_id, text)
                print(f"✅ Сообщение отправлено в чат {chat_id}")
                logger.info(f"Пользователь отправил сообщение в чат {chat_id}: {text[:50]}...")
            except Exception as e:
                print(f"❌ Ошибка отправки: {e}")
                logger.error(f"Ошибка отправки в чат {chat_id}: {e}")
                
        except KeyboardInterrupt:
            print("\n👋 Выход...")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            logger.error(f"Ошибка в terminal_input_handler: {e}")

# Функция для запуска бота и обработчика терминала
def run_bot():
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=bot.polling, kwargs={'none_stop': True})
    bot_thread.daemon = True
    bot_thread.start()
    
    # Запускаем обработчик ввода из терминала в основном потоке
    print("="*60)
    print("🚀 Бот запущен!")
    print("📝 Вводите команды в формате: <chat_id> <текст>")
    print("   Пример: 123456789 Привет, мир!")
    print("   /skip - пропустить")
    print("   /help - справка")
    print("   /exit - выход")
    print("="*60)
    
    terminal_input_handler()

if __name__ == '__main__':
    try:
        run_bot()
    except KeyboardInterrupt:
        print("\n👋 Программа остановлена")
        sys.exit(0)
