#!/usr/bin/env python3

import os
import random
import socket

import qrcode
import click
from embit import bip32
from embit import bip39
from embit import wordlists

wordlist = wordlists.bip39.WORDLIST


def is_online():
    """
    Check if we are online

    Thanks @KeithMukai for the suggestion!
    https://twitter.com/KeithMukai/status/1470571942000443392
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(('1.1.1.1', 53))
        return True
    except OSError:
        return False


def seed_qr_string(words):
    """
    Return a string representation of our words for seed_signer
    """

    return ''.join([str(wordlist.index(w)).zfill(4) for w in words.split()])


@click.command()
def main():
    """
    Generates a seed phrase
    """

    # if is_online():
    #     raise Exception('You should not be connected to the internet!')

    # generate a strong wallet
    entropy = random.randbytes(32)
    words = bip39.mnemonic_from_bytes(entropy)
    qr_string = seed_qr_string(words)

    print(words)

    # Thanks @simulx
    # https://twitter.com/simulx/status/1470894394232516608
    os.system('qr --ascii "%s"' % qr_string)


if __name__ == '__main__':
    main()
