import binascii
import sys
import os, os.path
import random
import glob


def random_multihex(png_hex, lo_index, hi_index):
    """
    :param png_hex: hex string of seed png file
    :param lo_index: start index
    :param hi_index: end index
    :return: hex string of png file, data from start index to end index is replaced
    """
    for i in range(lo_index, hi_index):
        png_hex[i] = random_onehex()
    return png_hex


def random_onehex():
    """
    :return: a random hex number
    """
    return str(random.choice("0123456789abcdef"))


def random_num(num):
    return random.randint(0, num)


def fuzz(runtime, fuzzed_filename):
    # count how many files in SEED folder
    seed_arr = glob.glob("Seed/*.png")
    seed_arr_size = len(seed_arr)
    # randomly pick a seed png file
    seed_file_path = seed_arr[random_num(seed_arr_size - 1)]
    # get hex value of seed png file
    with open(seed_file_path, 'rb') as f:
        content = f.read()
    # seed_hex is a string
    seed_hex = str(binascii.hexlify(content))
    seed_hex = seed_hex[2:len(seed_hex)-1]

    # fuzz it
    chunks = 10 # need to figure out how many chunks
    chunk_num = random_num(chunks)
    chunk_length = 8 # need to figure out how many bytes this chunk has
    chunk_start = 0
    chunk_end = 0
    # random_multihex(seed_hex, chunk_start, chunk_end)

    # make fuzzed data be a new png file
    # barr = bytearray.fromhex(seed_hex)
    # fuzzed_data = barr.decode(encoding="ascii", errors="ignore")

    data = binascii.a2b_hex(seed_hex)
    fuzzed_savepath = "./FuzzedData/fuzzedpng/" + fuzzed_filename
    file = open(fuzzed_savepath, "wb")
    file.write(data)
    file.close()
    pass


def main():
    runtime = int(sys.argv[1])
    fuzz(runtime, "test1.png")


if __name__ == '__main__':
    main()
