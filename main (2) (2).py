import os
import re
import logging

from telethon import TelegramClient, events
from config import Config, load_config
from database import requests as rq
from database import models
from telethon.errors import PeerFloodError
import tempCodeRunnerFile as cr

# Загружаем конфигурацию
config: Config = load_config()
api_id = config.tg_bot.api_id
api_hash = config.tg_bot.api_hash

# Создаем клиент
client = TelegramClient('session_name', api_id, api_hash, system_version="4.16.30-vxCUSTOM")


async def forward_message(from_chat: str, to_chat: str, message_id: int):
    try:
        await client.forward_messages(to_chat, message_id, from_chat)
        print(f"Сообщение {message_id} успешно переслано из {from_chat} в {to_chat}.")
    except Exception as e:
        print(f"Ошибка при пересылке сообщения: {e}")



async def download_media_from_post(chat: str, message_id: int, download_path: str = 'C:/Users/zah-g/OneDrive/Desktop/Downloads_pictures'):
    try:
        os.makedirs(download_path, exist_ok=True)
        message = await client.get_messages(chat, ids=message_id)

        if message.media:
            file_path = await client.download_media(message, file=download_path)
            text = cr.main(file_path)
            await client.send_message(
            entity=chat,           # Чат, на который отправляется ответ
            message=text,    # Текст ответа
            reply_to=message_id    # ID сообщения, на которое отвечаем
        )
            print(f"Медиафайл скачан: {file_path}")
        else:
            print("Сообщение не содержит медиафайлов.")
    except Exception as e:
        print(f"Ошибка при скачивании медиа: {e}")




@client.on(events.NewMessage())
async def handle_messages(event):
    sender = await event.get_sender()
    message = event.message
    # Определяем имя отправителя (пользователь, канал или чат)
    if hasattr(sender, 'first_name') and sender.first_name:
        sender_name = sender.first_name  # Имя пользователя
    elif hasattr(sender, 'title') and sender.title:
        sender_name = sender.title  # Название канала или чата
    else:
        sender_name = "Неизвестный отправитель"  # На случай отсутствия информации

    message_text = event.message.text.strip().lower()


    if event.is_private:
        if sender.id == 1663197277 :
            await download_media_from_post(chat=1663197277, message_id=message.id, download_path='C:/Users/zah-g/OneDrive/Desktop/Downloads_pictures')
        



async def main():
    await models.async_main()
    await client.start()
    print("Клиент запущен")
    await client.run_until_disconnected()


if __name__ == "__main__":
    client.loop.run_until_complete(main())