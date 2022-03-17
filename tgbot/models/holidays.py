from sqlalchemy import Column, Date, String

from tgbot.services.db_base import Base


class Holidays(Base):
    __tablename__ = "holidays"
    holiday_date = Column(Date, nullable=False)
    holiday_name = Column(String(255), nullable=False, primary_key=True)
    hide_link = Column(String, nullable=False)
    where = Column(String, nullable=False)

    def __repr__(self):
        return f'Holidays (holiday date: {self.holiday} - hide_link: {self.hide_link})'

