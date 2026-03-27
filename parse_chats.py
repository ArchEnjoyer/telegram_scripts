from pyrogram import Client

app = Client("session_parse_name", api_id=, api_hash='')

async def main():
    async with app:
        async for dialog in app.get_dialogs():
            print(f"{dialog.chat.title}: {dialog.chat.id}")

app.run(main())