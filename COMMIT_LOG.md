# Commit Log – Music Player CLI (Simulator)

---

## 2025-12-10
**[Inisialisasi Proyek & Struktur Dasar]**  
Anggota: Avrio de Galyn Athar (103102400032)  

Perubahan:
- Membuat struktur awal proyek **Music Player CLI (Simulator)**.
- Membuat file:
  - `SongLibrary.py`:
    - Membuat class `Song` sebagai record data lagu (id, title, artist, album, genre, year, duration).
    - Mengimplementasikan ADT **Singly Linked List (SLL)** versi kampus (`Node`, `List`) sebagai dasar library lagu.
  - `YtMusic.py`:
    - Menyediakan **menu utama**:
      - Login sebagai Admin.
      - Masuk sebagai User.
- Menambahkan file awal `songLibrary.csv` sebagai sumber data lagu.

---

## 2025-12-11
**[Fitur Admin – Kelola Library Lagu (SLL + CSV)]**  
Anggota: Devika Widya Vania (103102400044)  

Perubahan:
- Menambahkan modul `admin.py` yang terhubung dengan `SongLibrary.py`.
- Implementasi fitur Admin:
  - Tambah lagu baru ke library:
    - Data disimpan ke struktur SLL (`music_library`).
    - Data disimpan permanen dengan `append_song_to_library_file()` ke `songLibrary.csv`.
  - Edit data lagu berdasarkan **ID**:
    - Cari node lagu di SLL (`find_song_node_by_id`).
    - Update field `title`, `artist`, `album`, `genre`, `year`, `duration`.
    - Simpan ulang seluruh library ke CSV menggunakan `save_library_to_file()`.
  - Hapus lagu berdasarkan **ID**:
    - Hapus node dari SLL (`delete_song_by_id`).
    - Tulis ulang isi library ke `songLibrary.csv`.
  - Lihat seluruh lagu di library:
    - Menampilkan isi SLL dengan `print_all_songs()`.
- Memastikan setiap perubahan Admin (add/edit/delete) **langsung sinkron** ke file `songLibrary.csv`.

---

## 2025-12-12
**[Fitur User – Playlist (DLL), Stack History, Queue Up Next]**  
Anggota: Nicholas (103102400047)  

Perubahan:
- Menambahkan modul:
  - `playlist.py`  
    - Mengimplementasikan ADT **Doubly Linked List (DLL)** versi kampus untuk playlist:
      - `Node` (info, next, prev).
      - `List` dengan `first` dan `last`.
    - Membuat class `PlaylistDoublyLinkedList` di atas ADT DLL untuk menyimpan urutan lagu dalam playlist user.
  - `HistoryLagu.py`  
    - Mengimplementasikan ADT **StackList** (stack berbasis linked list):
      - Operasi `push`, `pop`, `isEmpty`, `printStack`.
    - Digunakan sebagai riwayat lagu yang sudah diputar (fitur `Previous`).
  - `UpNext.py`  
    - Mengimplementasikan ADT **QueueList** (queue berbasis linked list):
      - Operasi `enqueue`, `dequeue`, `isEmpty`, `printQueue`.
    - Digunakan untuk antrian lagu `Up Next`.
  - `user.py`  
    - Berisi seluruh logika menu untuk User (library, playlist, now playing, queue, history).

- Fitur User yang diimplementasikan:
  - **Library User**:
    - Lihat semua lagu di library (menggunakan `music_library.print_all_songs()` dari `SongLibrary.py`).
    - Cari lagu berdasarkan kata kunci judul (traversal SLL dan pencocokan substring).
  - **Playlist (DLL)**:
    - Buat playlist baru (disimpan di `user_playlists_dictionary`).
    - Tampilkan daftar semua nama playlist.
    - Lihat isi playlist tertentu (traversal DLL).
    - Tambah lagu ke playlist berdasarkan **ID lagu** dari library (ambil node dari `music_library`).
    - Hapus lagu dari playlist berdasarkan ID.
  - **History (Stack)**:
    - Setiap ganti lagu (`Next`/putar lagu baru), lagu lama di-*push* ke `SongStack`.
    - Fitur `Previous` mengambil lagu terakhir dari stack (`pop`) dan menjadikannya `Now Playing`.
  - **Up Next (Queue)**:
    - Menambahkan lagu-lagu ke antrian Up Next menggunakan QueueList.
    - Menampilkan isi antrian.
    - Menghapus lagu paling depan dari antrian tanpa memutar.

