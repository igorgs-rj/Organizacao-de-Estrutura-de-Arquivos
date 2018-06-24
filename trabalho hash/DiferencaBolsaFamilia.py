import struct
import hashlib
import os
import sys

hashSize = 17000023

def h(key):
    global hashSize
    return int(hashlib.sha1(key).hexdigest(),16)%hashSize

if len(sys.argv)<4:
    print "Tente novamente"
else:
    f1 = open(str(sys.argv[1]),"r")
    f2 = open(str(sys.argv[2]), "r+b")
    f3 = open(str(sys.argv[3]), "a+")
    header = f1.readline()
    f3.write(header)
    indexFormat = "14sLL"
    indexStruct = struct.Struct(indexFormat)

    while True:
        line = f1.readline()
        infoLine = line.split('\t')
        if line == "":  # EOF
            break
        nis = infoLine[7]
        p = h(nis)
        offset = p * indexStruct.size
        i = 1
        while True:
            f2.seek(offset, os.SEEK_SET)
            indexRecord = indexStruct.unpack(f2.read(indexStruct.size))
            if indexRecord[0] == nis:
                break
            offset = indexRecord[2]
            if offset == 0:
                f3.write(line)
                break
            i += 1
    f1.close()
    f2.close()
    f3.close()























