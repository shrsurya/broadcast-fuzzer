import binascii
import sys
import random
import glob
# from . import constant

"""
0 stands for header size (index 16 - 23, usually last two digits)
1 stands for pixel wide ()
2 stands for pixel high
3 stands for how many bits for pixel
4 stands for color type
5 stands for compression method ()
6 stands for filter method 
7 stands for IDAT content size
8 stands for data chunk 
"""
CHUNK_INDEX = [[16, 23], [32, 39], [40, 47], [48, 49], [50, 51], [52, 53], [54, 55], [66, 73]]


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


def fuzz_one(file_type, fuzzed_filename, fuzz_index_arr):
    """
    :param fuzzed_filename:
    :param fuzz_index_arr:
    :return:
    """
    # count how many files in SEED folder
    seed_path = "../../SEED/" + file_type + "/*.png"
    # print(seed_path)
    seed_arr = glob.glob(seed_path)
    seed_arr_size = len(seed_arr)
    # randomly pick a seed png file and get hex value of it
    seed_file_path = seed_arr[random_num(seed_arr_size - 1)]
    with open(seed_file_path, 'rb') as f:
        content = f.read()
    # convert the hex string to good format
    seed_hex = str(binascii.hexlify(content))
    seed_hex = seed_hex[2:len(seed_hex)-1]

    # fuzz it
    for i in range(len(fuzz_index_arr)):
        chunk_start = fuzz_index_arr[i][0]
        chunk_end = fuzz_index_arr[i][1]
        seed_hex = random_multihex(seed_hex, chunk_start, chunk_end)

    # barr = bytearray.fromhex(seed_hex)
    # fuzzed_data = barr.decode(encoding="ascii", errors="ignore")

    # make fuzzed data be a new png file
    data = binascii.a2b_hex(seed_hex)
    fuzzed_savepath = "../../FuzzedData/Fuzzed" + file_type + "/" + fuzzed_filename
    file = open(fuzzed_savepath, "wb")
    file.write(data)
    file.close()
    pass


def fuzz(file_type, fuzz_time, chunk_index_arr):
    for i in range(0, fuzz_time):
        total_random_chunks = random_num(len(chunk_index_arr) - 1)
        fuzz_index_arr = []
        for j in range(total_random_chunks):
            random_temp = random_num(len(chunk_index_arr) - 1)
            fuzz_index_arr.append(chunk_index_arr[random_temp])
        file_name = str(i) + "." + file_type
        fuzz_one(file_type, file_name, fuzz_index_arr)
    return


def main():
    file_type = str(sys.argv[1])
    fuzz_time = int(sys.argv[2])
    chunk_index_arr = CHUNK_INDEX

    fuzz(file_type, fuzz_time, chunk_index_arr)


if __name__ == '__main__':
    main()
