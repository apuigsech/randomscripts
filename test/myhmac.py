#!/usr/bin/env python

from cryptohelper import *
import hmac

def HMAC(m, k, blocklen, hf, ipad=0x36, opad=0x5c):
	ipad_key = strxor(chr(ipad) * blocklen, k)
	opad_key = strxor(chr(opad) * blocklen, k)
	return hf(opad_key + hf(ipad_key + m))

def hmac_sha1(m, k):
    from hashlib import sha1
    import hmac

    hashed = hmac.new(k, m, sha1)

    return hashed.digest()

 
MSG="A"*64

print HMAC(MSG, "\x01"*64, 64, sha1).encode('hex')
print hmac_sha1(MSG, "\x01"*64).encode('hex')