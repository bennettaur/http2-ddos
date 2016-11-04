from __future__ import print_function

import sys
import time

from hyperframe.frame import SettingsFrame

from tornado_http2_client import H2Client

from tornado import gen
from tornado.ioloop import IOLoop

__author__ = 'bennettaur'

@gen.coroutine
def test_no_server_push(io_loop, host):
    c = H2Client(io_loop=io_loop)

    yield c.connect(host, 8443)
    print("Disabling Server Push")
    yield c.update_settings({SettingsFrame.ENABLE_PUSH: 0})

    print("Sending request")
    now = time.time()
    response = yield c.get_request("/")
    total_time = c.last_time_data_recvd - now

    print(
        "Pushes Received: {}\nTotal data received: {} bytes\nDuration: {}s\nRate: {} Bps".format(
            len(c.pushes),
            c.data_received_size,
            total_time,
            c.data_received_size/total_time
        )
    )
    c.close_connection()

@gen.coroutine
def test_server_push(io_loop, host):
    c = H2Client(io_loop=io_loop)

    yield c.connect(host, 8443)

    print("Sending request with Server Push")
    now = time.time()
    response = yield c.get_request("/")
    yield gen.sleep(1)

    total_time = c.last_time_data_recvd - now

    print(
        "Pushes Received: {}\nTotal data received: {} bytes\nDuration: {}s\nRate: {} Bps".format(
            len(c.pushes),
            c.data_received_size,
            total_time,
            c.data_received_size/total_time
        )
    )
    #print response
    c.close_connection()


@gen.coroutine
def run_tests(io_loop, host):
    yield test_no_server_push(io_loop=io_loop, host=host)
    yield test_server_push(io_loop=io_loop, host=host)
    io_loop.stop()


host = sys.argv[1]
io_loop = IOLoop.current()

io_loop.add_callback(run_tests, io_loop=io_loop, host=host)

io_loop.start()
