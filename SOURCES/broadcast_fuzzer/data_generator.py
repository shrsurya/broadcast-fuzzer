import binascii
import os
import sys
from pathlib import Path
import random
import glob
import string
from constants import Constants


"""
0 stands for header size
1 stands for pixel wide
2 stands for pixel high
3 stands for how many bits for pixel
4 stands for color type
5 stands for compression method
6 stands for filter method
7 stands for IDAT content size
8 stands for data chunk
"""
# PNG_CHUNK_INDEX = [[16, 23], [32, 39], [40, 47], [48, 49], [50, 51], [52, 53], [54, 55], [66, 73]]


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


def fuzz_one_txtfile(strlen, data_path, file_name):
    # generate random string with given length
    random_str = ""
    for i in range(strlen):
        random_str = random_str + random.choice(string.printable)
    # write to txt file
    fuzzed_savepath = data_path + file_name
    file = open(fuzzed_savepath, "w")
    file.write(random_str)
    file.close()


def fuzz_one_mp4file(file_type, fuzzed_filename, seed_path, data_path):
    """
    :param intent_id: intent id that will be used to make a new folder store fuzzed data
    :param file_type: what type of fuzzed data to generate
    :param fuzzed_filename: fuzzed data file name
    :param fuzz_index_arr: store index of important chunks
    :param seed_path: path of this particular seed
    :param data_path: path of this particular fuzzed file
    :return: fuzzed data
    """
    # store all seeds file names inside an array for later use
    full_seed_path = seed_path + file_type + "/*." + file_type
    seed_arr = glob.glob(full_seed_path)
    seed_arr_size = len(seed_arr)
    # check if the Seed folder has seeds
    if seed_arr_size == 0:
        raise Exception("Error: No Seed found in Seed folder!")
    # randomly pick a seed file, read it and store data to a hex string
    seed_file_path = seed_arr[random_num(seed_arr_size - 1)]
    with open(seed_file_path, 'rb') as f:
        content = f.read()
    seed_hex = str(binascii.hexlify(content))
    seed_hex = seed_hex[2:len(seed_hex) - 1]

    # get all header index
    all_header_index = []
    for i in range(len(seed_hex)):
        for j in range(len(Constants.MP4_IMPORTANT_HEADER)):
            if seed_hex.startswith(Constants.MP4_IMPORTANT_HEADER[j], i):
                all_header_index.append(i)
    # random pick index to fuzz
    random_header_index = []
    random_index_size = random_num(len(all_header_index))
    for i in range(random_index_size):
        random_header_index.append(all_header_index[random_num(len(all_header_index) - 1)])
    if len(random_header_index) == 0:
        random_header_index.append(all_header_index[random_num(len(all_header_index) - 1)])
    print("hhhh ", random_header_index)

    # fuzz it
    for i in range(len(random_header_index)):
        random_header = random_num(len(Constants.MP4_IMPORTANT_HEADER) - 1)
        seed_hex = seed_hex[:random_header_index[i]] + Constants.MP4_IMPORTANT_HEADER[random_header] + seed_hex[random_header_index[i] + 8:]

    # write fuzzed data to a new mp4 file
    data = binascii.a2b_hex(seed_hex)
    fuzzed_savepath = data_path + fuzzed_filename
    file = open(fuzzed_savepath, "wb")
    file.write(data)
    file.close()


def fuzz_one_pngfile(file_type, fuzzed_filename, fuzz_index_arr, seed_path, data_path):
    """
    :param intent_id: intent id that will be used to make a new folder store fuzzed data
    :param file_type: what type of fuzzed data to generate
    :param fuzzed_filename: fuzzed data file name
    :param fuzz_index_arr: store index of important chunks
    :param seed_path: path of this particular seed
    :param data_path: path of this particular fuzzed file
    :return: fuzzed data
    """
    # store all seeds file names inside an array for later use
    full_seed_path = seed_path + file_type + "/*." + file_type
    seed_arr = glob.glob(full_seed_path)
    seed_arr_size = len(seed_arr)
    # check if the Seed folder has seeds
    if seed_arr_size == 0:
        raise Exception("Error: No Seed found in Seed folder!")
    # randomly pick a seed file, read it and store data to a hex string
    seed_file_path = seed_arr[random_num(seed_arr_size - 1)]
    with open(seed_file_path, 'rb') as f:
        content = f.read()
    seed_hex = str(binascii.hexlify(content))
    seed_hex = seed_hex[2:len(seed_hex)-1]

    # fuzz it
    for i in range(len(fuzz_index_arr)):
        chunk_start = fuzz_index_arr[i][0]
        chunk_end = fuzz_index_arr[i][1]
        seed_hex = random_multihex(seed_hex, chunk_start, chunk_end)

    # write fuzzed data to a new png file
    data = binascii.a2b_hex(seed_hex)
    fuzzed_savepath = data_path + fuzzed_filename
    file = open(fuzzed_savepath, "wb")
    file.write(data)
    file.close()


def fuzz(intent_id, file_type, data_runs, seed_path, data_path):
    """
    :param intent_id: intent id that will be used to make a new folder store fuzzed data
    :param file_type: what type of fuzzed data to generate
    :param data_runs: how many fuzzed data to generate
    :param seed_path: path of this particular seed
    :param data_path: path of this particular fuzzed file
    :return: fuzzed data
    """
    # add intent_id to data_path
    data_path = data_path + "/" + intent_id + "_" + file_type + "/"
    # making a new folder
    Path(data_path).mkdir(parents=True, exist_ok=True)
    # check if the folder exists
    if not os.path.isdir(seed_path):
        raise Exception("Error: Cannot find seed folder!")
    if not os.path.isdir(data_path):
        raise Exception("Error: Cannot find path to store fuzzed data!")

    # For each run
    for i in range(data_runs):
        if file_type == "png":
            # first creates random num of chunks to fuzz
            total_random_chunks = random_num(len(Constants.PNG_CHUNK_INDEX) - 1)
            fuzz_index_arr = []
            # then, picks random chunks to fuzz
            for j in range(total_random_chunks):
                random_temp = random_num(len(Constants.PNG_CHUNK_INDEX) - 1)
                fuzz_index_arr.append(Constants.PNG_CHUNK_INDEX[random_temp])
            # new unique filename
            file_name = str(i) + "." + file_type
            # create a new fuzzed file
            fuzz_one_pngfile(file_type, file_name, fuzz_index_arr, seed_path, data_path)
        if file_type == "txt":
            strlen = random_num(2048)
            file_name = str(i) + "." + file_type
            fuzz_one_txtfile(strlen, data_path, file_name)
        if file_type == "mp4":
            # new unique filename
            file_name = str(i) + "." + file_type
            # create a new fuzzed file
            fuzz_one_mp4file(file_type, file_name, seed_path, data_path)
# if __name__ == '__main__':
#     fuzz("png", 10, "../../SEED/", "../../FuzzedData/")
