from errorlistener import ErrorListener
from adbutil import adbUtil
import os
adb_path = os.environ.get('ADB_PATH')


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
    adb = adbUtil(adb_path)
    if adb.copy_to_android(src='../../SEED/png/',dest='/storage/self/primary/buzzData') == 0:
        print("Copied!")
    else:
        print("failed")
    