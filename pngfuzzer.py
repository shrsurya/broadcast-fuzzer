import binascii
import sys
import random
import glob
# from . import constant

"""
0 stands for header size (index 16 - 23, usually last two digits) [16, 23]
1 stands for pixel wide () [32, 39]
2 stands for pixel high [40, 47]
3 stands for how many bits for pixel [48, 49]
4 stands for color type [50, 51]
5 stands for compression method () [52, 53]
6 stands for filter method [54, 55]
7 stands for IDAT content size [66, 73]
8 stands for data chunk (not modifying this now)
"""
# a constant array to remember the index of each chunks
CHUNK_INDEX_ARR = [[16, 23], [32, 39], [40, 47], [48, 49], [50, 51], [52, 53], [54, 55], [66, 73]]


def random_multihex(png_hex, lo_index, hi_index):
    """
    :param png_hex: hex string of seed png file
    :param lo_index: start index
    :param hi_index: end index
    :return: hex string of png file, data from start index to end index is replaced
    """
    for i in range(lo_index, hi_index):
        png_hex = png_hex[:i] + random_onehex() + png_hex[i + 1:]
    return png_hex


def random_onehex():
    """
    :return: a random hex number
    """
    return str(random.choice("0123456789abcdef"))


def random_num(num):
    return random.randint(0, num)


def fuzz_one(fuzzed_filename, fuzz_index_arr):
    """
    :param fuzzed_filename: file path to store fuzzed data
    :param fuzz_index_arr: array to store which chunk should be fuzzed in this iteration
    :return: none, this function creates a new fuzzed png file
    """
    # count how many files in SEED folder
    seed_filename_arr = glob.glob("Seed/*.png")
    seed_file_num = len(seed_filename_arr)
    # randomly pick a seed png file and get hex value of it
    seed_file = seed_filename_arr[random_num(seed_file_num - 1)]
    with open(seed_file, 'rb') as f:
        content = f.read()
    # convert the hex string to good format
    seed_hex = str(binascii.hexlify(content))
    seed_hex = seed_hex[2:len(seed_hex)-1]

    # fuzz it
    fuzzed_hex = ""
    for i in range(len(fuzz_index_arr)):
        chunk_start = fuzz_index_arr[i][0]
        chunk_end = fuzz_index_arr[i][1]
        fuzzed_hex = random_multihex(seed_hex, chunk_start, chunk_end)

    # make fuzzed data be a new png file
    data = binascii.a2b_hex(fuzzed_hex)
    fuzzed_savepath = "./FuzzedData/fuzzedpng/" + fuzzed_filename
    file = open(fuzzed_savepath, "wb")
    file.write(data)
    file.close()
    pass


def fuzz(run_time):
    for i in range(0, run_time):
        total_randomechunk_num = random_num(len(CHUNK_INDEX_ARR) - 1)
        fuzz_index_arr = []
        for j in range(total_randomechunk_num):
            random_temp = random_num(len(CHUNK_INDEX_ARR) - 1)
            fuzz_index_arr.append(CHUNK_INDEX_ARR[random_temp])
        file_name = str(i) + ".png"
        print("filename: ", file_name," chunknum: ", total_randomechunk_num, " chunkindex: ", fuzz_index_arr)
        fuzz_one(file_name, fuzz_index_arr)
    return


def main():
    fuzz_num = int(sys.argv[1])
    fuzz(fuzz_num)


if __name__ == '__main__':
    main()
