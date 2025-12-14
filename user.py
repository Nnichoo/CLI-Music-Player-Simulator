import random
import time
import threading

from SongLibrary import (
    music_library,
    get_all_songs_from_library_as_list,
)

from playlist import PlaylistDoublyLinkedList
from HistoryLagu import SongStack
from UpNext import SongQueue


# ====== GLOBAL STATE PEMUTARAN ======
user_playlists_dictionary = {}
user_now_playing_song = None
user_current_active_playlist = None
user_current_song_node_in_active_playlist = None

user_play_history_stack = SongStack()
user_up_next_song_queue = SongQueue()

playback_thread = None
playback_stop_event = threading.Event()
current_song_duration_seconds = 0
song_start_time = None


# ====== TIMER BACKGROUND UNTUK DURASI LAGU ======

def start_playback_timer(song):
    global playback_thread, playback_stop_event
    global current_song_duration_seconds, song_start_time

    # matikan timer lama (kalau masih hidup)
    if playback_thread is not None and playback_thread.is_alive():
        playback_stop_event.set()
        playback_thread.join(timeout=0.1)

    playback_stop_event = threading.Event()

    # baca durasi lagu
    try:
        minutes, seconds = map(int, song.song_duration.split(":"))
        current_song_duration_seconds = minutes * 60 + seconds
    except Exception:
        current_song_duration_seconds = 0

    song_start_time = time.time()

    # kalau durasi valid, mulai thread background
    if current_song_duration_seconds > 0:
        playback_thread = threading.Thread(
            target=_playback_worker,
            args=(playback_stop_event,),
            daemon=True,
        )
        playback_thread.start()


def _playback_worker(stop_event):
    global current_song_duration_seconds

    remaining = current_song_duration_seconds

    # Hanya tidur, tidak nge-print tiap detik
    while remaining > 0 and not stop_event.is_set():
        time.sleep(1)
        remaining -= 1

    if not stop_event.is_set():
        print("\n(Lagu selesai otomatis. Tekan 4 di menu Now Playing untuk ke lagu berikutnya.)")


# ====== FUNGSI BANTUAN LIBRARY & QUEUE ======

def add_random_song_to_up_next_from_library():
    global user_now_playing_song

    all_songs = get_all_songs_from_library_as_list()
    if not all_songs:
        return False

    if user_now_playing_song is not None and len(all_songs) > 1:
        candidates = [s for s in all_songs if s.song_id != user_now_playing_song.song_id]
        if candidates:
            random_song = random.choice(candidates)
        else:
            random_song = random.choice(all_songs)
    else:
        random_song = random.choice(all_songs)

    user_up_next_song_queue.enqueue_song(random_song)
    return True


# ==========================
# LIBRARY & SEARCH
# ==========================

def user_show_all_songs_in_library():
    print("\n=== Semua Lagu di Library ===")
    music_library.print_all_songs()
    print()


def user_search_song_in_library():
    print("\n=== Cari Lagu di Library ===")
    search_keyword = input("Masukkan kata kunci judul lagu: ").lower()

    if music_library.head_node is None:
        print("Library lagu masih kosong.\n")
        return

    current_song_node = music_library.head_node
    found_any_song = False

    while current_song_node is not None:
        current_title_lower = current_song_node.song_data.song_title.lower()
        if search_keyword in current_title_lower:
            print(current_song_node.song_data)
            found_any_song = True
        current_song_node = current_song_node.next_node

    if not found_any_song:
        print("Tidak ada lagu yang cocok dengan kata kunci tersebut.\n")
    else:
        print()


# ==========================
# PLAYLIST
# ==========================

def user_create_new_playlist():
    print("\n=== Buat Playlist Baru ===")
    new_playlist_name = input("Masukkan nama playlist baru: ")

    if new_playlist_name in user_playlists_dictionary:
        print("Nama playlist sudah ada, silakan gunakan nama lain.\n")
        return

    new_playlist_object = PlaylistDoublyLinkedList(new_playlist_name)
    user_playlists_dictionary[new_playlist_name] = new_playlist_object
    print(f"Playlist '{new_playlist_name}' berhasil dibuat.\n")


