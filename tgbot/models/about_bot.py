from datetime import date

from sqlalchemy import Column, TIMESTAMP, func, String, Date, Integer

from tgbot.services.db_base import Base


class AboutBot(Base):
    __tablename__ = "botinfo"
    username = Column(String, nullable=False, primary_key=True)
    version = Column(String(length=5), nullable=False, default="0.0.0")
    languages = Column(Integer, nullable=False, default=2)
    updated_at = Column(TIMESTAMP(timezone=True), default=func.now(), onupdate=func.now(),
                        server_default=func.now())
    updated_on = Column(Date, default=date.today())
    released_on = Column(Date, default=date(2022, 1, 9))
    created_on = Column(Date, default=date(2021, 12, 25))

    def __repr__(self):
        return f'AboutBot (version: {self.version} - updated on: {self.updated_on})'
