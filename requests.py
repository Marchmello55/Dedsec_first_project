import logging


from database.models import async_session
from database.models import User, CHATS, MESSAGE,Chat_reaction
from sqlalchemy import select
from datetime import  datetime, timedelta


"""USER"""



async def add_new_user(user_id: int) -> None:
    logging.info(f'add_new_user')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.user_id == user_id))
        if not user:
            print(1)
            user = User(user_id=user_id)
            session.add(user)
            await session.commit()

async def get_user_tg_id(user_id: int) -> User:
    logging.info('get_user_tg_id')
    async with async_session() as session:
        return await session.scalar(select(User).where(User.user_id == user_id))


async def update_user_request(user_id: int, REQUESTS: str) -> None:
    logging.info('update_username')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.user_id == user_id))
        user.REQUESTS = REQUESTS
        await session.commit()

async def include_user_request(user_id: int, REQUESTS: str) -> None:
    logging.info('update_username')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.user_id == user_id))
        user.REQUESTS += f"{REQUESTS}\n"
        await session.commit()

async def update_user_id(user_id: int, ID: str) -> None:
    logging.info('update_username')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.user_id == user_id))
        user.ID = ID
        await session.commit()

async def include_user_id(user_id: int, ID: str) -> None:
    logging.info('update_username')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.user_id == user_id))
        user.ID += f"{ID}\n"
        await session.commit()

async def update_url_user_id(user_id: int, URL: str) -> None:
    logging.info('update_honor')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.user_id == user_id))
        user.URL = URL
        await session.commit()

async def include_url_user_id(user_id: int, URL: str) -> None:
    logging.info('update_honor')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.user_id == user_id))
        user.URL += f"{URL}\n"
        await session.commit()

"""CHATS"""

async def add_new_request(REQUEST: str) -> None:
    logging.info(f'add_new_user')
    async with async_session() as session:
        user = await session.scalar(select(CHATS).where(CHATS.REQUEST == REQUEST))
        if not user:
            user = CHATS(REQUEST=REQUEST)
            session.add(user)
            await session.commit()

async def update_url_chats(REQUEST: str, URL: str) -> None:
    logging.info('update_honor')
    async with async_session() as session:
        user = await session.scalar(select(CHATS).where(CHATS.REQUEST == REQUEST))
        user.URL += f"{URL}\n"
        await session.commit()


async def get_chats(REQUEST: str) -> User:
    logging.info('get_user_tg_id')
    async with async_session() as session:
        return await session.scalar(select(CHATS).where(CHATS.REQUEST == REQUEST))

"""MESSAGE"""

async def add_new_url(URL: str) -> None:
    logging.info('update_clan_name')
    async with async_session() as session:
        user = await session.scalar(select(MESSAGE).where(MESSAGE.URL == URL))
        if not user:
            user = MESSAGE(URl=URL)
            session.add(user)
            await session.commit()


async def get_message(URL: str) -> User:
    logging.info('get_user_tg_id')
    async with async_session() as session:
        return await session.scalar(select(MESSAGE).where(MESSAGE.URL == URL))


async def update_url_message(URL: str, message_id: int) -> None:
    logging.info('update_invitation')
    async with async_session() as session:
        user = await session.scalar(select(MESSAGE).where(MESSAGE.URL == URL))
        user.message_id = message_id
        await session.commit()


async def update_text_message(URL: str, message_text: str) -> None:
    logging.info('update_clan_name')
    async with async_session() as session:
        user = await session.scalar(select(MESSAGE).where(MESSAGE.URL == URL))
        user.message_text = message_text
        await session.commit()


async def update_media_path_message(URL: str, media_path: str) -> None:
    logging.info('update_clan_name')
    async with async_session() as session:
        user = await session.scalar(select(MESSAGE).where(MESSAGE.URL == URL))
        user.media_path += rf"{media_path}" +'\n'
        await session.commit()

"""Chat_reaction"""

async def add_chat_reaction_tg_id(tg_id: int) -> None:
    logging.info('update_clan_name')
    async with async_session() as session:
        user = await session.scalar(select(Chat_reaction).where(Chat_reaction.tg_id == tg_id))
        if not user:
            user = Chat_reaction(tg_id=tg_id)
            session.add(user)
            await session.commit()


async def get_chat_reaction(tg_id: int) -> User:
    logging.info('get_user_tg_id')
    async with async_session() as session:
        return await session.scalar(select(Chat_reaction).where(Chat_reaction.tg_id == tg_id))


async def update_chat_reaction_url(tg_id: int, URL: str) -> None:
    logging.info('update_clan_name')
    async with async_session() as session:
        user = await session.scalar(select(Chat_reaction).where(Chat_reaction.tg_id == tg_id))
        user.URL = URL
        await session.commit()

async  def update_chat_reaction_message_id(tg_id:int, message_id:int):
    logging.info('after_verification_warn')
    async with async_session() as session:
        user = await session.scalar(select(Chat_reaction).where(Chat_reaction.tg_id == tg_id))
        user.message_id = message_id
        await session.commit()

async  def update_chat_reaction_comment(tg_id:int, comment: str):
    logging.info('get_warn_sum')
    async with async_session() as session:
        user = await session.scalar(select(Chat_reaction).where(Chat_reaction.tg_id == tg_id))
        user.comment = comment
        await session.commit()