def user_show_all_playlists_name():
    print("\n=== Daftar Playlist User ===")
    if not user_playlists_dictionary:
        print("Belum ada playlist yang dibuat.\n")
        return

    for index, playlist_name in enumerate(user_playlists_dictionary.keys(), start=1):
        print(f"{index}. {playlist_name}")
    print()


def user_show_playlist_content():
    print("\n=== Lihat Isi Playlist ===")
    target_playlist_name = input("Masukkan nama playlist: ")

    playlist_object = user_playlists_dictionary.get(target_playlist_name)
    if playlist_object is None:
        print("Playlist dengan nama tersebut tidak ditemukan.\n")
        return

    print(f"\nIsi playlist '{target_playlist_name}':")
    playlist_object.print_all_songs_in_playlist()
    print()


def user_add_song_to_playlist():
    print("\n=== Tambah Lagu ke Playlist ===")
    target_playlist_name = input("Masukkan nama playlist: ")

    playlist_object = user_playlists_dictionary.get(target_playlist_name)
    if playlist_object is None:
        print("Playlist dengan nama tersebut tidak ditemukan.\n")
        return

    target_song_id = input("Masukkan ID lagu yang ingin ditambahkan ke playlist: ")
    target_song_node_in_library = music_library.find_song_node_by_id(target_song_id)

    if target_song_node_in_library is None:
        print("Lagu dengan ID tersebut tidak ditemukan di library.\n")
        return

    playlist_object.add_song_to_playlist_end(target_song_node_in_library.song_data)
    print(f"Lagu berhasil ditambahkan ke playlist '{target_playlist_name}'.\n")


def user_remove_song_from_playlist():
    print("\n=== Hapus Lagu dari Playlist ===")
    target_playlist_name = input("Masukkan nama playlist: ")

    playlist_object = user_playlists_dictionary.get(target_playlist_name)
    if playlist_object is None:
        print("Playlist dengan nama tersebut tidak ditemukan.\n")
        return

    target_song_id = input("Masukkan ID lagu yang ingin dihapus dari playlist: ")
    has_removed_song = playlist_object.remove_song_from_playlist_by_id(target_song_id)

    if has_removed_song:
        print(f"Lagu berhasil dihapus dari playlist '{target_playlist_name}'.\n")
    else:
        print("Lagu dengan ID tersebut tidak ditemukan di playlist.\n")


def user_play_song_from_playlist():
    global user_now_playing_song
    global user_current_active_playlist
    global user_current_song_node_in_active_playlist

    print("\n=== Putar Lagu dari Playlist ===")
    target_playlist_name = input("Masukkan nama playlist: ")

    playlist_object = user_playlists_dictionary.get(target_playlist_name)
    if playlist_object is None:
        print("Playlist dengan nama tersebut tidak ditemukan.\n")
        return

    target_song_id = input("Masukkan ID lagu yang ingin diputar dari playlist: ")
    target_song_node_in_playlist = (
        playlist_object.find_song_node_in_playlist_by_id(target_song_id)
    )

    if target_song_node_in_playlist is None:
        print("Lagu dengan ID tersebut tidak ditemukan di playlist.\n")
        return

    if user_now_playing_song is not None:
        user_play_history_stack.push_song_to_stack(user_now_playing_song)

    user_now_playing_song = target_song_node_in_playlist.song_data
    user_current_active_playlist = playlist_object
    user_current_song_node_in_active_playlist = target_song_node_in_playlist

    print(f"\nSekarang memutar lagu dari playlist '{target_playlist_name}':")
    print(user_now_playing_song)
    start_playback_timer(user_now_playing_song)


