#!/usr/bin/python
import sys
import hashlib

# for i in $(ls /mnt//backup/123456789/*); do python ./check_hekate_sha256sum.py $i; done

CHUNK_SIZE = 8192*512

in_file = sys.argv[1]
if (in_file.find("rawnand.bin.") == -1 and in_file.find("BOOT") == -1) or in_file.find(".sha256sums") != -1:
    # print("  >> Nothing to do here. Skipping...")
    sys.exit(0)
    
print("[*] Processing {}:".format(in_file))
in_filesha = in_file + ".sha256sums"

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
            # print("  >> offset {}: calculated {} vs {} expected: SUCCESS".format(file_offset, sha256sum_calculated, sha256sum_expected))
            pass
        else:
            # print("  >> offset {}: calculated {} vs {} expected: FAILED".format(file_offset, sha256sum_calculated, sha256sum_expected))
            success = False
        chunk_index += 1
        data = fp.read(CHUNK_SIZE)
if success:
    # print("[*] SUCCESS: all hashes verified for {}".format(in_file))
    print("  >> OK")
else:
    print("  >> FAILED: at least one of the hashes failed checking for {}".format(in_file))
