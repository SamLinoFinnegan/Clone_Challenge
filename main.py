import os
import argparse
import shutil
import logging
import logging.handlers
from crontab import CronTab

# add the path to your project folder
FULLPATH ="place/the/full/path/to/your/dir"
handler = logging.handlers.WatchedFileHandler(os.path.join(FULLPATH,"main.log"))

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)

root = logging.getLogger()
root.setLevel(logging.INFO)
root.addHandler(handler)

def parse_arguments():
    """
    Argparser to be able to take arguments from the command line and send it to the clone function
    """
    parser = argparse.ArgumentParser(description="This argparser will take paths as arguments to synchronize two folders")
    parser.add_argument("-PO", "--path_origin", required=True, type=str, help="Use the -PO flag for the path of the origin folder.")
    parser.add_argument("-PT", "--path_target", required=True, type=str, help="Use the -PT flag for the path of the target folder.")
    parser.add_argument("-t", "--time", nargs='?', const=0, type=str,help="Use the -t flag to set up your synchronization time, this is set in minutes")
    return parser.parse_args()

def cron_job(time, command_input):
    """
    Function to create the cronjob, this function takes two parameters, time, and command
    Time should be input as minutes
    """
    with CronTab(user='root') as cron:
        job = cron.new(command=command_input)
        job.minute.every(time)

def clone_folder(path_origin, path_target):
    """
    This is a program that will link two folders, copying whatever is in one to the other
    It takes in two arguments, path_origin, and path_target
    """
    logging.info(f"Cloning files from {path_origin} to {path_target}")

    # remove the previous content from the target folder
    for file in os.listdir(path_target):
        target_path = os.path.join(path_target, file)
        if os.path.isdir(target_path):
            shutil.rmtree(target_path)
            logging.info(f"Removing {target_file} folder from {path_target}")
        else:
            os.remove(target_path)
            logging.info(f"Removing {target_file} file from {path_target}")

    try:
        os.makedirs(path_target, exist_ok=True)
        
        for file_name in os.listdir(path_origin):

            source_path = os.path.join(path_origin, file_name)
            target_path = os.path.join(path_target, file_name)
            
            shutil.copy(source_path, target_path)
            logging.info(f"Copied {file_name} to {path_target}")
           
    except Exception as error:
        logging.error(f"An error occurred: {error}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    args = parse_arguments()
    clone_folder(args.path_origin, args.path_target)
    if args.time:
        # add the path to your project folder
        command = f"cd /home/Clone_Challange && /usr/bin/python3.10 main.py -PO {args.origin} -PT {args.target}"
        cron_job(args.time, command)
