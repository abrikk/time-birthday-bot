from sqlalchemy import Column, Date, String, Integer, PrimaryKeyConstraint

from tgbot.services.db_base import Base


class Holidays(Base):
    __tablename__ = "holidays"
    id = Column(Integer, autoincrement=True)
    holiday_date = Column(Date, nullable=False)
    holiday_name = Column(String(255), nullable=False)
    holiday_code = Column(String(128), nullable=False)
    hide_link = Column(String, nullable=True)
    where = Column(String, nullable=True)
    PrimaryKeyConstraint(id, holiday_code, name="holidays_pk")

    def __repr__(self):
        return f'Holidays (holiday date: {self.holiday} - hide_link: {self.hide_link})'

