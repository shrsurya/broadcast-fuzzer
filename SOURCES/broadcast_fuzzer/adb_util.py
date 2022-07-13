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
        """
        Copies data from give src dir to dest dir in android device
        args:
            src: source path
            dest: destination path on android device (permissible path)
        returns:
            ret: code (0 for success, else failure)
        """
        #./adb push ../SEED/png/ /storage/self/primary/buzzData'
        log.debug('copy_to_android()')
        log.debug('src = '+src)
        log.debug('dest ='+src)
        # Ensures that size of file is below MAX_FUZZ_DATA_SIZE_CAP
        nbytes = sum(d.stat().st_size for d in os.scandir(src) if d.is_file())
        log.debug('size of source = %d',nbytes)
        if nbytes < Constants.MAX_FUZZ_DATA_SIZE_CAP:
            log.debug('source is %d less than %d',nbytes,Constants.MAX_FUZZ_DATA_SIZE_CAP)
            ret = subprocess.call([self.adb_path,"push",src,dest])
        else:
            ret = -1
        return ret
        
    def send_intent_activity(self,mimeType,action,component_name,data,pkg_name):
        '''Launch intents of given mimeType'''
        log.debug('send_intent_activity()')
        log.debug('mimeType ='+mimeType)
        log.debug('Component Name ='+component_name)
        log.debug('Package Name ='+pkg_name)
        if mimeType == Constants.textType:            
            # adb shell am start -a android.intent.action.SEND --es "android.intent.extra.TEXT" \"My message\" -t "text/plain" -n "org.telegram.messenger/org.telegram.ui.LaunchActivity" 
            ret = subprocess.call([self.adb_path,'shell','am','start','-a',action,'--es'
            ,Constants.INTENT_EXTRA_TEXT, "\'"+ data +"\'", '-t',mimeType,'-n',pkg_name +'/'+component_name])
            return ret
        elif mimeType == Constants.pngType:
            # ./adb shell am start -a android.intent.action.SEND -t  image/jpg --eu android.intent.extra.STREAM file:///storage/self/primary/buzzData/test1.png -n "org.telegram.messenger/org.telegram.ui.LaunchActivity"
            ret = subprocess.call([self.adb_path,'shell','am','start','-a',action,'--eu'
            ,Constants.INTENT_EXTRA_STREAM, data, '-t',mimeType,'-n',pkg_name +'/'+component_name])
            return ret
        else:
            return -1

    '''Function to check if at least one device is connected'''
    def is_device_conn(self):
        device_list = self.get_device_list()
        return len(device_list) != 0

    '''Function to check if multiple devices are connected'''
    def get_device_list(self):
        '/adb devices -l'
        device_list = []
        log.debug('is_device_conn()')
        output = subprocess.check_output([self.adb_path,'devices','-l'])
        log.debug(output)
        output = output.split(b'\n') 
        for line in output:
            device = line.decode('utf-8',errors='')
            if device != '':
                device_list.append(device)
        device_list.pop(0) # Remove the first message line that says 'List of Devices'
        return device_list


    '''Gets the whole log dump from logcat returns a file descriptor'''
    def get_logcat(self):
        log.debug('get_logcat')
        log_dump = subprocess.check_output([self.adb_path,'logcat','-d'])
        #log.debug(log_dump)
        return log_dump

    
    '''Clears logs created in the android logcat'''
    def clear_logs(self):
        log_dump = subprocess.run([self.adb_path,'logcat','-c'])
        log.debug('log_dump.returncode is '+log_dump.returncode)
        return log_dump.returncode