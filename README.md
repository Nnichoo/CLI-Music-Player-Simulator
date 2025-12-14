# Music Player CLI – Simulator Tugas Besar Struktur Data

**Anggota Kelompok**:
* Nicholas / NIM 103102400047 
* Devika Widya Vania / 103102400044
* Avrio de Galyn Athar / 103102400032

**Music Player CLI** adalah *simulator* pemutar musik berbasis terminal
yang dibuat untuk tugas besar mata kuliah Struktur Data.  
Simulator ini mencontoh perilaku layanan streaming musik: library lagu,
playlist, antrian `Up Next`, riwayat pemutaran, dan sistem `Now Playing`
(durasi lagu hanya disimulasikan, tidak memutar audio sungguhan).

---
## Struktur Project
```
CLI-Music-Player-Simulator/
├── YtMusic.py              
├── songLibrary.csv         
├── SongLibrary.py          
├── user.py                 
├── admin.py                
├── playlist.py             
├── HistoryLagu.py          
├── UpNext.py               
├── README.md               
└── COMMIT_LOG.md
```           

## Fitur Utama

### 1. Manajemen Library Lagu (Singly Linked List / SLL)
- Data lagu disimpan sebagai record `Song`.
- Struktur data library menggunakan **ADT List & Node (SLL)** versi kampus.
- Data lagu dimuat dari file CSV `songLibrary.csv`.
- Mode Admin bisa:
  - Menambah lagu baru.
  - Mengubah data lagu.
  - Menghapus lagu.
  - Melihat daftar semua lagu di library.
- Perubahan library otomatis disimpan kembali ke file CSV.

### 2. Playlist (Doubly Linked List / DLL)
- User dapat membuat banyak playlist.
- Setiap playlist disimpan sebagai **Doubly Linked List (List & Node DLL)**.
- Fitur playlist:
  - Membuat playlist baru.
  - Menampilkan semua nama playlist.
  - Melihat isi playlist tertentu.
  - Menambah lagu ke playlist (berdasarkan ID lagu di library).
  - Menghapus lagu dari playlist.
  - Memutar lagu dari playlist (mengatur `Now Playing` + pointer node aktif).

### 3. Riwayat Lagu (Stack)
- Riwayat lagu yang pernah diputar disimpan menggunakan **Stack berbasis linked list (StackList)**.
- Setiap kali ganti lagu (`Next` atau putar lagu baru), lagu sebelumnya di-*push* ke Stack.
- Menu `Previous` akan mengambil lagu dari Stack (operasi `pop`).

### 4. Antrian Up Next (Queue)
- Antrian `Up Next` menggunakan **Queue berbasis linked list (QueueList)**.
- User bisa:
  - Membuat antrian random dari library (memilih jumlah lagu).
  - Melihat isi antrian.
  - Menghapus lagu paling depan dari antrian tanpa memutar.
- Fitur `Next` memprioritaskan:
  1. Lagu dari queue `Up Next`.
  2. Kalau queue kosong, lanjut ke lagu berikutnya di playlist aktif.
  3. Kalau dua-duanya kosong, pilih 1 lagu random dari library.

### 5. Now Playing + Simulasi Durasi Lagu
- Menampilkan lagu yang sedang “diputar”.
- **Simulasi durasi lagu** berdasarkan field `song_duration` (format `m:ss`).
- Timer berjalan di background menggunakan **threading**, jadi user tetap bisa
  memakai menu lain.
- User bisa mengecek posisi durasi saat ini lewat menu:
  - `Menu Now Playing` → `Tampilkan lagu yang sedang diputar`.

> Catatan: Simulator ini **tidak memutar file audio asli (.mp3)**, hanya mensimulasikan
> alur pemutaran dan durasi lagunya di terminal.

---

## Cara Menjalankan Program

### 1. Prasyarat
- Python **3.10+** sudah terinstal.
- Sistem operasi: diuji di **macOS**, tapi harusnya juga bisa di **Windows / Linux**.
- Modul yang digunakan hanya dari Python Standard Library:
  - `csv`, `os`, `time`, `threading`, `random`.

### 2. Langkah Instalasi & Run

1. **Clone atau download repository** ke perangkat lokal:
   ```bash
   git clone https://github.com/Nnichoo/CLI-Music-Player-Simulator.git
   cd CLI-Music-Player-Simulator
   ```

2. **Jalankan program simulator**:
   ```bash
   python YtMusic.py
   ```
   

   
