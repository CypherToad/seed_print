#!/usr/bin/env python3

# Built in python libraries
import json
import base64
from io import BytesIO
from hashlib import sha256

# Trusting Trezor's for randopm wallet creations
from mnemonic import Mnemonic

# Thanks @KeithMukai for the suggestion!
# https://twitter.com/KeithMukai/status/1470571942000443392
# Confirm we are offline
import requests

# Trusting qrcode library as offline qr code creation
import qrcode

# Trusting Flask as simple web interface which can be easily printed or stored as pdf
from flask import Flask, render_template, request


app = Flask(__name__)
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


def seed_qr_base64(words):
    """
    Return a base64 PNG encoding of our seed_qr.
    """

    # create a qrcode of our seed_qr_string
    img = qrcode.make(
        seed_qr_string(words))

    # generate a
    # https://jdhao.github.io/2020/03/17/base64_opencv_pil_image_conversion/
    im_file = BytesIO()
    img.save(im_file, format="PNG")
    im_b64 = base64.b64encode(im_file.getvalue())

    return im_b64.decode()


@app.route("/")
def home():
    """
    Main home page which generates random wallets
    """

    # generate a strong wallet
    words = mnemo.generate(strength=256)
    qr_string = seed_qr_string(words)

    # Thanks for the suggestion @KeithMukai
    # https://twitter.com/KeithMukai/status/1470571942000443392
    if requests.get('http://bitcoin.org'):
        return render_template('panic.html')

    return render_template(
        'index.html', words=words, seed_qr=seed_qr_base64(words),
        qr_string=qr_string)


if __name__ == "__main__":
    app.run(debug=True)
