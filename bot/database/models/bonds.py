from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Date, BigInteger, Time, CHAR
from sqlalchemy.orm import relationship

from bot.config import Base


class Bond(Base):
    """Модель облигации"""
    __tablename__ = "bonds"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.telegram_id"), nullable=False)

    secid = Column(String(20), nullable=False)
    boardid = Column(String(20), nullable=False)
    shortname = Column(String(255))
    prevwaprice = Column(Numeric(15, 2))
    yieldatprevwaprice = Column(Numeric(15, 2))
    couponvalue = Column(Numeric(15, 2))
    nextcoupon = Column(Date)
    accruedint = Column(Numeric(15, 2))
    prevprice = Column(Numeric(15, 2))
    lotsize = Column(Integer)
    facevalue = Column(Numeric(15, 2))
    boardname = Column(String(255))
    status = Column(CHAR(1))
    matdate = Column(Date)
    decimals = Column(Integer)
    couponperiod = Column(Integer)
    issuesize = Column(BigInteger)
    prevlegalcloseprice = Column(Numeric(15, 2))
    prevdate = Column(Date)
    secname = Column(String(255))
    remarks = Column(String)
    marketcode = Column(String(10))
    instrid = Column(String(10))
    sectorid = Column(String(10))
    minstep = Column(Numeric(15, 2))
    faceunit = Column(String(10))
    buybackprice = Column(Numeric(15, 2))
    buybackdate = Column(String(30))
    isin = Column(String(20))
    latname = Column(String(255))
    regnumber = Column(String(50))
    currencyid = Column(String(10))
    issuesizeplaced = Column(Numeric(15, 2))
    listlevel = Column(Integer)
    sectype = Column(CHAR(1))
    couponpercent = Column(Numeric(15, 2))
    offerdate = Column(Date)
    settledate = Column(Date)
    lotvalue = Column(Numeric(15, 2))
    facevalueonsettledate = Column(Numeric(15, 2))
    calloptiondate = Column(Date)
    putoptiondate = Column(Date)
    dateyieldfromissuer = Column(Date)
    bid = Column(Numeric(15, 2))
    biddepth = Column(Numeric(15, 2))
    offer = Column(Numeric(15, 2))
    offerdepth = Column(Numeric(15, 2))
    spread = Column(Numeric(15, 2))
    biddeptht = Column(Numeric(15, 2))
    offerdeptht = Column(Numeric(15, 2))
    open = Column(Numeric(15, 2))
    low = Column(Numeric(15, 2))
    high = Column(Numeric(15, 2))
    last = Column(Numeric(15, 2))
    lastchange = Column(Numeric(15, 2))
    lastchangeprcnt = Column(Numeric(15, 2))
    qty = Column(Numeric(15, 2))
    value = Column(Numeric(15, 2))
    yield_value = Column(Numeric(15, 2))  # Переименован в yield_value, чтобы избежать конфликта с именем поля
    value_usd = Column(BigInteger)
    waprice = Column(Numeric(15, 2))
    lastcngtolastwaprice = Column(Numeric(15, 2))
    waptoprevwapriceprcnt = Column(Numeric(15, 2))
    waptoprevwaprice = Column(Numeric(15, 2))
    yieldatwaprice = Column(Numeric(15, 2))
    yieldtoprevyield = Column(Numeric(15, 2))
    closeyield = Column(Numeric(15, 2))
    closeprice = Column(Numeric(15, 2))
    marketpricetoday = Column(Numeric(15, 2))
    marketprice = Column(Numeric(15, 2))
    lasttoprevprice = Column(Numeric(15, 2))
    numtrades = Column(Numeric(15, 2))
    voltoday = Column(Numeric(15, 2))
    valtoday = Column(BigInteger)
    valtoday_usd = Column(BigInteger)
    tradingstatus = Column(CHAR(1))
    updatetime = Column(Time)
    duration = Column(Numeric(15, 2))
    numbids = Column(Numeric(15, 2))
    numoffers = Column(Numeric(15, 2))
    change = Column(Numeric(15, 2))
    time = Column(Time)
    highbid = Column(Numeric(15, 2))
    lowoffer = Column(Numeric(15, 2))
    priceminusprevwaprice = Column(Numeric(15, 2))
    lastbid = Column(Numeric(15, 2))
    lastoffer = Column(Numeric(15, 2))
    lcurrentprice = Column(Numeric(15, 2))
    lcloseprice = Column(Numeric(15, 2))
    marketprice2 = Column(Numeric(15, 2))
    openperiodprice = Column(Numeric(15, 2))
    seqnum = Column(BigInteger)
    systime = Column(Time)
    valtoday_rur = Column(BigInteger)
    iricpiclose = Column(Numeric(15, 2))
    beiclose = Column(Numeric(15, 2))
    cbrclose = Column(Numeric(15, 2))
    yieldtooffer = Column(Numeric(15, 2))
    yieldlastcoupon = Column(Numeric(15, 2))
    tradingsession = Column(String(50))
    calloptionyield = Column(Numeric(15, 2))
    calloptionduration = Column(Numeric(15, 2))

    user = relationship("User", back_populates="bonds")
