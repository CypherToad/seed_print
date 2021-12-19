#!/usr/bin/env python3

import os
import random
import socket
from binascii import unhexlify, hexlify

import click
import qrcode

# SeedSigner embit library
# A minimal bitcoin library for MicroPython and Python3 with a focus on embedded systems
from embit import bip32
from embit import bip39
from embit import script
from embit import wordlists
from embit.networks import NETWORKS
from embit.ec import PublicKey


NETWORK = NETWORKS['main']


class SeedPhrase(object):

    def __init__(self, words=None, entropy=b'', derivation_path="m/84'/0'/0'"):
        """
        class constructor
        """

        # Generate or set word list
        self.entropy = unhexlify(entropy)
        if not words:
            if not entropy:
                self.entropy = random.randbytes(32)
            self.words = bip39.mnemonic_from_bytes(self.entropy)
        else:
            self.words = words

        self.wordlist = wordlists.bip39.WORDLIST

        self.network = NETWORKS['main']
        self.derivation_path = derivation_path

    @property
    def seed(self):
        """
        Return seed
        """

        return bip39.mnemonic_to_seed(self.words)

    @property
    def root(self):
        """
        Return root
        """

        return bip32.HDKey.from_seed(self.seed)

    @property
    def fingerprint(self):
        """
        Return fingerprint
        """

        return self.root.child(0).fingerprint

    @property
    def xpriv(self):
        """
        Return xpriv
        """

        return self.root.derive(self.derivation_path)

    @property
    def xpub(self):
        """
        Return xpub
        """

        return self.xpriv.to_public()

    @property
    def seed_qr(self):
        """
        Return a string representation our seedqr
        """

        # make a list of wordlist position for our words
        pos = [str(self.wordlist.index(w)).zfill(4) for w in self.words.split()]

        # return list as a single string
        return ''.join(pos)


def is_online():
    """
    Check if we are online by connecting to cloudflare dns servers.
    Thanks @KeithMukai for the suggestion!
    https://twitter.com/KeithMukai/status/1470571942000443392
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(('1.1.1.1', 53))
        return True
    except OSError:
        return False


@click.command()
def main():
    """
    Generates a seed phrase
    """

    if is_online():
        raise Exception('You should not be connected to the internet!')

    # generate a strong wallet
    seedphrase = SeedPhrase()

    print()
    print('entropy: %s' % hexlify(seedphrase.entropy).decode())
    print('seed: %s' % hexlify(seedphrase.seed).decode())

    # print out seed phrase in columns
    print()
    print('seed phrase:\n')
    c = 0
    for n, _word in enumerate(seedphrase.words.split(), 1):
        word = '%s: %s' % (str(n).rjust(2), _word)
        print(word.ljust(25), end='')
        c += 1
        # new line and reset count
        if c >= 4:
            print()
            c = 0

    # Thanks @simulx
    # https://twitter.com/simulx/status/1470894394232516608
    os.system('qr --ascii "%s"' % seedphrase.seed_qr)
    print('seed QR: %s' % seedphrase.seed_qr)
    print('-' * 120)

    print()
    print('fingerprint: %s' % hexlify(seedphrase.fingerprint).decode())
    print('derivation_path: %s' % seedphrase.derivation_path)
    print('xpriv: %s' % seedphrase.xpriv)
    print('xpub: %s' % seedphrase.xpub)
    os.system('qr --ascii "%s"' % seedphrase.xpub)
    print()

    # print out a couple addresses using this key
    print('Adresses:')
    for i in range(10):
        print(script.p2wpkh(seedphrase.xpub.derive('0/%s' % i).get_public_key()).address())

    print()


if __name__ == '__main__':
    main()
