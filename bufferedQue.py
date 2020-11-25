from collections import OrderedDict


class BufferedQue:
    """
    A Queue type that can be buffered. After buffer is full, on adding 
    operations returns oldest object in queue. Works with unique key 
    by using <key, item>
    """

    _buffer_size = None
    _queue_dict = None

    def __init__(self, buffer_size=50):
        """
        Args:
            buffer_size (int): size of buffer (default: 50)
        """
        self._buffer_size = buffer_size
        self._queue_dict = OrderedDict()

    def add(self, item_id, item):
        """
        Adds an item with its id as <key, item> pair. If buffer is full 
        returns oldest item in the buffer.

        Args:
            item_id (object): key of item
            item (object): item itself

        Returns:
            object - oldest item if buffer is full else None
        """
        if item_id in self._queue_dict:
            return None
        self._queue_dict[item_id] = item
        if len(self._queue_dict) > self._buffer_size:
            return self._queue_dict.pop(list(self._queue_dict.keys())[0])
        return None

    def get(self, item_id):
        """Returns item that matches the given id"""
        return self._queue_dict.get(item_id)

    def contains(self, item_id):
        """Returns true if given item_id is in key list"""
        return item_id in self._queue_dict

    def toList(self):
        """Returns all items(without keys) as a list"""
        return list(self._queue_dict.values())

    def size(self):
        """Returns how much element is in queue"""
        return len(self._queue_dict)

    def __len__(self):
        """Returns how much element is in queue"""
        return len(self._queue_dict)
