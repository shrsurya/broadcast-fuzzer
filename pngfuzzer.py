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
    print(png_hex[20:30])
    for i in range(lo_index, hi_index):
        png_hex = png_hex[:i] + random_onehex() + png_hex[i + 1:]
        print(png_hex[20:30])
    return png_hex


def random_onehex():
    """
    :return: a random hex number
    """
    return str(random.choice("0123456789abcdef"))


def random_num(num):
    return random.randint(0, num)


def fuzz_one(fuzzed_filename):
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
    #print(seed_hex)
    #print("  ")

    # fuzz it
    chunks = 10 # need to figure out how many chunks
    chunk_num = random_num(chunks)
    chunk_length = 8 # need to figure out how many bytes this chunk has
    chunk_start = 22
    chunk_end = 24
    random_multihex(seed_hex, chunk_start, chunk_end)
    #print(seed_hex)
    # barr = bytearray.fromhex(seed_hex)
    # fuzzed_data = barr.decode(encoding="ascii", errors="ignore")

    # make fuzzed data be a new png file
    data = binascii.a2b_hex(seed_hex)
    fuzzed_savepath = "./FuzzedData/fuzzedpng/" + fuzzed_filename
    file = open(fuzzed_savepath, "wb")
    file.write(data)
    file.close()
    pass


def fuzz(run_time):
    for i in range(0, run_time):
        file_name = str(i) + ".png"
        fuzz_one(file_name)
    return


def main():
    runtime = int(sys.argv[1])
    fuzz(runtime)


if __name__ == '__main__':
    main()
