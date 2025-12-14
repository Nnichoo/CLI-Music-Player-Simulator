from SongLibrary import (
    Song,
    music_library,
    append_song_to_library_file,
    save_library_to_file,
)

def admin_add_new_song():
    print("\n=== Tambah Lagu ke Library ===")
    input_song_id = input("ID lagu         : ")
    input_song_title = input("Judul lagu      : ")
    input_song_artist = input("Nama artis      : ")
    input_song_album = input("Nama album      : ")
    input_song_genre = input("Genre lagu      : ")
    input_song_release_year = input("Tahun rilis     : ")
    input_song_duration = input("Durasi (contoh 3:45): ")

    new_song_object = Song(
        input_song_id,
        input_song_title,
        input_song_artist,
        input_song_album,
        input_song_genre,
        input_song_release_year,
        input_song_duration,
    )

    # Masuk ke struktur data SLL (ADT List turunan)
    music_library.add_song_to_end(new_song_object)

    # Disimpan permanen ke file CSV
    append_song_to_library_file(new_song_object)

    print("Lagu baru berhasil ditambahkan ke library dan disimpan ke file.\n")


def admin_show_all_songs():
    print("\n=== Daftar Lengkap Lagu di Library ===")
    music_library.print_all_songs()
    print()


def admin_edit_existing_song():
    print("\n=== Ubah Data Lagu di Library ===")
    target_song_id = input("Masukkan ID lagu yang ingin diubah: ")

    target_song_node = music_library.find_song_node_by_id(target_song_id)
    if target_song_node is None:
        print("Lagu dengan ID tersebut tidak ditemukan di library.\n")
        return

    current_song = target_song_node.song_data
    print(f"Data lagu saat ini: {current_song}")

    new_song_title = input(
        f"Judul baru (kosongkan jika tidak diubah) [{current_song.song_title}]: "
    )
    new_song_artist = input(
        f"Artis baru (kosongkan jika tidak diubah) [{current_song.song_artist}]: "
    )
    new_song_album = input(
        f"Album baru (kosongkan jika tidak diubah) [{current_song.song_album}]: "
    )
    new_song_genre = input(
        f"Genre baru (kosongkan jika tidak diubah) [{current_song.song_genre}]: "
    )
    new_song_release_year = input(
        f"Tahun rilis baru (kosongkan jika tidak diubah) "
        f"[{current_song.song_release_year}]: "
    )
    new_song_duration = input(
        f"Durasi baru (kosongkan jika tidak diubah) [{current_song.song_duration}]: "
    )

    if new_song_title:
        current_song.song_title = new_song_title
    if new_song_artist:
        current_song.song_artist = new_song_artist
    if new_song_album:
        current_song.song_album = new_song_album
    if new_song_genre:
        current_song.song_genre = new_song_genre
    if new_song_release_year:
        current_song.song_release_year = new_song_release_year
    if new_song_duration:
        current_song.song_duration = new_song_duration

    save_library_to_file()

    print("Data lagu berhasil diperbarui dan disimpan ke file.\n")


def admin_delete_song_from_library():
    print("\n=== Hapus Lagu dari Library ===")
    target_song_id = input("Masukkan ID lagu yang ingin dihapus: ")

    has_deleted = music_library.delete_song_by_id(target_song_id)
    if has_deleted:
        save_library_to_file()
        print("Lagu berhasil dihapus dari library dan file.\n")
    else:
        print("Lagu dengan ID tersebut tidak ditemukan di library.\n")


def admin_menu():
    while True:
        print("\n=== MENU ADMIN ===")
        print("[1] Tambah lagu ke Library")
        print("[2] Lihat semua lagu di Library")
        print("[3] Ubah data lagu di Library")
        print("[4] Hapus lagu dari Library")
        print("[0] Kembali ke menu utama")
        admin_menu_choice = input("Pilihan menu Admin: ")

        if admin_menu_choice == "1":
            admin_add_new_song()
        elif admin_menu_choice == "2":
            admin_show_all_songs()
        elif admin_menu_choice == "3":
            admin_edit_existing_song()
        elif admin_menu_choice == "4":
            admin_delete_song_from_library()
        elif admin_menu_choice == "0":
            break
        else:
            print("Pilihan menu Admin tidak valid, silakan coba lagi.")