def user_playlist_menu():
    while True:
        print("\n=== MENU PLAYLIST USER ===")
        print("[1] Buat playlist baru")
        print("[2] Lihat semua nama playlist")
        print("[3] Lihat isi playlist")
        print("[4] Tambah lagu ke playlist")
        print("[5] Hapus lagu dari playlist")
        print("[6] Putar lagu dari playlist")
        print("[0] Kembali ke menu User")
        playlist_menu_choice = input("Pilihan menu Playlist User: ")

        if playlist_menu_choice == "1":
            user_create_new_playlist()
        elif playlist_menu_choice == "2":
            user_show_all_playlists_name()
        elif playlist_menu_choice == "3":
            user_show_playlist_content()
        elif playlist_menu_choice == "4":
            user_add_song_to_playlist()
        elif playlist_menu_choice == "5":
            user_remove_song_from_playlist()
        elif playlist_menu_choice == "6":
            user_play_song_from_playlist()
        elif playlist_menu_choice == "0":
            break
        else:
            print("Pilihan menu Playlist tidak valid, silakan coba lagi.")


# ==========================
# NOW PLAYING + QUEUE + HISTORY
# ==========================

def user_show_current_now_playing_song():
    global song_start_time, current_song_duration_seconds

    if user_now_playing_song is None:
        print("Saat ini tidak ada lagu yang sedang diputar.\n")
        return

    print("\n=== Sedang Diputar ===")
    print(user_now_playing_song)

    if song_start_time is None or current_song_duration_seconds <= 0:
        print(f"  Posisi: ? / {user_now_playing_song.song_duration}\n")
        return

    elapsed = int(time.time() - song_start_time)
    if elapsed < 0:
        elapsed = 0
    if elapsed > current_song_duration_seconds:
        elapsed = current_song_duration_seconds

    mins = elapsed // 60
    secs = elapsed % 60
    print(f"  Posisi sekarang: {mins}:{secs:02d} / {user_now_playing_song.song_duration}\n")


def user_play_song_from_library():
    global user_now_playing_song
    global user_current_active_playlist
    global user_current_song_node_in_active_playlist

    print("\n=== Putar Lagu dari Library ===")
    input_song_title = input("Masukkan JUDUL lagu yang ingin diputar: ")

    target_song_node_in_library = music_library.find_song_node_by_title(input_song_title)
    if target_song_node_in_library is None:
        print("Lagu dengan judul tersebut tidak ditemukan di library.\n")
        return

    if user_now_playing_song is not None:
        user_play_history_stack.push_song_to_stack(user_now_playing_song)

    user_now_playing_song = target_song_node_in_library.song_data
    user_current_active_playlist = None
    user_current_song_node_in_active_playlist = None

    print("\n▶️  Sekarang memutar lagu dari library:")
    print(user_now_playing_song)
    start_playback_timer(user_now_playing_song)


def user_add_song_to_up_next_queue():
    global user_up_next_song_queue

    print("\n=== Buat Antrian Random dari Library (Up Next) ===")
    all_songs = get_all_songs_from_library_as_list()
    if not all_songs:
        print("Library lagu masih kosong.\n")
        return

    jumlah_str = input("Masukkan jumlah lagu random untuk antrian Up Next (misal 5): ")
    try:
        jumlah = int(jumlah_str)
    except ValueError:
        print("Input jumlah lagu harus berupa angka.\n")
        return

    if jumlah <= 0:
        print("Jumlah lagu harus lebih besar dari 0.\n")
        return

    # clear antrian: buat queue baru
    user_up_next_song_queue = SongQueue()

    for _ in range(jumlah):
        random_song = random.choice(all_songs)
        user_up_next_song_queue.enqueue_song(random_song)

    print(f"Antrian Up Next telah diisi {jumlah} lagu random dari library.\n")
    user_show_up_next_queue()
    print()


def user_show_up_next_queue():
    print("\n=== Antrian Lagu (Up Next) ===")
    user_up_next_song_queue.show_all_songs_in_queue()
    print()


def user_remove_next_song_from_up_next_queue():
    print("\n=== Hapus Lagu Paling Depan dari Antrian (Tanpa Diputar) ===")
    removed_song = user_up_next_song_queue.remove_first_song_without_playing()

    if removed_song is None:
        print("Tidak ada lagu di antrian Up Next yang bisa dihapus.\n")
    else:
        print("Lagu berikut ini telah dihapus dari antrian tanpa diputar:")
        print(removed_song)
        print()


