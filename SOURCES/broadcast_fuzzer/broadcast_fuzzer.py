import logging
logger = logging.getLogger(__name__)
import xml.etree.ElementTree as ET
from manifest import ManifestData
from data_generator import fuzz

class BroadcastFuzzer(object):
    """
    A class to handle the various functionalities of
    broadcast fuzzer
    """
    REQUIRED = ['manifest']
    MIMETYPE_FILETYPE_DICT = {'image/*': 'png',
                              'text/plain': 'txt',
                              "text/*": "txt",
                              "video/*": "mp4",
                              "*/*": "any"}

    def __init__(self, **kwargs) -> None:
        """Configure self and execute"""
        self.dry = kwargs["dry"]
        self.print_flag = kwargs["print"]

        # Extract data from manifest file
        if 'manifest' in kwargs:
            manifest_file = kwargs['manifest']
            self.manifest_data = ManifestData(manifest_file)
        else:
            logger.error('manifest file missing')

        # Print Manifest Data
        if self.print_flag:
            self.print_manifest()

        # Fuzzed Data params
        self.data_runs = kwargs['data_runs']
        self.gen = kwargs['gen']
        self.data_path = kwargs['data_path']
        self.seed_path = kwargs['seed_path']

        # if gen flag is true
        if self.gen:
            self.generate_fuzzed_data()

    def print_manifest(self):
        print(self.manifest_data)

    def generate_fuzzed_data(self):
        for intent in self.manifest_data.intent_filters:
            # if mimetype is in the global dic, fuzz, else skip
            try:
                intent_type = self.MIMETYPE_FILETYPE_DICT[intent.data_mimetype]
                if intent_type == 'png':
                    fuzz(intent.id, intent_type, self.data_runs, self.seed_path, self.data_path)
            except:
                pass
        pass