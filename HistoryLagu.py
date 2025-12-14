class Node:
    def __init__(self, data):
        self.info = data
        self.next = None


class StackList:
    def __init__(self):
        self.top = None

    def isEmpty(self):
        return self.top is None

    def push(self, x):
        newNode = Node(x)
        newNode.next = self.top
        self.top = newNode

    def pop(self):
        if self.isEmpty():
            return None
        item = self.top
        self.top = self.top.next
        return item.info

    def peek(self):
        if self.isEmpty():
            return None
        return self.top.info

    def size(self):
        count = 0
        current = self.top
        while current:
            count += 1
            current = current.next
        return count

    def printStack(self):
        if self.isEmpty():
            print("Stack kosong")
        else:
            print("Isi stack (dari puncak ke dasar):", end=" ")
            current = self.top
            while current:
                print(current.info, end=" ")
                current = current.next
            print()


class SongStack(StackList):
    def push_song_to_stack(self, song_data):
        self.push(song_data)

    def pop_song_from_stack(self):
        return self.pop()

    def is_song_stack_empty(self):
        return self.isEmpty()
