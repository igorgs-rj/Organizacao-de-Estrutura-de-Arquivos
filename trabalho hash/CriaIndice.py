import struct
import hashlib
import os
import sys

hashSize = 17000023




def h(key):
    global hashSize
    return int(hashlib.sha1(key).hexdigest(),16)%hashSize


def criaIndice(fName,indFName):
    hashSize = 17000023
    fileName = fName
    indexName = indFName
    indexFormat = "14sLL"
    indexStruct = struct.Struct(indexFormat)
    fi = open(indexName, "wb")
    emptyIndexRecord = indexStruct.pack("", 0, 0)
    for i in range(0, hashSize):
        fi.write(emptyIndexRecord)
    fi.close()

    f = open(fileName, "r")
    fi = open(indexName, "r+b")

    fi.seek(0, os.SEEK_END)
    fileIndexSize = fi.tell()
    print "IndexFileSize", fileIndexSize
    f.readline()



    recordNumber = 0
    while True:
        recordNumber = f.tell()
        line = f.readline()
        infoLine = line.split('\t')
        if line == "":  # EOF
            break
        p = h(infoLine[7])
        fi.seek(p * indexStruct.size, os.SEEK_SET)
        indexRecord = indexStruct.unpack(fi.read(indexStruct.size))
        fi.seek(p * indexStruct.size, os.SEEK_SET)
        if indexRecord[0][0] == "\0":
            fi.write(indexStruct.pack(infoLine[7], recordNumber, 0))
        else:
            nextPointer = indexRecord[2]
            fi.write(indexStruct.pack(indexRecord[0], indexRecord[1], fileIndexSize))
            fi.seek(0, os.SEEK_END)
            fi.write(indexStruct.pack(infoLine[7], recordNumber, nextPointer))
            fileIndexSize = fi.tell()
        recordNumber += 1
    f.close()
    fi.close()



if len(sys.argv)<3:
    print "Tente novamente"
else:
    criaIndice(str(sys.argv[1]), str(sys.argv[2]))
    print "Indice criado com sucesso"






