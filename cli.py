#!/usr/bin/env python3

import os
import json
from hashlib import sha256

from mnemonic import Mnemonic
import qrcode
import click

mnemo = Mnemonic("english")


# load our words.txt which was fetched from Trezor's github
# https://github.com/trezor/python-mnemonic/blob/master/src/mnemonic/wordlist/english.txt
with open('words.txt') as f:
    wordlist = [ i for i in f.read().split('\n') if i ]

# confirm we have our 2048 words
if len(wordlist) != 2048:
    raise Exception("Word list is not correct length: %s" % len(wordlist))

# confirm our checksum matches
checksum = sha256(json.dumps(wordlist).encode()).hexdigest()
if checksum != '9944a25d756463cef4038bd1b5e312932ec874f0236be654a977fa7cc49fb03a':
    raise Exception("Checksum mistmatch!")

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

    # generate a strong wallet
    words = mnemo.generate(strength=256)
    qr_string = seed_qr_string(words)

    # Thanks for the suggestion @KeithMukai
    # https://twitter.com/KeithMukai/status/1470571942000443392
    try:
        if requests.get('http://bitcoin.org'):
            return render_template('panic.html')
    except:
        pass

    print(words)
    print(qr_string)

    # Thanks @simulx
    # https://twitter.com/simulx/status/1470894394232516608
    os.system('qr --ascii "%s" % qr_string')


if __name__ == '__main__':
    main()
