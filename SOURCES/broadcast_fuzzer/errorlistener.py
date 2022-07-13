# Use adb and logcat cmd tool to listen to the error log
from constants import Constants
from adbutil import adbUtil
import time
import os

class ErrorListener(object):

    # Timeout in ms

    def __init__(self,package_name,timeout):
        self.timeout = timeout
        self.package= package_name
        adb_path = os.environ.get('ADB_PATH')
        if adb_path == '':
            raise Exception('Cannot find path to adb tools!')
        self.adbUtil = adbUtil(adb_path)

    def __filter_err__(self):
        '''Text filter for finding relevant errors,
            Go through each line and check if there is an error phrase '''
        error_lines = []
        logcat = self.adbUtil.get_logcat()
        logcat = logcat.split(b'\n')

        # Ignore the first element as package names are usually in reverse DNS order 
        # eg. org.telegram.messenger
        package_tags = self.package.split('.')
        package_tags = package_tags[1:] 
        
        for line in logcat:
            str_line = line.decode('utf-8',errors='')
            for phrase in Constants.ERROR_PHRASES:
                if str_line.find(phrase) != -1:
                    for tags in package_tags:
                        if str_line.find(tags) != -1:
                            error_lines.append(str_line)        
        return error_lines
    
    def listen(self):
        # ./adb logcat -d | grep 'NullPointerException.*telegram'
        
        t0 = time.time()
        t1 = time.time()
        while (t1-t0) < self.timeout:
            devices = self.adbUtil.is_device_conn()
            if devices:
                errors = self.__filter_err__()
                if errors:
                    return errors
            else:
                raise Exception("No device connected!")
            time.sleep(1) # Wait for 1 second before sending the next logcat - (experimental value)
            t1 = time.time()
