import subprocess
import logger

'''This class will contain utility functions that will use the adb cmd tool'''
class adbUtil(object):

    def __init__(self,adb_path):
        self.log =  logger.get_logger(__name__)
        self.adb_path = adb_path

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
    # def get_logcat(self):
    #     self.log.debug('get_logcat')
    #     log_dump = subprocess.Popen([self.adb_path,'logcat','-d'],stdout=subprocess.PIPE)
    #     errors = subprocess.check_output(['grep','-E' ,'NullPointerException.*telegram'],stdin=log_dump.stdout) 
    #     log_dump.wait()
    #     return errors

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