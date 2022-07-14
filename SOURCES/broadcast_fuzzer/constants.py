class Constants(object):
    ERROR_PHRASES = ["SIGSEGV","NullPointer","Runtime","Exception","Error"]
    textType = "text/plain"
    pngType = "image/*"
    mp4Type = "video/mp4"
    MIMETYPE_FILETYPE_DICT = {"image/*": "png",
                            "text/plain": "txt",
                            "text/*": "txt",
                            "video/*": "mp4",
                            "*/*": "any"}
    MAX_FUZZ_DATA_SIZE_CAP = 3e+7 # 30 MB file size limit to copy to android
    
    INTENT_EXTRA_TEXT = "android.intent.extra.TEXT"
    INTENT_ACTION_SEND = "android.intent.action.SEND"
    INTENT_EXTRA_STREAM = "android.intent.extra.STREAM"
    
    ANDROID_STR = "{http://schemas.android.com/apk/res/android}"
    ANDROID_STR_NAME = ANDROID_STR+"name"
    ANDROID_STR_MIMETYPE = ANDROID_STR+"mimeType"

    DEVICE_FUZZ_DATA_DIR = "/storage/self/primary/buzzData/"
    MOBILE_DATA_PATH_PREFIX = "file://"
    PNG_CHUNK_INDEX = [[16, 23], [32, 39], [40, 47], [48, 49], [50, 51], [52, 53], [54, 55], [66, 73]]
    MP4_IMPORTANT_HEADER = ["6d6d7034", "6d646174", "6d6f6f76", "6d766864", "636d6f76", "726d7261"]

    