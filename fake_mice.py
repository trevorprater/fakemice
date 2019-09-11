"""Generates 'keep-alive' websocket connections to emulate n viewers on https://micerace.com"""

import time
import ssl
from multiprocessing import Pool

from retry import retry
from websocket import create_connection

NUM_FAKE_VIEWERS = 1000

WEBSOCKET_CONN_URI = 'wss://micerace.com/socket.io/?EIO=3&transport=websocket'
SSL_OPT = {'cert_reqs': ssl.CERT_NONE}


@retry(Exception, tries=2, delay=2, backoff=1, jitter=1)
def process_message(_):
    conn = create_connection(WEBSOCKET_CONN_URI, sslopt=SSL_OPT)
    conn.recv()
    conn.send('40/chat,')
    conn.send('40/user,')

    while '42/user' not in conn.recv():
        pass
    else:
        conn.send('42/user,')
    while True:
        conn.send('2')
        conn.recv()
        time.sleep(20)


def main():
    for _ in Pool(NUM_FAKE_VIEWERS).imap_unordered(process_message, range(NUM_FAKE_VIEWERS)):
        pass


if __name__ == '__main__':
    main()
