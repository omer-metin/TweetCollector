from collections import OrderedDict


class BufferedQue:

    _buffer_size = None
    _queue_dict = None

    def __init__(self, buffer_size=50):
        self._buffer_size = buffer_size
        self._queue_dict = OrderedDict()

    def add(self, item_id, item):
        if item_id in self._queue_dict:
            return None
        self._queue_dict[item_id] = item
        if len(self._queue_dict) > self._buffer_size:
            return self._queue_dict.pop(list(self._queue_dict.keys())[0])
        return None

    def get(self, item_id):
        return self._queue_dict.get(item_id)

    def contains(self, item_id):
        return item_id in self._queue_dict

    def toList(self):
        return list(self._queue_dict.values())

    def size(self):
        return len(self._queue_dict)

    def __len__(self):
        return len(self._queue_dict)
