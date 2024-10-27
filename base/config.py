from os import getenv
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

engine = create_engine(getenv("DATABASE_URL"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True)
    contract = Column(String(9), unique=True)
    phone = Column(String(15))
    address = Column(String(255))
    service = Column(String(45))
<<<<<<< HEAD
    intent = Column(String(550))
    user_text = Column(String(800))


class People(Base):
    __tablename__ = 'peoples'

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(50))
    role = Column(String(55))
    password = Column(String(10))
=======
>>>>>>> 8dcd97331709b8b89578eed676f75abdbfe3a14f

Base.metadata.create_all(bind=engine)
