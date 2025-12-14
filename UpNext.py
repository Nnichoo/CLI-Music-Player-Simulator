class Node:
    def __init__(self, data):
        self.info = data
        self.next = None


class QueueList:
    def __init__(self):
        self.front = None
        self.rear = None

    def isEmpty(self):
        return self.front is None

    def enqueue(self, x):
        newNode = Node(x)
        if self.isEmpty():
            self.front = newNode
            self.rear = newNode
        else:
            self.rear.next = newNode
            self.rear = newNode

    def dequeue(self):
        if self.isEmpty():
            return None
        item = self.front
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        return item.info

    def peek(self):
        if self.isEmpty():
            return None
        return self.front.info

    def size(self):
        count = 0
        current = self.front
        while current:
            count += 1
            current = current.next
        return count

    def printQueue(self):
        if self.isEmpty():
            print("Queue kosong")
        else:
            print("Isi queue (dari front ke rear):", end=" ")
            current = self.front
            while current:
                print(current.info, end=" ")
                current = current.next
            print()


class SongQueue(QueueList):
    def enqueue_song(self, song_data):
        self.enqueue(song_data)

    def dequeue_song(self):
        return self.dequeue()

    def is_song_queue_empty(self):
        return self.isEmpty()

    def show_all_songs_in_queue(self):
        if self.isEmpty():
            print("Antrian Up Next masih kosong.")
            return
        print("Daftar lagu di antrian Up Next:")
        current = self.front
        i = 1
        while current:
            print(f"{i}. {current.info}")
            current = current.next
            i += 1

    def remove_first_song_without_playing(self):
        return self.dequeue()

    def clear_queue(self):
        self.front = None
        self.rear = None
