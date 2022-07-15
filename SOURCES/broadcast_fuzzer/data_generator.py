import binascii
import os
import sys
from pathlib import Path
import random
import glob
import string
from constants import Constants


def random_multihex(png_hex, lo_index, hi_index):
    """
    hex string png_hex from start index to end index is replaced by new random hex
    """
    for i in range(lo_index, hi_index):
        png_hex = png_hex[:i] + random_onehex() + png_hex[i + 1:]
    return png_hex


def random_onehex():
    """
    get a random hex number
    """
    return str(random.choice("0123456789abcdef"))


def random_num(num):
    """
    get one random number
    """
    return random.randint(0, num)


def fuzz_one_txtfile(strlen, data_path, file_name):
    """
    generate a random string and store in a txt file
    """
    # generate random string with given length
    random_str = ""
    for i in range(strlen):
        random_str = random_str + random.choice(string.printable)
    # write to txt file
    fuzzed_savepath = data_path + file_name
    file = open(fuzzed_savepath, "w")
    file.write(random_str)
    file.close()


def fuzz_one_mp4file(file_type, fuzzed_filename, seed_path, data_path, mode):
    """
    generate a fuzzed mp4 file and store it to given path
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

    # mode 0 is only replacing header to other random header, consider file format
    if mode == 0:
        # get all headers' index, store it to all_header_index array
        all_header_index = []
        for i in range(len(seed_hex)):
            for j in range(len(Constants.MP4_IMPORTANT_HEADER)):
                if seed_hex.startswith(Constants.MP4_IMPORTANT_HEADER[j], i):
                    all_header_index.append(i)
        # random pick a number of how many headers need to be replaced
        random_header_index = []
        random_index_size = random_num(len(all_header_index))
        # pick header to modify
        for i in range(random_index_size):
            random_header_index.append(all_header_index[random_num(len(all_header_index) - 1)])
        if len(random_header_index) == 0:
            random_header_index.append(all_header_index[random_num(len(all_header_index) - 1)])
        # fuzz it, replace header
        for i in range(len(random_header_index)):
            random_header = random_num(len(Constants.MP4_IMPORTANT_HEADER) - 1)
            seed_hex = seed_hex[:random_header_index[i]] + Constants.MP4_IMPORTANT_HEADER[random_header] + seed_hex[random_header_index[i] + 8:]
    # mode 1 to randomly replace some of the digit, not consider file format
    elif mode == 1:
        # randomly pick how many digit to replace
        replace_random_num = random_num(10)
        # replace it
        for i in range(replace_random_num):
            random_index = random_num(len(seed_hex))
            seed_hex = seed_hex[:random_index] + random_onehex() + seed_hex[random_index + 1:]

    # write fuzzed data to a new mp4 file
    data = binascii.a2b_hex(seed_hex)
    fuzzed_savepath = data_path + fuzzed_filename
    file = open(fuzzed_savepath, "wb")
    file.write(data)
    file.close()


def fuzz_one_pngfile(file_type, fuzzed_filename, fuzz_index_arr, seed_path, data_path, mode):
    """
    generate a fuzzed png file and store it to given path
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

    # mode 0 is only replacing header to random digits, consider file format
    if mode == 0:
        # fuzz it
        for i in range(len(fuzz_index_arr)):
            chunk_start = fuzz_index_arr[i][0]
            chunk_end = fuzz_index_arr[i][1]
            seed_hex = random_multihex(seed_hex, chunk_start, chunk_end)
    # mode 1 to randomly replace some of the digit, not consider file format
    elif mode == 1:
        # randomly pick how many digit to replace
        replace_random_num = random_num(10)
        # replace it
        for i in range(replace_random_num):
            random_index = random_num(len(seed_hex))
            seed_hex = seed_hex[:random_index] + random_onehex() + seed_hex[random_index + 1:]

    # write fuzzed data to a new png file
    data = binascii.a2b_hex(seed_hex)
    fuzzed_savepath = data_path + fuzzed_filename
    file = open(fuzzed_savepath, "wb")
    file.write(data)
    file.close()


def fuzz(intent_id, file_type, data_runs, seed_path, data_path):
    """
    a driver function to control fuzz
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
            # create a new fuzzed png file with random mode
            mode = random.randint(0, 1)
            fuzz_one_pngfile(file_type, file_name, fuzz_index_arr, seed_path, data_path, mode)
        if file_type == "txt":
            # create a new fuzzed txt file
            strlen = random_num(2048)
            file_name = str(i) + "." + file_type
            fuzz_one_txtfile(strlen, data_path, file_name)
        if file_type == "mp4":
            # new unique filename
            file_name = str(i) + "." + file_type
            # create a new fuzzed mp4 file with random mode
            mode = random.randint(0, 1)
            fuzz_one_mp4file(file_type, file_name, seed_path, data_path, mode)


# if __name__ == '__main__':
#     fuzz("png", 10, "../../SEED/", "../../FuzzedData/")
