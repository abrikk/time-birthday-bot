from sqlalchemy import Column, BigInteger, TIMESTAMP, func, Integer, extract, \
    PrimaryKeyConstraint, String

from tgbot.services.db_base import Base


class BDStat(Base):
    __tablename__ = "bd_stat"
    bd_user_id = Column(BigInteger)
    bd_user_name = Column(String(length=100), nullable=False)
    bd_year = Column(Integer, default=extract('year', func.current_date()))
    congo_id = Column(BigInteger)
    congo_name = Column(String(length=100), nullable=False)
    congratzed_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    PrimaryKeyConstraint(bd_user_id, bd_year, congo_id, name="bdstat_pk")

    def __repr__(self):
        return f'Birthday Man (Man ID: {self.bd_user_id} -  year {self.bd_year} -' \
               f'congratulator ID {self.congo_id})'
