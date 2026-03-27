from pyrogram import Client
from datetime import datetime, timedelta

api_id = 
api_hash = ''
chat_id = 

app = Client("session_parse_name", api_id=api_id, api_hash=api_hash)

async def view_recent_messages():
    async with app:
        print(f"Сообщения за последние 2 дня:\n")
        print("{:<15} {:<20} {:<15} {:<30}".format("User ID", "Имя", "Дата", "Сообщение"))
        print("-" * 85)
        
        # Текущая дата в UTC (без информации о часовом поясе)
        now = datetime.utcnow()
        two_days_ago = now - timedelta(days=2)
        
        print(f"Ищу сообщения с {two_days_ago.strftime('%d.%m.%Y')} по {now.strftime('%d.%m.%Y')}\n")
        
        count = 0
        async for message in app.get_chat_history(chat_id, limit=200):
            # Пропускаем служебные сообщения
            if not message.from_user:
                continue
            
            # Дата сообщения от Telegram (убираем информацию о часовом поясе)
            message_date = message.date.replace(tzinfo=None)
            
            # Пропускаем сообщения старше 2 дней
            if message_date < two_days_ago:
                continue
            
            # Получаем имя пользователя
            user_name = message.from_user.first_name or ""
            
            # Форматируем дату для отображения
            if message_date.date() == now.date():
                date_str = "Сегодня"
            elif message_date.date() == (now - timedelta(days=1)).date():
                date_str = "Вчера"
            else:
                date_str = message_date.strftime("%d.%m.%Y")
            
            time_str = message_date.strftime("%H:%M")
            full_date_str = f"{date_str} {time_str}"
            
            # Получаем текст сообщения
            if message.text:
                message_text = message.text[:50] + "..." if len(message.text) > 50 else message.text
            elif message.caption:
                message_text = "[Медиа] " + (message.caption[:40] + "..." if len(message.caption) > 40 else message.caption)
            elif message.sticker:
                message_text = f"[Стикер]"
            elif message.photo:
                message_text = "[Фото]"
            elif message.video:
                message_text = "[Видео]"
            elif message.document:
                message_text = "[Док]"
            else:
                continue
            
            print(f"{message.from_user.id:<15} {user_name:<20} {full_date_str:<15} {message_text}")
            count += 1
        
        if count == 0:
            print("Нет сообщений за последние 2 дня")
        else:
            print(f"\nВсего показано {count} сообщений за последние 2 дня")

app.run(view_recent_messages())