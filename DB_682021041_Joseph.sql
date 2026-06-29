-- 1. Tabel Admin (Untuk Login)
CREATE TABLE admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Masukkan akun admin default (username: admin, password: admin123)
-- Catatan: Di dunia nyata password harus di-hash (enkripsi), ini versi simpel untuk tugas
INSERT INTO admin (username, password) VALUES ('admin', 'admin123');

-- 2. Tabel Profil
CREATE TABLE profil (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    deskripsi TEXT,
    foto_url VARCHAR(255)
);

-- 3. Tabel Skill
CREATE TABLE skill (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_skill VARCHAR(100) NOT NULL,
    persentase INT -- Contoh: 90 (untuk 90%)
);

-- 4. Tabel Pengalaman
CREATE TABLE pengalaman (
    id INT AUTO_INCREMENT PRIMARY KEY,
    posisi VARCHAR(100) NOT NULL,
    perusahaan VARCHAR(100) NOT NULL,
    tahun VARCHAR(50),
    deskripsi TEXT
);

-- 5. Tabel Proyek
CREATE TABLE proyek (
    id INT AUTO_INCREMENT PRIMARY KEY,
    judul VARCHAR(100) NOT NULL,
    deskripsi TEXT,
    gambar_url VARCHAR(255),
    link_proyek VARCHAR(255)
);

-- 6. Tabel Kontak (Untuk menyimpan pesan dari pengunjung)
CREATE TABLE kontak (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    pesan TEXT NOT NULL,
    tanggal_kirim TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);