def user_go_to_next_song():
    global user_now_playing_song
    global user_current_song_node_in_active_playlist

    if user_now_playing_song is None:
        print("Belum ada lagu yang sedang diputar.\n")
        return

    user_play_history_stack.push_song_to_stack(user_now_playing_song)

    if not user_up_next_song_queue.is_song_queue_empty():
        next_song_from_queue = user_up_next_song_queue.dequeue_song()
        user_now_playing_song = next_song_from_queue
        user_current_song_node_in_active_playlist = None

        print("\nSekarang memutar (dari Up Next):")
        print(user_now_playing_song)
        start_playback_timer(user_now_playing_song)
        return

    if (
        user_current_song_node_in_active_playlist is not None
        and user_current_song_node_in_active_playlist.next_song_node is not None
    ):
        user_current_song_node_in_active_playlist = (
            user_current_song_node_in_active_playlist.next_song_node
        )
        user_now_playing_song = (
            user_current_song_node_in_active_playlist.song_data
        )

        print("\nSekarang memutar (Next dari playlist):")
        print(user_now_playing_song)
        start_playback_timer(user_now_playing_song)
        return

    if add_random_song_to_up_next_from_library():
        next_song_from_queue = user_up_next_song_queue.dequeue_song()
        user_now_playing_song = next_song_from_queue
        user_current_song_node_in_active_playlist = None

        print("\nSekarang memutar (lagu random dari library):")
        print(user_now_playing_song)
        start_playback_timer(user_now_playing_song)
        return

    print("Tidak ada lagu berikutnya di library.\n")


def user_go_to_previous_song():
    global user_now_playing_song
    global user_current_song_node_in_active_playlist

    previous_song = user_play_history_stack.pop_song_from_stack()
    if previous_song is None:
        print("Tidak ada lagu sebelumnya di riwayat.\n")
        return

    user_now_playing_song = previous_song
    user_current_song_node_in_active_playlist = None

    print("\nKembali ke lagu sebelumnya:")
    print(user_now_playing_song)
    start_playback_timer(user_now_playing_song)


def user_now_playing_menu():
    while True:
        print("\n=== MENU NOW PLAYING ===")
        print("[1] Tampilkan lagu yang sedang diputar")
        print("[2] Putar lagu dari library (pilih judul lagu)")
        print("[3] Buat antrian random dari library (Up Next)")
        print("[4] Lagu berikutnya (Next)")
        print("[5] Lagu sebelumnya (Previous dari history)")
        print("[6] Lihat daftar antrian Up Next")
        print("[7] Hapus lagu paling depan dari antrian (tanpa diputar)")
        print("[0] Kembali ke menu User")
        now_playing_choice = input("Pilihan menu Now Playing: ")

        if now_playing_choice == "1":
            user_show_current_now_playing_song()
        elif now_playing_choice == "2":
            user_play_song_from_library()
        elif now_playing_choice == "3":
            user_add_song_to_up_next_queue()
        elif now_playing_choice == "4":
            user_go_to_next_song()
        elif now_playing_choice == "5":
            user_go_to_previous_song()
        elif now_playing_choice == "6":
            user_show_up_next_queue()
        elif now_playing_choice == "7":
            user_remove_next_song_from_up_next_queue()
        elif now_playing_choice == "0":
            break
        else:
            print("Pilihan menu Now Playing tidak valid, silakan coba lagi.")


# ==========================
# MENU USER (ROOT)
# ==========================

def user_menu():
    while True:
        print("\n=== MENU USER ===")
        print("[1] Lihat semua lagu di library")
        print("[2] Cari lagu di library")
        print("[3] Kelola playlist")
        print("[4] Menu Now Playing (Play / Next / Prev / Queue)")
        print("[0] Kembali ke menu utama")
        user_menu_choice = input("Pilihan menu User: ")

        if user_menu_choice == "1":
            user_show_all_songs_in_library()
        elif user_menu_choice == "2":
            user_search_song_in_library()
        elif user_menu_choice == "3":
            user_playlist_menu()
        elif user_menu_choice == "4":
            user_now_playing_menu()
        elif user_menu_choice == "0":
            break
        else:
            print("Pilihan menu User tidak valid, silakan coba lagi.")
