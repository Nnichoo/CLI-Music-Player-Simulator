class Node:
    def __init__(self, data):
        self.info = data
        self.next = None
        self.prev = None

    @property
    def song_data(self):
        return self.info

    @property
    def next_song_node(self):
        return self.next

    @next_song_node.setter
    def next_song_node(self, value):
        self.next = value

    @property
    def previous_song_node(self):
        return self.prev

    @previous_song_node.setter
    def previous_song_node(self, value):
        self.prev = value


class List:
    def __init__(self):
        self.first = None
        self.last = None

    def createList(self):
        self.first = None
        self.last = None

    def createElement(self, x):
        return Node(x)

    def insertFirst(self, P):
        if P:
            P.next = self.first
            P.prev = None
            if self.first:
                self.first.prev = P
            else:
                self.last = P
            self.first = P

    def insertLast(self, P):
        if P:
            P.prev = self.last
            P.next = None
            if self.last:
                self.last.next = P
            else:
                self.first = P
            self.last = P

    def deleteFirst(self):
        if self.first:
            P = self.first
            self.first = P.next
            if self.first:
                self.first.prev = None
            else:
                self.last = None
            return P
        return None

    def deleteLast(self):
        if self.last:
            P = self.last
            self.last = P.prev
            if self.last:
                self.last.next = None
            else:
                self.first = None
            return P
        return None

    def searchInfo(self, x):
        current = self.first
        while current and current.info != x:
            current = current.next
        return current

    def printList(self):
        if not self.first:
            print("List kosong")
        else:
            current = self.first
            while current:
                print(current.info, end=" ")
                current = current.next
            print()

    def printListReverse(self):
        if not self.last:
            print("List kosong")
        else:
            current = self.last
            while current:
                print(current.info, end=" ")
                current = current.prev
            print()


class PlaylistDoublyLinkedList(List):
    def __init__(self, playlist_name):
        super().__init__()
        self.playlist_name = playlist_name

    def add_song_to_playlist_end(self, song_data):
        P = self.createElement(song_data)
        self.insertLast(P)

    def print_all_songs_in_playlist(self):
        if not self.first:
            print(f"Playlist '{self.playlist_name}' masih kosong.")
            return
        current = self.first
        i = 1
        while current:
            print(f"{i}. {current.info}")
            current = current.next
            i += 1

    def find_song_node_in_playlist_by_id(self, target_song_id: str):
        current = self.first
        while current:
            if current.info.song_id == target_song_id:
                return current
            current = current.next
        return None

    def remove_song_from_playlist_by_id(self, target_song_id: str):
        current = self.first
        while current:
            if current.info.song_id == target_song_id:
                if current == self.first:
                    self.deleteFirst()
                elif current == self.last:
                    self.deleteLast()
                else:
                    prev_node = current.prev
                    next_node = current.next
                    prev_node.next = next_node
                    if next_node:
                        next_node.prev = prev_node
                return True
            current = current.next
        return False
