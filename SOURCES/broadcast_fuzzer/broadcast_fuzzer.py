import logging
logger = logging.getLogger(__name__)
from .manifest_data import manifest_data

class broadcastFuzzer(object):
    """
    A class to handle the various functionalities of
    broadcast fuzzer
    """
    REQUIRED = ['mainfest']

    def __init__(self, **kwargs) -> None:
        """Configure self and execute"""
        if 'mainfest' in kwargs:
            self.manifest_data = manifest_data(kwargs['config'])
        else:
            logger.error("Manifest file missing")

    

    def extract_apk(self, apk_path, extract_folder):
        """
        TODO: Not a priority as of now
        Use apktool to extract apk file
        apk_path: absolute path the apk file
        extract_folder:
        apktool d -s yourapk.apk -o yourfolder 

        Assumes: user has apktool installed
        """
        pass

    