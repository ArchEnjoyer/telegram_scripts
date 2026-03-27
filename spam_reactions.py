from pyrogram import Client
import asyncio

api_id = 
api_hash = ''
chat_id = 
target_user_id = 
emoji = "💩"

app = Client("session_parse_name", api_id=api_id, api_hash=api_hash)

async def react_to_recent_messages():
    async with app:
        print(f"Ищем ПОСЛЕДНИЕ сообщения от пользователя {target_user_id}...")
        
        # Собираем ВСЕ сообщения пользователя
        user_messages = []
        
        async for message in app.get_chat_history(chat_id, limit=400):
            if message.from_user and message.from_user.id == target_user_id:
                user_messages.append(message)
        
        if not user_messages:
            print(f"Не найдено сообщений от пользователя {target_user_id}")
            return
        
        # Берем только ПОСЛЕДНИЕ 50 сообщений
        recent_messages = user_messages[:50]
        
        print(f"\nНайдено {len(user_messages)} сообщений от пользователя")
        print(f"Буду ставить реакции на ПОСЛЕДНИЕ {len(recent_messages)} сообщений:\n")
        
        # Показываем сообщения, на которые будут поставлены реакции
        for i, msg in enumerate(recent_messages, 1):
            timestamp = msg.date.strftime("%d.%m %H:%M")
            text_preview = msg.text[:60] + "..." if msg.text and len(msg.text) > 60 else (msg.text or "[Медиа]")
            print(f"{i}. [{timestamp}] {text_preview}")
        
        # Подтверждение
        confirm = input(f"\nПоставить реакции на эти {len(recent_messages)} сообщений? (y/n): ").lower()
        if confirm != 'y':
            print("Отменено")
            return
        
        # Ставим реакции
        print("\nНачинаю ставить реакции...")
        
        success_count = 0
        for i, message in enumerate(recent_messages, 1):
            try:
                # Способ 1: Попробуем сначала удалить старую реакцию (если есть)
                try:
                    # Если уже стоит какая-то реакция от нас, удалим её
                    await app.send_reaction(chat_id, message.id, emoji)  # Сначала поставим
                    await asyncio.sleep(0.3)
                    await app.send_reaction(chat_id, message.id, emoji)  # Поставим ещё раз (удалит если уже стоит)
                except:
                    # Если не было реакции, просто ставим новую
                    await app.send_reaction(chat_id, message.id, emoji)
                
                success_count += 1
                print(f"{i}/{len(recent_messages)} ✓ Реакция {emoji} на сообщение от {message.date.strftime('%H:%M')}")
                
                # Ждем 3 секунды перед следующим
                if i < len(recent_messages):
                    await asyncio.sleep(3)
                    
            except Exception as e:
                print(f"{i}/{len(recent_messages)} ✗ Ошибка: {e}")
                await asyncio.sleep(5)
        
        print(f"\n✅ Готово! Поставлено {success_count} реакций на последние сообщения")

app.run(react_to_recent_messages())