import unittest
from adb_util import adbUtil
import os
adb_path = os.environ.get('ADB_PATH')
from constants import Constants
from error_listener import ErrorListener
PACKAGE_NAME = "org.telegram.messenger"
adb_path = os.environ.get('ADB_PATH')
class TestAdb(unittest.TestCase):

# Listener test
    def listener_test(self):
        listener = ErrorListener(PACKAGE_NAME,5)
        logs =  listener.listen()
        if logs:
            print(logs)
        else:
            print('No errors raised within timeout')

# Copy test
    def copy_file_test(self):
        adb = adbUtil(adb_path)
        ret = adb.copy_to_android(src='../../FuzzedData/LaunchActivity_1_png/',dest='/storage/self/primary/buzzData')
        self.assertEquals(ret,0)

# Intent fire test
    def test_intent_fire(self):
        adb = adbUtil(adb_path)
        ret = adb.send_intent_activity(mimeType=Constants.pngType
        ,component_name='org.telegram.ui.LaunchActivity',action=Constants.INTENT_ACTION_SEND,
        data='file:///storage/self/primary/buzzData/LaunchActivity_1_png/0.png',pkg_name=PACKAGE_NAME)
        self.assertEquals(ret,0)
# Close app test
    def close_app(self):
        adb = adbUtil(adb_path)
        ret = adb.close_app(PACKAGE_NAME)
        self.assertEquals(ret,0)

# Create folder test
    def create_folder_test(self):
        adb = adbUtil(adb_path)
        ret = adb.mkdir('/storage/self/primary/buzzData')
        self.assertEquals(ret,0)


if __name__ == "__main__":
    unittest.main()