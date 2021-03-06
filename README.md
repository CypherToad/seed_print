# seed_print

> **WARNING** This project has mainly been used for local development, use at your own risk, and always use on an air-gapped machine!

A minimal python script for generating **bip39 seed phrases**, and corresponding [Seed Signer Seed](https://github.com/SeedSigner/seedsigner) seed phrase **qr code** ready for offline printing.

![screenshot](/examples/screenshoot_v1.png)

### Dependencies

The following python project are used, and should be retrieved
before moving to the final air-gapped machine.

```
click==8.0.3
embit==0.4.10
Flask==2.0.2
itsdangerous==2.0.1
Jinja2==3.0.3
MarkupSafe==2.0.1
Pillow==8.4.0
qrcode==7.3.1
Werkzeug==2.0.2
```

### Installation

```
$ cd seed_print/
$ virtualenv -p python3 venv/
$ source venv/bin/activate
$ pip install -r requirements.txt
```

### Usage

```
$ ./main.py
```

If successful you will have a local website available with your
random seed phrases.


> * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

Go ahead and refresh the page to get a new set of addresses!
