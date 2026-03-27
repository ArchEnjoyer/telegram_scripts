import logging
import sys
import time
import asyncio
from aiogram import Bot, Dispatcher, html

YOUR_CHAT_ID = 
dp = Dispatcher()

async def main() -> None:
    bot = Bot(token='')
    
    for id_ in range(1, 10000000): #нужно с 1
        print(id_)
        try:
            await bot.forward_message(
                chat_id=YOUR_CHAT_ID,
                from_chat_id=,
                message_id=id_
            )
        except Exception as e:
            print(e)
            time.sleep(60)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())


