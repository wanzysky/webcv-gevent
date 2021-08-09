import socket
import base64
import cv2
import numpy as np
from collections import OrderedDict

from .server import get_server


def jpeg_encode(img):
    return cv2.imencode('.png', img)[1]


def get_free_port(rng, low=2000, high=10000):
    in_use = True
    while in_use:
        port = rng.randint(high - low) + low
        in_use = False
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind(("0.0.0.0", port))
        except socket.error as e:
            if e.errno == 98:  # port already in use
                in_use = True
        s.close()
    return port


class Manager:
    def __init__(self, img_encode_method=jpeg_encode, rng=None):
        self._queue = OrderedDict()
        self._server = None
        self.img_encode_method = img_encode_method
        if rng is None:
            rng = np.random.RandomState(self.get_default_seed())
        self.rng = rng

    def get_default_seed(self):
        return 0

    def imshow(self, title, img):
        data = self.img_encode_method(img)
        data = base64.b64encode(data)
        data = data.decode('utf8')
        self._queue[title] = {
            "dtype": "image", "caption": title, "content": data}

    @property
    def conn(self):
        if self._server is None:
            self.port = get_free_port(self.rng)
            self._server, self._conn = get_server(port=self.port)
        return self._conn

    def table_show(self, title, table):
        self._queue[title] = {
                "dtype": "table", "caption": title, "content": table}

    def head_show(self, title, head):
        self._queue[title] = {"dtype": "header", "content": head}

    def send(self, delay=0):
        self.conn.send([delay, list(self._queue.values())])
        self._queue = OrderedDict()
        return True

    def waitKey(self, delay=0):
        self.conn.send([delay, list(self._queue.values())])
        self._queue = OrderedDict()
        return self.conn.recv()

global_manager = Manager()
