from sqlalchemy import Column, Date, String, Integer, PrimaryKeyConstraint

from tgbot.services.db_base import Base


class Holidays(Base):
    __tablename__ = "holidays"
    uid = Column(String(10), nullable=False)
    holiday_name = Column(String(255), nullable=False)
    holiday_date = Column(Date, nullable=False)
    photo_id = Column(String, nullable=True)
    message_id = Column(Integer, nullable=True)
    hn_en = Column(String, nullable=True)
    hn_uz = Column(String, nullable=True)
    hn_ua = Column(String, nullable=True)
    hn_es = Column(String, nullable=True)
    hn_fr = Column(String, nullable=True)
    PrimaryKeyConstraint(uid, name="holidays_pk")

    def __repr__(self):
        return f'Holidays (holiday date: {self.holiday} - hide_link: {self.hide_link})'

