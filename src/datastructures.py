class Queue:
    def __init__(self):
        self._queue = [{
            "name":"hello",
            "phone": '+19543090566'
            }]
        # depending on the _mode, the queue has to behave like a FIFO or LIFO
        self._mode = 'FIFO'

    def enqueue(self, item):
        self._queue.insert(0, item)
    def dequeue(self):
        return self._queue.pop()
    def get_queue(self):
        return self._queue
    def size(self):
        return len(self._queue) 