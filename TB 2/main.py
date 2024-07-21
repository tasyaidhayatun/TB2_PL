# main.py
from database_setup import BukuTable, Session
from sqlalchemy.exc import SQLAlchemyError
import logging

# Configuring logger
logging.basicConfig(
    filename='app.log',  # Nama file log
    filemode='a',  # Mode append untuk menambahkan log baru ke file
    format='%(asctime)s - %(levelname)s - %(message)s',  # Format pesan log
    level=logging.INFO  # Level log
)
logger = logging.getLogger()

class HTTPException(Exception):
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail
        super().__init__(self.detail)
        logger.error(f"HTTPException {self.status_code}: {self.detail}")

class Buku:
    def __init__(self, judul, penulis, penerbit, tahun_terbit, konten, iktisar):
        self.judul = judul
        self.penulis = penulis
        self.penerbit = penerbit
        self.tahun_terbit = tahun_terbit
        self.konten = konten
        self.iktisar = iktisar
    
    def read(self, halaman):
        if halaman <= len(self.konten):
            for i in range(halaman):
                print(f"Bab {i+1}: {self.konten[i]}")
        else:
            print("Halaman melebihi jumlah bab yang ada.")
    
    def __str__(self):
        return f"{self.judul} by {self.penulis}"

def get_buku(judul):
    session = Session()
    try:
        buku = session.query(BukuTable).filter_by(judul=judul).first()
        if buku:
            logger.info(f"Buku ditemukan: {buku.judul} oleh {buku.penulis}")
            return Buku(buku.judul, buku.penulis, buku.penerbit, buku.tahun_terbit, buku.konten.split(';'), buku.iktisar)
        else:
            logger.warning(f"Buku dengan judul '{judul}' tidak ditemukan.")
            return None
    except SQLAlchemyError as e:
        logger.error(f"SQLAlchemyError: {e}")
        return None
    finally:
        session.close()

def post_buku(buku):
    session = Session()
    try:
        buku_data = BukuTable(
            judul=buku.judul,
            penulis=buku.penulis,
            penerbit=buku.penerbit,
            tahun_terbit=buku.tahun_terbit,
            konten=';'.join(buku.konten),
            iktisar=buku.iktisar
        )
        session.add(buku_data)
        session.commit()
        logger.info(f"Buku '{buku.judul}' berhasil disimpan ke basis data.")
    except SQLAlchemyError as e:
        logger.error(f"SQLAlchemyError: {e}")
    finally:
        session.close()

# Contoh Penggunaan
buku1 = Buku("Mathematics for Machine Learning", "Marc Peter Deisenroth", "Cambridge University Press", 2020, ["Introduction", "Linear Algebra", "Calculus", "Probability"], "This book provides a comprehensive introduction to the mathematical foundations of machine learning.")

# Menyimpan objek Buku ke basis data
post_buku(buku1)

# Mengambil objek Buku dari basis data
buku_dari_db = get_buku("Mathematics for Machine Learning")
if buku_dari_db:
    print(buku_dari_db)
    buku_dari_db.read(3)
