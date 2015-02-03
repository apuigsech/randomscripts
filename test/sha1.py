#!/usr/bin/env python

import math
import hashlib
import struct
import cryptohelper

def block_split(data, blocklen=16):
    return [data[i*blocklen:(i+1)*blocklen] for i in range(int(math.ceil(float(len(data))/blocklen)))]


def block_join(blocks):
    return ''.join(blocks)


# Functions from: https://github.com/ajalt/python-sha1/blob/master/sha1.py
def _left_rotate(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xffffffff

def gh_sha1(message):
    """SHA-1 Hashing Function
    A custom SHA-1 hashing function implemented entirely in Python.
    Arguments:
        message: The input message string to hash.
    Returns:
        A hex SHA-1 digest of the input message.
    """
    # Initialize variables:
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0
    
    # Pre-processing:
    original_byte_len = len(message)
    original_bit_len = original_byte_len * 8
    # append the bit '1' to the message
    message += b'\x80'
    
    # append 0 <= k < 512 bits '0', so that the resulting message length (in bits)
    #    is congruent to 448 (mod 512)
    message += b'\x00' * ((56 - (original_byte_len + 1) % 64) % 64)
    
    # append length of message (before pre-processing), in bits, as 64-bit big-endian integer
    message += struct.pack('>Q', original_bit_len)
    # Process the message in successive 512-bit chunks:
    # break message into 512-bit chunks

    for i in range(0, len(message), 64):
        w = [0] * 80
        # break chunk into sixteen 32-bit big-endian words w[i]
        for j in range(16):
            w[j] = struct.unpack('>I', message[i + j*4:i + j*4 + 4])[0]



        # Extend the sixteen 32-bit words into eighty 32-bit words:
        for j in range(16, 80):
            w[j] = _left_rotate(w[j-3] ^ w[j-8] ^ w[j-14] ^ w[j-16], 1)
 
  
        # Initialize hash value for this chunk:
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4

        for i in range(80):
            if 0 <= i <= 19:
                # Use alternative 1 for f from FIPS PB 180-1 to avoid ~
                f = d ^ (b & (c ^ d))
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d) 
                k = 0x8F1BBCDC
            elif 60 <= i <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6

           # print i, "---", a, b, c, d, e
    
            a, b, c, d, e = ((_left_rotate(a, 5) + f + e + k + w[i]) & 0xffffffff, 
                            a, _left_rotate(b, 30), c, d)

            
        # sAdd this chunk's hash to result so far:
        h0 = (h0 + a) & 0xffffffff
        h1 = (h1 + b) & 0xffffffff 
        h2 = (h2 + c) & 0xffffffff
        h3 = (h3 + d) & 0xffffffff
        h4 = (h4 + e) & 0xffffffff
    
    # Produce the final hash value (big-endian):

    return '%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4)


def sha1_round(block, s):
    block = block[:64]
    chunks = block_split(block, 4)
    w = [struct.unpack('>I', x)[0] for x in chunks] + [0]*64

    for j in range(16, 80):
            w[j] = _left_rotate(w[j-3] ^ w[j-8] ^ w[j-14] ^ w[j-16], 1)

    a, b, c, d, e = s

    for i in range(80):
        if 0 <= i <= 19:
            f = d ^ (b & (c ^ d))
            k = 0x5A827999
        elif 20 <= i <= 39:
            f = b ^ c ^ d
            k = 0x6ED9EBA1
        elif 40 <= i <= 59:
            f = (b & c) | (b & d) | (c & d) 
            k = 0x8F1BBCDC
        elif 60 <= i <= 79:
            f = b ^ c ^ d
            k = 0xCA62C1D6

        a, b, c, d, e = ((_left_rotate(a, 5) + f + e + k + w[i]) & 0xffffffff, a, _left_rotate(b, 30), c, d)

    o = [s[0]+a & 0xffffffff, s[1]+b & 0xffffffff, s[2]+c & 0xffffffff, s[3]+d & 0xffffffff, s[4]+e & 0xffffffff]

    return o


def sha1(m, s=[0x67452301,0xEFCDAB89,0x98BADCFE,0x10325476,0xC3D2E1F0]):
    l = len(m)
    m += '\x80'
    m += '\x00' * ((56-(l+1)%64)%64)
    m += struct.pack('>Q', l*8)

    blocks = block_split(m, 64)

    for b in blocks:
        s = sha1_round(b, s)

    return struct.pack(">IIIII", s[0],s[1],s[2],s[3],s[4])



MSG = "this is a test for sha-1 functions. I hope it works good. Damm, I need It larger than..."
#MSG = MSG[:64]




print gh_sha1(MSG)
print hashlib.sha1(MSG).hexdigest()
print sha1(MSG).encode('hex')
print cryptohelper.sha1(MSG).encode('hex')
