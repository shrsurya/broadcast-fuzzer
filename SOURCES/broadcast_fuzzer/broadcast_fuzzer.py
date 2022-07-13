import logging
import os
logger = logging.getLogger(__name__)
from manifest import ManifestData
from data_generator import fuzz
from constants import Constants
from adb_util import adbUtil
from error_listener import ErrorListener


class BroadcastFuzzer(object):
    """
    A class to handle the various functionalities of
    broadcast fuzzer
    """
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
        self.adb_path = ""
        if kwargs["adb_path"]:
            self.adb_path = kwargs["adb_path"]
        else:
            self.adb_path = os.environ.get("ADB_PATH")
            if self.adb_path == "":
                raise Exception("Cannot find path to adb tools!")

        self.adb = adbUtil(self.adb_path)

        # Execute intent fuzzing
        # TODO: Simultaneously handle mutliple android devices connected to PC
        if kwargs["execute"]:
            if self.adb.is_device_conn():
                self.execute()
            else:
                logger.error("Android device not connected")

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
                intent_type = Constants.MIMETYPE_FILETYPE_DICT[intent.data_mimetype]
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
                    self.intent_to_fuzzed_data_folder_path_dict[intent] = path
                if intent_type == "png":
                    fuzz(intent.id, intent_type, self.data_runs, self.seed_path, self.data_path)
            except:
                pass


    def execute(self):
        """
        Executes the fuzzing of every intent in the manifest
        """
        for intent, data_path in self.intent_to_fuzzed_data_folder_path_dict.items():
            # print(intent_id, " : ", data_path)
            # Try to copy fuzzed data to the android device
            ret_code = self.adb.copy_to_android(src=data_path, dest=Constants.DEVICE_FUZZ_DATA_DIR)
            # if not successful, break
            if ret_code !=0:
                logger.debug(ret_code)
                logger.error("Failed to copy fuzzed data to destination")
                break
            # Fire an intent based on files copied to android device
            for i in range(self.data_runs):
                # Clearing logs before each intent/test case
                ret_code = self.adb.clear_logs()
                # if not successful, break
                if ret_code !=0:
                    logger.debug(ret_code)
                    logger.error("Failed to clear log")
                    return
                # file name
                file_ext = data_path.split("-")[-1]
                file_name = str(i)+"."+file_ext
                mobile_data_path = Constants.DEVICE_FUZZ_DATA_DIR + data_path + file_name
                ret_code = self.adb.send_intent_activity(
                    mimeType=intent.data_mimetype,
                    action=intent.action_name,
                    component_name=intent.sar_name,
                    data=mobile_data_path,
                    pkg_name= self.package_name
                )
                # if not successful, break
                if ret_code !=0:
                    logger.debug(ret_code)
                    logger.warn(str(intent.id)+" wasn't fired successfully for "+mobile_data_path)
                    continue
                # instantiate listener
                listener = ErrorListener(package_name=self.package_name, timeout=13)
                errors = listener.listen()
                # if no errors, we move one
                if len(errors) == 0:
                    logger.info("No erros found for ", str(mobile_data_path))
                    continue
                
                # TODO: Create a report, save the logs along with the datafile that caused the crash
                logger.warn("Crash detected: "+ str(errors))

