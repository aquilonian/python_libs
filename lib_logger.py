# --------------------------------------------------------------------------------------------------
# Name:         lib_logger
# Purpose:      Log messages to console and rotating file
#
# Created:      2013
# --------------------------------------------------------------------------------------------------
""" Atomate logging object creation. By default, only info is sent to console and rotating files.
    Optionally, debug messages to console and file can be added.
"""

import os
import time
import logging
import traceback
import logging.handlers


def get_logger(name, root_dir, dbg_to_console=False, dbg_to_file=False, clear_current=True,
               log_size_mb=5, logs_to_keep=5):
    """ Function to get the logger. If the logger already exists that is returned. Most of the
        parameters are self explanatory. clear_current simply opens the files in write mode to
        clear content.
    """
    # Return the logger if it already exists in the logging manager
    if name in logging.root.manager.loggerDict:
        return logging.getLogger(name)

    # Set the Console logging level
    console_level = logging.DEBUG if dbg_to_console else logging.INFO

    msg_format = "%(asctime)s %(levelname)-8s : %(module)-18s Ln:%(lineno)4d : %(message)s"
    log_byte_size = log_size_mb * 1048576 #Convert to bytes

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(msg_format)

    # Create the console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(console_level)
    logger.addHandler(console_handler)

    # Prepare the path where log files will be saved
    logs_dir = os.path.join(root_dir, "debuglogs")

    if not os.path.isdir(logs_dir):
        # Just a freak precaution
        if os.path.isfile(logs_dir):
            logs_dir = os.path.join(root_dir, f"debuglogs{int(time.time())}")

        try:
            os.makedirs(logs_dir)
        except FileExistsError:
            print(traceback.format_exc())
            exit()

    # Info Log file is always created
    info_log = os.path.join(logs_dir, f"{name}.info.log")
    if clear_current:
        with open(info_log, "w"):
            pass

    info_handler = logging.handlers.RotatingFileHandler(info_log, maxBytes=log_byte_size,
                                                        backupCount=logs_to_keep)
    info_handler.setFormatter(formatter)
    info_handler.setLevel(logging.INFO)
    logger.addHandler(info_handler)

    # Optionally, create the debug level log file
    if dbg_to_file:
        debug_log = os.path.join(logs_dir, f"{name}.debug.log")
        if clear_current:
            with open(debug_log, "w"):
                pass
        debug_handler = logging.handlers.RotatingFileHandler(debug_log, maxBytes=log_byte_size,
                                                         backupCount=logs_to_keep)
        debug_handler.setFormatter(formatter)
        debug_handler.setLevel(logging.DEBUG)
        logger.addHandler(debug_handler)


    logger.propagate = False

    return logger
