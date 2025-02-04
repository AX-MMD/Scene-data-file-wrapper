class InfiniteIterator:
    def __init__(self, data):
        self.data = data
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if not self.data:
            raise StopIteration("The data list is empty.")
        value = self.data[self.index]
        self.index = (self.index + 1) % len(self.data)
        return value
