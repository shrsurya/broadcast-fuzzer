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
    REQUIRED = ["manifest"]
    MIMETYPE_FILETYPE_DICT = {
                                "image/*": "png",
                                "text/plain": "txt",
                                "text/*": "txt",
                                "video/*": "mp4",
                                "*/*": "any"
                            }

    def __init__(self, **kwargs) -> None:
        """Configure self and execute"""

        # If dry is true, we only print what will happen
        self.dry = kwargs["dry"]

        # Extract data from manifest file
        if "manifest" in kwargs:
            manifest_file = kwargs["manifest"]
            self.manifest_data = ManifestData(manifest_file)
        else:
            logger.error("manifest file missing")

        # Package name
        self.package_name = self.manifest_data.manifest_package_name
        # Intent List
        self.intents = self.manifest_data.intent_filters
        # Fuzzed Data Path for each intent
        # Values added during fuzzed data generation
        self.intent_to_fuzzed_data_folder_path_dict = dict()

        # Print Manifest Data
        if kwargs["print"]:
            self.print_manifest()

        # Fuzzed Data params
        self.data_runs = kwargs["data_runs"]
        self.data_path = kwargs["data_path"]
        self.seed_path = kwargs["seed_path"]

        # if gen flag is true
        if kwargs["gen"]:
            self.generate_fuzzed_data()
        
        # if adb path is provided
        if kwargs["adb_path"]:
            self.adb_path = kwargs["adb_path"]
        else:
            # get env path
            pass

        # Execute intent fuzzing
        if kwargs["execute"]:
            self.execute()


    def print_manifest(self):
        """
        Prints the Manifest file
        """
        print(self.manifest_data)


    def generate_fuzzed_data(self):
        """
        Generates fuzzed data for each intent in the manifest
        """
        for intent in self.intents:
            # if mimetype is in the global dic, fuzz, else skip
            try:
                intent_type = self.MIMETYPE_FILETYPE_DICT[intent.data_mimetype]
                if intent_type == "png":
                    fuzz(
                        intent.id, 
                        intent_type, 
                        self.data_runs, 
                        self.seed_path, 
                        self.data_path
                        )
                    # add a path for each intent with fuzzed data
                    path = self.data_path + intent.id + "-" + intent_type + "/"
                    self.intent_to_fuzzed_data_folder_path_dict[intent.id] = path
            except:
                pass


    def execute(self):
        """
        Executes the fuzzing of every intent in the manifest
        """
        for k,v in self.intent_to_fuzzed_data_folder_path_dict.items():
            print(k, " : ", v)