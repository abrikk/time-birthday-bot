from sqlalchemy import Column, BigInteger, String, Date, TIMESTAMP, func, SmallInteger

from tgbot.services.db_base import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(BigInteger, primary_key=True)
    first_name = Column(String(length=100), nullable=False)
    last_name = Column(String(length=100), nullable=True)
    username = Column(String(length=100), nullable=True, unique=True)
    user_bd = Column(Date, index=True, nullable=True)
    sex = Column(String(length=1), nullable=True)
    lang_code = Column(String(length=5), default='ru_RU')
    rating = Column(SmallInteger, nullable=True)
    role = Column(String(length=100), default='user')
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=func.now(),
                        onupdate=func.now(),
                        server_default=func.now())

    def __repr__(self):
        return f'User (ID: {self.user_id} - {self.first_name} {self.last_name})'
