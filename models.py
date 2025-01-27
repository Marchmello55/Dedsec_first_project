from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


# Создаем асинхронный движок
engine = create_async_engine("sqlite+aiosqlite:///database/db.sqlite3", echo=False)
# Настраиваем фабрику сессий
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ =  "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)#заказчики
    REQUESTS: Mapped[str] = mapped_column(String(), default='')
    ID: Mapped[str] = mapped_column(String(), default='') # люди с такими интересами ???
    URL: Mapped[str] = mapped_column(String(), default='')

class CHATS(Base):
    __tablename__ = "requests"

    REQUEST: Mapped[str] = mapped_column(primary_key=True) #для записи типовых запросов интересов
    URL: Mapped[str] = mapped_column(String(), default='') # результаты обработки запросов(ссылки на тг канал и т п)


class MESSAGE(Base):
    __tablename__ = "message"

    URL: Mapped[str] = mapped_column(primary_key=True)
    message_id: Mapped[int] = mapped_column(Integer(), default=0)#id поста
    message_text: Mapped[str] = mapped_column(String(), default='')#текст поста
    media_path: Mapped[str] = mapped_column(String(), default='')# путь к медиафайлам

#добавить новую колонку в которую вводится данные об сообщении

class Chat_reaction(Base):
    __tablename__ = "chat_reaction"

    tg_id: Mapped[int] = mapped_column(primary_key=True)
    URL: Mapped[str] = mapped_column(String(), default='')
    message_id: Mapped[int] = mapped_column(Integer(), default=0)
    comment: Mapped[str] = mapped_column(String(), default='')
    

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
