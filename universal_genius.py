import logging, argparse, sys, os, time
from DataStore import DataStore
from rpc import rpc

from pprint import pprint


def ParseArgs():
    parser = argparse.ArgumentParser(description='Unified user unlocker',
                                     epilog='--\nHave a great day from Universal Genious')

    parser.add_argument('--db', help='Database TNS name')
    # , required=True

    parser.add_argument('--list-map', help='List mapping of DB to Host:Sid', action='store_true')
    parser.add_argument('--put', help="Add/Update mapping, format: --put DB:host1,port2;host2:port2")
    parser.add_argument('--delete', help="Delete mapping, format: --delete DB")
    parser.add_argument('--unlock', help="Unlock account only", action='store_true')
    parser.add_argument('--reset', help="Unlock and reset passord for account (new password will be generated.", action='store_true')
    # parser.add_argument('--key', help='Partition key')
    # parser.add_argument('--remap', help='Partition key')
    parsed_args = parser.parse_args()
    return parsed_args


def init_logging():
    logPath = "logs"
    vlogger = logging.getLogger()
    vlogger.setLevel(logging.DEBUG)
    logFormatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    ch = logging.StreamHandler()
    ch.setFormatter(logFormatter)
    ch.setLevel(logging.INFO)
    vlogger.addHandler(ch)

    fileName = "universal_genius_" + time.strftime("%Y%m%d")
    fh = logging.FileHandler("{0}/{1}.log".format(logPath, fileName), mode='a')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logFormatter)
    vlogger.addHandler(fh)

    vlogger.info("Logger initizlized")

    return vlogger

def main():
    args = ParseArgs()
    logger = init_logging()
    db = DataStore("pickle.pck", logger)

    if args.list_map:
        db.list()

    logger.info("User {} rinning this script.".format(os.getlogin()))

    if args.put:
        logger.info("Adding mapping, {}".format(args.put))
        db.set(*db.parseCommandLine(args.put))

    if args.delete:
        logger.info("Deleting mapping for DB: {}".format(args.delete))
        db.delete(args.delete.upper())

    if args.unlock or args.reset:
        # check if we have mapping for DB
        if db.get(args.db.upper()):
            logger.info("Trying to unlock/resep password for DB: {}.".format(args.db))
            rpc_call = rpc(db.get(args.db), logger)
            res = rpc_call.proceed_changes(args.unlock, args.reset)
        else:
            logger.critical("We don't have mapping for DB: {}".format(args.db))


if __name__ == "__main__":
    main()
