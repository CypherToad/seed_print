# seed_print

> **WARNING** This project has mainly been used for local development, use at your own risk, and always use on an air-gapped machine!

A minimal python script for generating **bip39 seed phrases**, and corresponding [Seed Signer Seed](https://github.com/SeedSigner/seedsigner) seed phrase **qr code**. Ready for offline printing.

![screenshot](/examples/example1.png)
![screenshot](/examples/example2.png)

### Dependencies

The following python libraries are used, and should be retrieved
before moving to the final air-gapped machine.

```
click==8.0.3
embit==0.4.10
qrcode==7.3.1
```

### Installation (pre-airgap)

```
$ cd seed_print/
$ virtualenv -p python3 venv/
$ source venv/bin/activate
$ pip install -r requirements.txt
```

### Usage (post-airgap)

Disconnect the machine from the internet forever, or until the machine has been formatted.

```
$ ./main.py
```
