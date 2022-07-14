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
    