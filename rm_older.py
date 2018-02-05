import os
import datetime
import logging
import argparse

# Program arguments parsing
parser = argparse.ArgumentParser(description='Script that can find and delete files older than certain number of days.')
parser.add_argument('-n', type=int, help='number of days to keep files', required=True)
parser.add_argument('-d', '--delete', help='delete files that meet set criteria', action='store_true')
parser.add_argument('-v', '--verbose', help='shows debugging information', action='store_true')
parser.add_argument('-l', '--log', help='log all information to file', action='store_true')
parser.add_argument('directory', help='directory to be processed')
args = parser.parse_args()


# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# Add console handler
console = logging.StreamHandler()
if args.verbose:
    console.setLevel(logging.DEBUG)
else:
    console.setLevel(logging.INFO)
console.setFormatter(formatter)
logger.addHandler(console)

# Add file handler
if args.log:
    file = logging.FileHandler('log.log')
    file.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file.setFormatter(formatter)
    logger.addHandler(file)


# Check if provided directory exists
if not os.path.isdir(args.directory):
    logger.critical('Could not find provided directory ' + args.directory)
    exit()


def convert_size(size, precision=2):
    '''Converts file size in bytes to human readable format.'''
    suffixes = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB']
    index = 0
    while size >= 1024 and index < len(suffixes):
        index += 1
        size /= 1024.0
    return "{} {}".format(round(size, precision), suffixes[index])


if __name__ == "__main__":
    filenum = 0
    removed = 0
    saved_space = 0

    logger.debug('Starting the script')

    logger.debug('Searching folders')
    for cwd, dirs, files in os.walk(args.directory):
        logger.debug("Searching in folder {}".format(cwd))
        for file in files:
            filenum += 1
            curr_file = os.path.join(cwd, file)
            elapsed_time = datetime.datetime.now() - datetime.datetime.fromtimestamp(os.path.getmtime(curr_file))
            if elapsed_time > datetime.timedelta(days=args.n):
                logger.info("Found {} days old file ".format(elapsed_time.days) + curr_file)
                if args.delete:
                    logger.info("Deleting file {}".format(curr_file))
                    removed += 1
                    saved_space += os.path.getsize(curr_file)
                    os.remove(curr_file)

    logger.info('')
    logger.info("Found {} files.".format(filenum))
    logger.info("Deleted {} files.".format(removed))
    logger.info("Saved space by deleting: {}".format(convert_size(saved_space)))
    logger.info('Finished.')
