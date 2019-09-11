"""Generates 'keep-alive' websocket connections to emulate n viewers on https://micerace.com"""

import time
import ssl
from multiprocessing import Pool

from retry import retry
from websocket import create_connection

NUM_FAKE_VIEWERS = 1000

WEBSOCKET_CONN_URI = 'wss://micerace.com/socket.io/?EIO=3&transport=websocket'
SSLOPT = {'cert_reqs': ssl.CERT_NONE}


@retry(Exception, tries=4, delay=1, backoff=1, jitter=1)
def process_message(_):
    conn = create_connection(WEBSOCKET_CONN_URI, sslopt=SSLOPT)
    conn.recv()
    conn.send(f'40/chat,')
    conn.send(f'40/user,')
    v = conn.recv()
    while '42/user' not in v:
        v = conn.recv()
    else:
        conn.send(f'42/user,')
    while True:
        send_ping(conn)
        time.sleep(20)


def send_ping(conn):
    conn.send('2')
    conn.recv()


def main():
    pool = Pool(NUM_FAKE_VIEWERS)
    for _ in enumerate(pool.imap_unordered(process_message, range(NUM_FAKE_VIEWERS))):
        pass


if __name__ == '__main__':
    main()
