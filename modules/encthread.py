from modules.bdgg.bdgg import pack_bdgg

from collections import namedtuple
from os.path import join
from uuid import UUID

from threading import Thread, Event
from queue import Queue

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

encdata = namedtuple("encdata", ("id", "name", "key", "iv"))
encreq = namedtuple("encreq", ("encdata", "callback"))


def smallest_queue(*queues):
    return sorted(queues, key=lambda x: x.queue.qsize())[0]


class Encryptor:
    @classmethod
    def initialize(cls, maxthread, basepath):
        cls.basepath = basepath
        cls.maxthread = maxthread

        cls.threads = []

        for i in range(1, maxthread + 1):
            thread = EncryptorThread(basepath, name=f"encthread_{i}")
            thread.start()
            cls.threads.append(thread)

    @classmethod
    def queue_encryption(cls, id_, name, callback, key=None, iv=None):
        data = encdata(id_, name, key, iv)
        req = encreq(data, callback)

        smallest_queue(*cls.threads).queue.put(req)

    @classmethod
    def cleanup(cls):
        for thread in cls.threads:
            thread.stop()


class EncryptorThread(Thread):
    def __init__(self, basepath, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.basepath = basepath
        self.queue = Queue()

        self.stop_flag = Event()

    def stop(self):
        self.stop_flag.set()

    def run(self):
        while not self.stop_flag.is_set():
            encdata, callback = self.queue.get()
            id_, name, key, iv = encdata

            with open(join(self.basepath, f"__{id_}"), "rb") as f:
                data = f.read()

            encdata, key, iv = self._enc(data, key, iv)

            bdggdata = self._bdgg_encode(id_, name, encdata)

            with open(join(self.basepath, id_), "wb") as f:
                f.write(bdggdata)

            callback(id_, key, iv)

    def _enc(self, data, key=None, iv=None):
        aes_buildargs = {"mode": AES.MODE_CBC, "key": key}
        if key is None:
            aes_buildargs['key'] = key = get_random_bytes(32)
        if iv is not None:
            aes_buildargs['iv'] = iv

        cipher = AES.new(**aes_buildargs)
        data = pad(data, AES.block_size)
        encdata = cipher.encrypt(plaintext=data)

        iv = cipher.iv

        return encdata, key, iv

    def _bdgg_encode(self, id_, name, data, runnable=None, version=0):
        uuid = UUID(id_)
        ext = name.rsplit(".", 1)[-1]

        return pack_bdgg(version, uuid, ext, runnable, data)
