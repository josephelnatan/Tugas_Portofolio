import os
import pymysql
from dotenv import load_dotenv
import cloudinary
import resend

# 1. Ambil data dari file .env
load_dotenv()

# 2. Konfigurasi Cloudinary (Untuk Upload Gambar)
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    secure=True
)

# 3. Konfigurasi Resend (Untuk Pengiriman Email)
resend.api_key = os.getenv('RESEND_API_KEY')

# 4. Fungsi untuk Menghubungkan Python ke Database TiDB
def get_db_connection():
    return pymysql.connect(
        host=os.getenv('TIDB_HOST'),
        user=os.getenv('TIDB_USER'),
        password=os.getenv('TIDB_PASSWORD'),
        database=os.getenv('TIDB_DATABASE'),
        port=int(os.getenv('TIDB_PORT', 4000)),
        ssl={'ssl': {}}, # TiDB Cloud wajib menggunakan SSL gratis bawaan
        cursorclass=pymysql.cursors.DictCursor # Biar hasil query database otomatis jadi bentuk kamus (dictionary) di Python
    )