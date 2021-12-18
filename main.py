#!/usr/bin/env python3

import json
import base64
import random
from io import BytesIO
import socket
from binascii import unhexlify, hexlify

# Trusting SeedSigner's embit library
# https://github.com/SeedSigner/embit
from embit import bip32
from embit import bip39
from embit import wordlists
from embit import script
from embit.networks import NETWORKS

# Trusting qrcode library as offline qr code creation
import qrcode

# Trusting Flask as simple web interface
from flask import Flask, render_template, request


app = Flask(__name__)
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
    Return the string value of our SeedQR.
    """

    return ''.join([str(wordlist.index(w)).zfill(4) for w in words.split()])


def seed_qr_base64(words):
    """
    Return a base64 PNG image of our SeedQR.
    """

    # create a qrcode of our seed_qr_string
    img = qrcode.make(
        seed_qr_string(words))

    # generate a base64 encoding of our png image
    # https://jdhao.github.io/2020/03/17/base64_opencv_pil_image_conversion/
    im_file = BytesIO()
    img.save(im_file, format="PNG")
    im_b64 = base64.b64encode(im_file.getvalue())

    return im_b64.decode()


def get_seed_phrase(entropy):
    """
    Generate random seedphrase
    """

    words = bip39.mnemonic_from_bytes(entropy)
    return words


@app.route("/")
def home():
    """
    Main home page which generates random seed phrases
    """

    if is_online():
        return render_template('panic.html')

    params = {}

    # generate a random seed phrase
    params['entropy'] = random.randbytes(32)

    # seedQR our our entropy
    params['words'] = get_seed_phrase(params['entropy'])
    params['seed_qr_string'] = seed_qr_string(params['words'])
    params['seed_qr_base64'] = seed_qr_base64(params['words'])

    params['seed'] = bip39.mnemonic_to_seed(params['words'])

    params['derivation_path'] = "m/84'/0'/0'"

    version = bip32.detect_version(params['derivation_path'], default="xpub",  network=NETWORKS['main'])
    root = bip32.HDKey.from_seed(params['seed'], NETWORKS['main']['xprv'])

    params['fingerprint'] = hexlify(root.child(0).fingerprint).decode()

    xpriv = root.derive(params['derivation_path'])
    xpub = xpriv.to_public()

    params['xpriv'] = xpriv
    params['xpub'] = xpub.to_string(version=version)



    return render_template('index.html', **params, wordlist=wordlist)


if __name__ == "__main__":
    app.run(debug=True)