---

## 2025-12-12
**[Perubahan Logika User – Putar Berdasarkan Judul & Antrian Random]**  
Anggota: Nicholas (103102400047)  

Perubahan:
- Mengubah cara memilih lagu dari library:
  - Sebelumnya: user memasukkan **ID lagu**.
  - Sekarang: user memasukkan **judul lagu** (substring, case-insensitive) dan sistem mencari node menggunakan `find_song_node_by_title()` di `SongLibrary.py`.
- Menambahkan fitur **antrian random Up Next**:
  - User dapat memilih berapa banyak lagu random dari library yang dimasukkan ke antrian.
  - Implementasi menggunakan fungsi `get_all_songs_from_library_as_list()` dan `random.choice()`.
  - Antrian lama dikosongkan sebelum membuat antrian baru.
- Mengatur prioritas `Next`:
  1. Jika Queue Up Next **tidak kosong** → ambil dari Queue.
  2. Else jika sedang ada playlist aktif dan masih ada lagu lanjut di DLL → ambil node berikutnya.
  3. Else → ambil 1 lagu random dari library (fallback).

---

## 2025-12-13
**[Simulasi Now Playing + Timer Durasi di Background]**  
Anggota: Nicholas (103102400047)  

Perubahan:
- Menambahkan **simulasi durasi lagu** (bukan audio sungguhan) di `user.py`:
  - Menggunakan field `song_duration` (format `m:ss`) dari objek `Song`.
  - Menggunakan modul `time` dan `threading`:
    - Fungsi `start_playback_timer(song)` untuk memulai timer.
    - Worker `_playback_worker()` berjalan di thread terpisah:
      - Mengurangi sisa durasi setiap 1 detik.
      - Saat habis, mencetak pesan bahwa lagu selesai dan mengingatkan user untuk menekan menu `Next`.
  - Menyimpan:
    - `current_song_duration_seconds`.
    - `song_start_time` (timestamp saat lagu mulai).
- Menyesuaikan fungsi:
  - `user_play_song_from_library()` → memanggil `start_playback_timer()` setelah mengganti Now Playing.
  - `user_go_to_next_song()` → memulai ulang timer untuk lagu berikutnya (baik dari Up Next, playlist, maupun random).
  - `user_show_current_now_playing_song()`:
    - Menghitung posisi waktu berjalan saat ini berdasarkan `time.time() - song_start_time`.
    - Menampilkan progres durasi: `menit:detik / total_durasi`.
- Timer dibuat **non-blok** (jalan di background) sehingga:
  - Menu User / Now Playing tetap responsif.
  - User bisa membuat playlist, mengubah antrian, atau navigasi menu sambil “lagu berjalan”.

---

## 2025-12-13
**[Refactor Menjadi Simulator & Bug Fix Sinkronisasi]**  
Anggota: Avrio de Galyn Athar dan Devika Widya Vania (103102400044)  

Perubahan:
- Mengklarifikasi bahwa aplikasi adalah **Music Player CLI – Simulator**:
  - Tidak memutar file `.mp3` asli.
  - Hanya mensimulasikan alur pemutaran dan durasi lagu.
- Memperbaiki masalah sinkronisasi admin–user:
  - Memastikan `user_show_all_songs_in_library()` memanggil `load_song_library_from_file()` sehingga perubahan yang dilakukan Admin (tambah / hapus / edit lagu) tercermin juga di sisi User.
- Membersihkan dan merapikan kode:
  - Memastikan pemisahan per modul:
    - `SongLibrary.py` → model `Song`, ADT SLL, fungsi CSV (load/save/append).
    - `admin.py` → seluruh fitur Admin.
    - `user.py` → seluruh fitur User (library, playlist, Now Playing, history, Up Next, timer).
    - `playlist.py` → ADT DLL khusus playlist.
    - `HistoryLagu.py` → StackList untuk riwayat lagu.
    - `UpNext.py` → QueueList untuk antrian Up Next.
  - Menguji ulang seluruh fitur:
    - Lihat & cari lagu di library.
    - Playlist: buat, lihat, tambah lagu, hapus lagu, play dari playlist.
    - Up Next: random dari library, lihat antrian, hapus head.
    - Now Playing: Next, Previous, cek durasi berjalan.
