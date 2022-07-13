class Constants(object):
    ERROR_PHRASES = ["SIGSEGV","NullPointer","Runtime","Exception","Error"]
    textType = 'text/plain'
    pngType = 'image/png'
    mp4Type = 'video/mp4'
    MIMETYPE_FILETYPE_DICT = {'image/*': 'png',
                            'text/plain': 'txt',
                            "text/*": "txt",
                            "video/*": "mp4",
                            "*/*": "any"}
    MAX_FUZZ_DATA_SIZE_CAP = 3e+7 # 30 MB file size limit to copy to android
