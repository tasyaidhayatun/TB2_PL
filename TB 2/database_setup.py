from sqlalchemy import create_engine, Column, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class BukuTable(Base):
    __tablename__ = 'buku'
    id = Column(Integer, primary_key=True)
    judul = Column(String, nullable=False)
    penulis = Column(String, nullable=False)
    penerbit = Column(String, nullable=False)
    tahun_terbit = Column(Integer, nullable=False)
    konten = Column(Text, nullable=False)
    iktisar = Column(Text, nullable=False)

engine = create_engine('sqlite:///perpustakaan.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
