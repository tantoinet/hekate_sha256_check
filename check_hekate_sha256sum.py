#!/usr/bin/python
import sys
import hashlib

CHUNK_SIZE = 8192*512

in_file = sys.argv[1]
in_filesha = sys.argv[2]

sha_table = []

with open(in_filesha) as fpsha:
    sha_table = fpsha.readlines()

chunk_index = 1
success = True
with open(in_file, 'rb') as fp:
    file_offset = fp.tell()
    data = fp.read(CHUNK_SIZE)
    while data:
        sha256sum_calculated = hashlib.sha256(data).hexdigest()
        sha256sum_expected = sha_table[chunk_index].rstrip()
        if (sha256sum_calculated == sha256sum_expected):
            print("offset {}: calculated {} vs {} expected: SUCCESS".format(file_offset, sha256sum_calculated, sha256sum_expected))
        else:
            print("offset {}: calculated {} vs {} expected: FAILED".format(file_offset, sha256sum_calculated, sha256sum_expected))
            success = False
        chunk_index += 1
        data = fp.read(CHUNK_SIZE)
if success:
    print("[*] SUCCESS: all hashes verified for {}".format(in_file))
else:
    print("[*] FAILURE: at least one of the hashes failed checking for {}".format(in_file))
