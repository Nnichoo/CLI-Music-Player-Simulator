import csv
import os

SONG_LIBRARY_FILE_PATH = "songLibrary.csv"


class Song:
    def __init__(
        self,
        song_id,
        song_title,
        song_artist,
        song_album,
        song_genre,
        song_release_year,
        song_duration,
    ):
        self.song_id = song_id
        self.song_title = song_title
        self.song_artist = song_artist
        self.song_album = song_album
        self.song_genre = song_genre
        self.song_release_year = song_release_year
        self.song_duration = song_duration
        self.song_play_count = 0
        self.is_favorite_song = False

    def __str__(self):
        return (
            f"[{self.song_id}] {self.song_title} - "
            f"{self.song_artist} ({self.song_genre}, {self.song_release_year})"
        )


class Node:
    def __init__(self, data):
        self.info = data
        self.next = None

    @property
    def song_data(self):
        return self.info

    @property
    def next_node(self):
        return self.next

    @next_node.setter
    def next_node(self, value):
        self.next = value


class List:
    def __init__(self):
        self.first = None

    def createList(self):
        self.first = None

    def createElement(self, x):
        return Node(x)

    def insertFirst(self, P):
        if P:
            P.next = self.first
            self.first = P

    def insertLast(self, P):
        if P:
            if not self.first:
                self.first = P
            else:
                last = self.first
                while last.next:
                    last = last.next
                last.next = P

    def printList(self):
        if not self.first:
            print("List kosong")
        else:
            current = self.first
            while current:
                print(current.info, end=" ")
                current = current.next
            print()

    def deleteFirst(self):
        if self.first:
            P = self.first
            self.first = P.next
            return P
        return None

    def deleteLast(self):
        if not self.first:
            return None
        if not self.first.next:
            P = self.first
            self.first = None
            return P
        current = self.first
        while current.next.next:
            current = current.next
        P = current.next
        current.next = None
        return P

    def searchInfo(self, x):
        current = self.first
        while current and current.info != x:
            current = current.next
        return current


class SongLinkedList(List):
    def __init__(self):
        super().__init__()

    @property
    def head_node(self):
        return self.first

    def add_song_to_end(self, new_song: Song):
        P = self.createElement(new_song)
        self.insertLast(P)

    def print_all_songs(self):
        if not self.first:
            print("Library lagu masih kosong.")
            return

        current = self.first
        while current is not None:
            print(current.info)
            current = current.next

    def find_song_node_by_id(self, target_song_id: str):
        current = self.first
        while current is not None:
            if current.info.song_id == target_song_id:
                return current
            current = current.next
        return None

    def delete_song_by_id(self, target_song_id: str):
        if not self.first:
            return False

        if self.first.info.song_id == target_song_id:
            self.first = self.first.next
            return True

        prev = self.first
        current = self.first.next
        while current is not None:
            if current.info.song_id == target_song_id:
                prev.next = current.next
                return True
            prev = current
            current = current.next

        return False

    def find_song_node_by_title(self, target_song_title: str):
        if not self.first:
            return None

        target_lower = target_song_title.lower()
        current = self.first
        while current is not None:
            if target_lower in current.info.song_title.lower():
                return current
            current = current.next
        return None


music_library = SongLinkedList()


def initialize_song_library_file_if_not_exists():
    if not os.path.exists(SONG_LIBRARY_FILE_PATH):
        with open(SONG_LIBRARY_FILE_PATH, mode="w", encoding="utf-8", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["id", "title", "artist", "album", "genre", "year", "duration"])


def load_song_library_from_file():
    initialize_song_library_file_if_not_exists()

    with open(SONG_LIBRARY_FILE_PATH, mode="r", encoding="utf-8", newline="") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        loaded_song_count = 0
        for row in csv_reader:
            song_id = row.get("id", "").strip()
            song_title = row.get("title", "").strip()
            song_artist = row.get("artist", "").strip()
            song_album = row.get("album", "").strip()
            song_genre = row.get("genre", "").strip()
            song_release_year = row.get("year", "").strip()
            song_duration = row.get("duration", "").strip()

            if not song_id or not song_title:
                continue

            new_song_object = Song(
                song_id,
                song_title,
                song_artist,
                song_album,
                song_genre,
                song_release_year,
                song_duration,
            )

            music_library.add_song_to_end(new_song_object)
            loaded_song_count += 1

    print(f"Berhasil memuat {loaded_song_count} lagu dari '{SONG_LIBRARY_FILE_PATH}'.")


def append_song_to_library_file(song: Song):
    initialize_song_library_file_if_not_exists()

    with open(SONG_LIBRARY_FILE_PATH, mode="a", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([
            song.song_id,
            song.song_title,
            song.song_artist,
            song.song_album,
            song.song_genre,
            song.song_release_year,
            song.song_duration,
        ])


def save_library_to_file():
    initialize_song_library_file_if_not_exists()

    with open(SONG_LIBRARY_FILE_PATH, mode="w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["id", "title", "artist", "album", "genre", "year", "duration"])

        current_node = music_library.first
        while current_node is not None:
            song = current_node.info
            writer.writerow([
                song.song_id,
                song.song_title,
                song.song_artist,
                song.song_album,
                song.song_genre,
                song.song_release_year,
                song.song_duration,
            ])
            current_node = current_node.next


def get_all_songs_from_library_as_list():
    songs = []
    current_node = music_library.first
    while current_node is not None:
        songs.append(current_node.info)
        current_node = current_node.next
    return songs
