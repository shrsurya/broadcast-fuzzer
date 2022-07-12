import logging
logger = logging.getLogger(__name__)
import xml.etree.ElementTree as ET
from manifest import ManifestData

class BroadcastFuzzer(object):
    """
    A class to handle the various functionalities of
    broadcast fuzzer
    """
    REQUIRED = ['manifest']

    def __init__(self, **kwargs) -> None:
        """Configure self and execute"""
        self.dry = kwargs["dry"]
        self.print_flag = kwargs["print"]
        if 'manifest' in kwargs:
            manifest_file = kwargs['manifest']
            self.manifest_data = ManifestData(manifest_file)
        else:
            logger.error('manifest file missing')
    
        if self.print_flag:
            self.print_manifest()

    def print_manifest(self):
        print(self.manifest_data)

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