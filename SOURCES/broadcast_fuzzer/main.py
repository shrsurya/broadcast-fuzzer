from adbutil import adbUtil
import os
adb_path = os.environ.get('ADB_PATH')
from constants import Constants

PACKAGE_NAME = "org.telegram.messenger"

if __name__ == '__main__':
# Listener test
    # listener = ErrorListener(PACKAGE_NAME,30)
    # logs =  listener.listen()
    # if logs:
    #     print(logs)
    # else:
    #     print('No errors raised within timeout')

# Copy test
    #calculate total directory size and only copy if smaller that that 
    # adb = adbUtil(adb_path)
    # if adb.copy_to_android(src='../../SEED/png/',dest='/storage/self/primary/buzzData') == 0:
    #     print("Copied!")
    # else:
    #     print("failed")

# Intent fire test
        # adb shell am start -a android.intent.action.SEND --es "android.intent.extra.TEXT" \"calling you\" -t "text/plain" -n "org.telegram.messenger/org.telegram.ui.LaunchActivity" 
    adb = adbUtil(adb_path)
    ret = adb.send_intent_activity(mimeType=Constants.pngType
    ,component_name='org.telegram.ui.LaunchActivity',action=Constants.INTENT_ACTION_SEND,data='file:///storage/self/primary/buzzData/test1.png',pkg_name=PACKAGE_NAME)
    if ret == 0:
        print("success!")
    else:
        print("failed to send!")
