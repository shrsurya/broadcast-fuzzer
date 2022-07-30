import logging
import os
logger = logging.getLogger(__name__)
from pathlib import Path
import shutil
import time
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
                flag = False
                if intent_type == "png":
                    fuzz(intent.id, intent_type, self.data_runs, self.seed_path, self.data_path)
                    flag = True
                elif intent_type == "txt":
                    fuzz(intent.id, intent_type, self.data_runs, self.seed_path, self.data_path)
                    flag = True
                elif intent_type == "mp4":
                    fuzz(intent.id, intent_type, self.data_runs, self.seed_path, self.data_path)
                    flag = True
                # add a path for each intent with fuzzed data
                if flag:
                    path = self.data_path + intent.id + "_" + intent_type + "/"
                    self.intent_to_fuzzed_data_folder_path_dict[intent] = path
            except:
                logger.info("Unsupported mimeType!")
                pass



    def execute(self):
        """
        Executes the fuzzing of every intent in the manifest
        """
        for intent, data_path in self.intent_to_fuzzed_data_folder_path_dict.items():
            # print(intent_id, " : ", data_path)
            # Try to copy fuzzed data to the android device
            if not os.path.isdir(data_path):
                logger.error("Invalid fuzzed data dir")
                break
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
                file_ext = data_path.split("_")[-1]
                file_ext = file_ext[:-1]
                file_name = str(i)+"."+file_ext

                # Removing the FuzzData/ from the data_path i.e Getting individual intent folder names  
                subfolder = data_path.split('/')[-2]

                mobile_data_path = Constants.MOBILE_DATA_PATH_PREFIX + Constants.DEVICE_FUZZ_DATA_DIR + subfolder + '/' + file_name
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
                self.generate_crash_report( fuzzed_file_path=data_path+file_name,
                                            error_list=errors,
                                            intent=intent)
        # self.delete_data()
        #TODO: close the target android application


    def delete_data(self):
        """
        delete all fuzzed data after using
        """
        # get all files
        files = self.data_path
        for file in os.listdir(files):
            file_path = os.path.join(files, file)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))


    def generate_crash_report(self, fuzzed_file_path, error_list, intent):
        """
        Creates a crash report folder with details of the crash
        args:
            fuzzed_file_path: Path the the fuzzed file that caused the crash
            error_list: A list containing error lines
            intent: current intent
        """
        # get current time
        timestr = time.strftime("%Y%m%d-%H%M%S")
        try:
            # Create a new Reports folder if it doesn't already exist
            reports_folder_path = 'Reports/'
            Path(reports_folder_path).mkdir(parents=True, exist_ok=True)

            # Create a new report folder with current datetime
            current_report_path = reports_folder_path + "report_"+ self.package_name+"_"+str(intent.id) + "_"+ timestr
            Path(current_report_path).mkdir(parents=True, exist_ok=True)
        except:
            logger.warning("Unable to create reports folder")
            pass

        try:
        # Add a log file to the new folder with:
        # 1. Intent Details, 2. Errors
            new_log_file = current_report_path + "/" + timestr + ".log"
            with open(new_log_file, 'w') as file:
                str_to_write = "Intent Details:\n" + str(intent) + "\n"
                for line in error_list:
                    str_to_write += line + "\n"
                file.write(str_to_write)
            # Copy the fuzzed file to the newly created report dir
            src_path = fuzzed_file_path
            file_name = fuzzed_file_path.split('/')[-1]
            dst_path = current_report_path+"/"+file_name
            shutil.copy2(src=src_path, dst=dst_path)
        except:
            logger.warning("Unable to copy log files, "+str(intent.id))
