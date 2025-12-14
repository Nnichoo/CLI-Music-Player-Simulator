# main.py
# Entry point YouTube Music CLI

from SongLibrary import load_song_library_from_file
from admin import admin_menu
from user import user_menu


def main_menu():
    while True:
        print("=================================")
        print("       YOUTUBE MUSIC CLI         ")
        print("=================================")
        print("[1] Login sebagai Admin")
        print("[2] Masuk sebagai User")
        print("[0] Keluar")
        pilihan = input("Pilihan: ")

        if pilihan == "1":
            admin_menu()
        elif pilihan == "2":
            user_menu()
        elif pilihan == "0":
            print("Terima kasih, program selesai.")
            break
        else:
            print("Pilihan tidak valid, silakan coba lagi.")


if __name__ == "__main__":
    # load semua lagu dari file CSV ke linked list
    load_song_library_from_file()
    # jalankan menu utama
    main_menu()
