from logging import log
import subprocess
import os
import logger
log = logger.get_logger(__name__)
from constants import Constants

'''This class will contain utility functions that will use the adb cmd tool'''
class adbUtil(object):

    def __init__(self,adb_path):
        self.adb_path = adb_path

    def copy_to_android(self,src,dest):
        #./adb push ../SEED/png/ /storage/self/primary/buzzData'
        log.debug('copy_to_android()')
        log.debug('src = '+src)
        log.debug('dest ='+src)
        nbytes = sum(d.stat().st_size for d in os.scandir(src) if d.is_file())
        log.debug('size of source = %d',nbytes)
        if nbytes < Constants.MAX_FUZZ_DATA_SIZE_CAP:
            log.debug('source is %d less than %d',nbytes,Constants.MAX_FUZZ_SIZE_CAP)
            ret = subprocess.call([self.adb_path,"push",src,dest])
        else:
            ret = -1
        return ret
        
    def send_intent_activity(self,mimeType,activity_name,data,pkg_name):
        '''Launch intents of given mimeType'''
        # adb shell am start -a android.intent.action.SEND --es "android.intent.extra.TEXT" \"calling you\" -t "text/plain" -n "org.telegram.messenger/org.telegram.ui.LaunchActivity" 
        if mimeType == Constants.textType:
            ret = subprocess.call([self.adb_path,'shell','am','start','--es'
            ,'"android.intent.extra.TEXT"','\"data\"', '-t',mimeType,'-n','pkg_name/activity_name'])
            return ret
        elif mimeType == Constants.pngType:
            pass

    '''Function to check if at least one device is connected'''
    def is_device_conn(self):
        device_list = self.get_device_list()
        return len(device_list) != 0

    '''Function to check if multiple devices are connected'''
    def get_device_list(self):
        '/adb devices -l'
        device_list = []
        self.log.debug('is_device_conn()')
        output = subprocess.check_output([self.adb_path,'devices','-l'])
        self.log.debug(output)
        output = output.split(b'\n') 
        for line in output:
            device = line.decode('utf-8',errors='')
            if device != '':
                device_list.append(device)
        device_list.pop(0) # Remove the first message line that says 'List of Devices'
        return device_list


    '''Gets the whole log dump from logcat returns a file descriptor'''
    def get_logcat(self):
        self.log.debug('get_logcat')
        log_dump = subprocess.check_output([self.adb_path,'logcat','-d'])
        #self.log.debug(log_dump)
        return log_dump

    
    '''Clears logs created in the android logcat'''
    def clear_logs(self):
        log_dump = subprocess.run([self.adb_path,'logcat','-c'])
        self.log.debug('log_dump.returncode is '+log_dump.returncode)
        return log_dump.returncode