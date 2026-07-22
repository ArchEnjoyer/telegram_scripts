import telebot
import logging
from telebot.types import Message

# Токен вашего бота
TOKEN = ''

# Настройка логов
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
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
    
    # --- ПРОВЕРКА НА ПЕРЕСЛАННОЕ СООБЩЕНИЕ ---
    if message.forward_from:
        # Переслано от пользователя
        log_parts.append(f"↩️ ПЕРЕСЛАНО от: {message.forward_from.full_name} (ID: {message.forward_from.id})")
    elif message.forward_from_chat:
        # Переслано из чата/канала
        chat_name = message.forward_from_chat.title or "Чат"
        log_parts.append(f"↩️ ПЕРЕСЛАНО из: {chat_name} (ID: {message.forward_from_chat.id})")
    elif message.forward_date:
        # Переслано, но источник скрыт (пользователь запретил пересылку)
        log_parts.append(f"↩️ ПЕРЕСЛАНО (источник скрыт)")
    
    # --- ОБРАБОТКА РАЗНЫХ ТИПОВ КОНТЕНТА ---
    content_info = []
    
    # Текст
    if message.text:
        content_info.append(f"📝 Текст: {message.text[:200]}{'...' if len(message.text) > 200 else ''}")
    
    # Команда бота
    if message.entities:
        for entity in message.entities:
            if entity.type == "bot_command":
                content_info.append(f"🤖 Команда: {message.text}")
    
    # Фото
    if message.photo:
        photo = message.photo[-1]  # Самое большое фото
        content_info.append(f"🖼️ Фото (ID: {photo.file_id}, размер: {photo.width}x{photo.height})")
    
    # Видео
    if message.video:
        video = message.video
        content_info.append(f"🎬 Видео (ID: {video.file_id}, длительность: {video.duration}с, {video.width}x{video.height})")
    
    # Документ
    if message.document:
        doc = message.document
        file_size_mb = doc.file_size / (1024 * 1024) if doc.file_size else 0
        content_info.append(f"📄 Документ: {doc.file_name} (MIME: {doc.mime_type}, размер: {file_size_mb:.2f} MB, ID: {doc.file_id})")
    
    # Голосовое сообщение
    if message.voice:
        voice = message.voice
        content_info.append(f"🎤 Голосовое (длительность: {voice.duration}с, ID: {voice.file_id})")
    
    # Аудио
    if message.audio:
        audio = message.audio
        content_info.append(f"🎵 Аудио: {audio.title} - {audio.performer} (длительность: {audio.duration}с)")
    
    # Стикер
    if message.sticker:
        sticker = message.sticker
        content_info.append(f"🎨 Стикер: {sticker.emoji} (ID: {sticker.file_id}, набор: {sticker.set_name})")
    
    # Анимация (GIF)
    if message.animation:
        anim = message.animation
        content_info.append(f"🎞️ GIF-анимация (ID: {anim.file_id}, {anim.width}x{anim.height})")
    
    # Видео-сообщение (кружок)
    if message.video_note:
        vn = message.video_note
        content_info.append(f"🔄 Видео-сообщение (длительность: {vn.duration}с, ID: {vn.file_id})")
    
    # Локация
    if message.location:
        loc = message.location
        content_info.append(f"📍 Локация: {loc.latitude}, {loc.longitude}")
    
    # Контакт
    if message.contact:
        contact = message.contact
        content_info.append(f"📇 Контакт: {contact.first_name} {contact.last_name or ''} (@{contact.username or 'нет username'})")
    
    # Если сообщение пустое (не содержит ни одного из вышеперечисленных типов)
    if not content_info and not message.text:
        content_info.append("📭 Сообщение без содержимого (возможно, удалено или служебное)")
    
    # --- ВЫВОД ВСЕЙ ИНФОРМАЦИИ ---
    logger.info(" | ".join(log_parts))
    for info in content_info:
        logger.info(f"   {info}")
    
    # Если нужно сохранить в файл, раскомментируйте:
    # with open("messages_log.txt", "a", encoding="utf-8") as f:
    #     f.write(" | ".join(log_parts) + "\n")
    #     for info in content_info:
    #         f.write(f"   {info}\n")

# Запуск бота
if __name__ == '__main__':
    logger.info("🚀 Бот запущен и ожидает сообщений...")
    bot.polling(none_stop=True)
