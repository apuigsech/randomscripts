#!/usr/bin/env python

import math
import hashlib
from binascii import hexlify
import struct

def block_split(data, blocklen=16):
    return [data[i*blocklen:(i+1)*blocklen] for i in range(int(math.ceil(float(len(data))/blocklen)))]


def block_join(blocks):
    return ''.join(blocks)



def md4_pad(m, l=None):
	if l == None:
		l = len(m)
	m += '\x80'
	m += '\x00' * ((56-(l+1)%64)%64)
	m += struct.pack('<Q', l*8)
	return m


def make_words(byte_array):
    res = []
    for i in xrange(0, len(byte_array), 4):
        index = i/4
        res.append(byte_array[i+3])
        res[index] = (res[index] << 8) | byte_array[i+2]
        res[index] = (res[index] << 8) | byte_array[i+1]
        res[index] = (res[index] << 8) | byte_array[i]
    return res


# Functions from: https://github.com/ajalt/python-sha1/blob/master/sha1.py
def _left_rotate(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xffffffff

def gh_md4(message):
    """
    https://tools.ietf.org/html/rfc1320
    """
    # we'll need to remember this for later
    original_length = len(message)

    message = [ord(c) for c in message]

    # add a '1' bit via a byte
    message += [0x80]


    mod_length = len(message) % 64
    # padding to 448 % 512 bits (56 % 64 byte)
    if mod_length < 56:
        message += [0x00] * (56 - mod_length)
    else:
        message += [0x00] * (120 - mod_length)

    # add the length as a 64 bit big endian, use lower order bits if length overflows 2^64
    length = [ord(c) for c in struct.pack('>Q', (original_length * 8) & 0xFFFFFFFFFFFFFFFF)]

    # add the two words least significant first
    message.extend(length[::-1])

    # initialize the registers to magic values
    A = 0x67452301
    B = 0xefcdab89
    C = 0x98badcfe
    D = 0x10325476

    # define F, G, and H
    def F(x,y,z): return ((x & y) | ((~x) & z))
    def G(x,y,z): return (x & y) | (x & z) | (y & z)
    def H(x,y,z): return x ^ y ^ z

    # round functions
    def FF(a,b,c,d,k,s): return ROL((a + F(b,c,d) + X[k]) & 0xFFFFFFFF, s)
    def GG(a,b,c,d,k,s): return ROL((a + G(b,c,d) + X[k] + 0x5A827999) & 0xFFFFFFFF, s)
    def HH(a,b,c,d,k,s): return ROL((a + H(b,c,d) + X[k] + 0x6ED9EBA1) & 0xFFFFFFFF, s)

    # define a 32-bit left-rotate function (<<< in the RFC)
    def ROL(x, n): return ((x << n) & 0xFFFFFFFF) | (x >> (32-n))

    # turn the padded message into a list of 32-bit words
    M = make_words(message)
        
    # process each 16 word (64 byte) block
    for i in xrange(0, len(M), 16):

        X = M[i:i+16]

        # save the current values of the registers
        AA = A
        BB = B
        CC = C
        DD = D

        # round 1

        # perform the 16 operations
        A = FF(A,B,C,D,0,3)
        D = FF(D,A,B,C,1,7)
        C = FF(C,D,A,B,2,11)
        B = FF(B,C,D,A,3,19)

       # print 1.1,[A,B,C,D]

        A = FF(A,B,C,D,4,3)
        D = FF(D,A,B,C,5,7)
        C = FF(C,D,A,B,6,11)
        B = FF(B,C,D,A,7,19)

        A = FF(A,B,C,D,8,3)
        D = FF(D,A,B,C,9,7)
        C = FF(C,D,A,B,10,11)
        B = FF(B,C,D,A,11,19)

        A = FF(A,B,C,D,12,3)
        D = FF(D,A,B,C,13,7)
        C = FF(C,D,A,B,14,11)
        B = FF(B,C,D,A,15,19)

        # round 2
      #  print 2,[A,B,C,D]

        # perform the 16 operations
        A = GG(A,B,C,D,0,3)
        D = GG(D,A,B,C,4,5)
        C = GG(C,D,A,B,8,9)
        B = GG(B,C,D,A,12,13)

        A = GG(A,B,C,D,1,3)
        D = GG(D,A,B,C,5,5)
        C = GG(C,D,A,B,9,9)
        B = GG(B,C,D,A,13,13)

        A = GG(A,B,C,D,2,3)
        D = GG(D,A,B,C,6,5)
        C = GG(C,D,A,B,10,9)
        B = GG(B,C,D,A,14,13)

        A = GG(A,B,C,D,3,3)
        D = GG(D,A,B,C,7,5)
        C = GG(C,D,A,B,11,9)
        B = GG(B,C,D,A,15,13)

      #  print 3,[A,B,C,D]
        # round 3

        A = HH(A,B,C,D,0,3)
        D = HH(D,A,B,C,8,9)
        C = HH(C,D,A,B,4,11)
        B = HH(B,C,D,A,12,15)

        A = HH(A,B,C,D,2,3)
        D = HH(D,A,B,C,10,9)
        C = HH(C,D,A,B,6,11)
        B = HH(B,C,D,A,14,15)

        A = HH(A,B,C,D,1,3)
        D = HH(D,A,B,C,9,9)
        C = HH(C,D,A,B,5,11)
        B = HH(B,C,D,A,13,15)

        A = HH(A,B,C,D,3,3)
        D = HH(D,A,B,C,11,9)
        C = HH(C,D,A,B,7,11)
        B = HH(B,C,D,A,15,15)

     #   print 4,[A,B,C,D]

        # increment by previous values
        A =  ((A + AA) & 0xFFFFFFFF)
        B =  ((B + BB) & 0xFFFFFFFF)
        C =  ((C + CC) & 0xFFFFFFFF)
        D =  ((D + DD) & 0xFFFFFFFF)


    # convert endian-ness for output
    A = hexlify(struct.pack('<L', A))
    B = hexlify(struct.pack('<L', B))
    C = hexlify(struct.pack('<L', C))
    D = hexlify(struct.pack('<L', D))

    return A + B + C + D



def md4(m, s=[0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476], pad=True):
    if pad == True:
        m = md4_pad(m)

	blocks = block_split(m, 64)

	for b in blocks:
		s = md4_round(b, s)

	return struct.pack("<IIII", s[0],s[1],s[2],s[3])



def md4_round(block, s):
    block = block[:64]
    chunks = block_split(block, 4)
    w = [struct.unpack('<I', x)[0] for x in chunks]

    a, b, c, d = s

    def F(x,y,z): return ((x & y) | ((~x) & z))
    def G(x,y,z): return (x & y) | (x & z) | (y & z)
    def H(x,y,z): return x ^ y ^ z

    def FF(a,b,c,d,k,n): return _left_rotate((a + F(b,c,d) + w[k]) & 0xFFFFFFFF, n)
    def GG(a,b,c,d,k,n): return _left_rotate((a + G(b,c,d) + w[k] + 0x5A827999) & 0xFFFFFFFF, n)
    def HH(a,b,c,d,k,n): return _left_rotate((a + H(b,c,d) + w[k]+ 0x6ED9EBA1) & 0xFFFFFFFF, n)


    a = FF(a,b,c,d,0,3)
    d = FF(d,a,b,c,1,7)
    c = FF(c,d,a,b,2,11)
    b = FF(b,c,d,a,3,19)

    a = FF(a,b,c,d,4,3)
    d = FF(d,a,b,c,5,7)
    c = FF(c,d,a,b,6,11)
    b = FF(b,c,d,a,7,19)

    a = FF(a,b,c,d,8,3)
    d = FF(d,a,b,c,9,7)
    c = FF(c,d,a,b,10,11)
    b = FF(b,c,d,a,11,19)

    a = FF(a,b,c,d,12,3)
    d = FF(d,a,b,c,13,7)
    c = FF(c,d,a,b,14,11)
    b = FF(b,c,d,a,15,19)

    a = GG(a,b,c,d,0,3)
    d = GG(d,a,b,c,4,5)
    c = GG(c,d,a,b,8,9)
    b = GG(b,c,d,a,12,13)

    a = GG(a,b,c,d,1,3)
    d = GG(d,a,b,c,5,5)
    c = GG(c,d,a,b,9,9)
    b = GG(b,c,d,a,13,13)

    a = GG(a,b,c,d,2,3)
    d = GG(d,a,b,c,6,5)
    c = GG(c,d,a,b,10,9)
    b = GG(b,c,d,a,14,13)

    a = GG(a,b,c,d,3,3)
    d = GG(d,a,b,c,7,5)
    c = GG(c,d,a,b,11,9)
    b = GG(b,c,d,a,15,13)

    a = HH(a,b,c,d,0,3)
    d = HH(d,a,b,c,8,9)
    c = HH(c,d,a,b,4,11)
    b = HH(b,c,d,a,12,15)

    a = HH(a,b,c,d,2,3)
    d = HH(d,a,b,c,10,9)
    c = HH(c,d,a,b,6,11)
    b = HH(b,c,d,a,14,15)

    a = HH(a,b,c,d,1,3)
    d = HH(d,a,b,c,9,9)
    c = HH(c,d,a,b,5,11)
    b = HH(b,c,d,a,13,15)

    a = HH(a,b,c,d,3,3)
    d = HH(d,a,b,c,11,9)
    c = HH(c,d,a,b,7,11)
    b = HH(b,c,d,a,15,15)

    o = [s[0]+a & 0xffffffff, s[1]+b & 0xffffffff, s[2]+c & 0xffffffff, s[3]+d & 0xffffffff]

    return o


MSG = "this is a test for sha-1 functions. I hope it works good. Damm, I need It larger than..."
#MSG = MSG[:64]




print gh_md4(MSG)
print hashlib.new('md4', MSG).hexdigest()
print md4(MSG).encode('hex')


#m="ABCDEFGHIJKL"
#print make_words([ord(c) for c in m])
#print [struct.unpack("<I", block) for block in block_split(m,4)]



