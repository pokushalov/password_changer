import pickle
import os.path
from pprint import pprint


class DataStore:
    def __init__(self, data_file, logger):
        self.map = None
        self.pkl_file = None
        self.file_name = data_file
        self.logger = logger

        self.logger.debug("Reading pickle file: {}".format(self.file_name))
        if os.path.isfile(self.file_name):
            self.pkl_file = open(self.file_name, 'rb')
            self.map = pickle.load(self.pkl_file)
            self.pkl_file.close()
        else:
            logger.critical("No file with mapping exists: {}, please add mapping".format(self.file_name))
            self.map = {}

    def save(self, data):
        self.logger.debug("In datastore::save")
        if self.pkl_file is None:
            self.pkl_file = open(self.file_name, 'wb')
        if self.pkl_file.closed :
            self.pkl_file = open(self.file_name, 'wb')
        pickle.dump(data, self.pkl_file)
        self.pkl_file.close()
        self.map = data
        self.logger.info("Changes saved to DB.")

    def list(self):
        self.logger.debug("In datastore::list")
        self.logger.debug("DataStore: list")
        self.logger.debug("Geting list of saved DB's")
        if self.map:
            print("List of database mapped in file:")

        for db,v in sorted(self.map.items()):
            print("\tDatabase: {}".format(db.upper()))
            for info in v:
                print("\t\t{}:{}".format(info[0], info[1]))

    def get(self, req):
        self.logger.debug("In datastore::get")
        self.logger.debug("Getting value of map for {}".format(req))
        return self.map.get(req.upper(), None)

    def set(self, p_db, p_value):
        self.logger.debug("In datastore::set")
        self.logger.debug("Setting value {} for DB: {}".format(p_value, p_db))
        dataOK = False
        if isinstance(p_value, list):
            dataOK = True
            for tpl in p_value:
                if not isinstance(tpl, tuple) or len(tpl) != 2:
                    dataOK = False
                    break
        if dataOK:
            self.logger.debug("Setting value of map for {}".format(p_db))
            self.map[p_db.upper()] = p_value
            self.save(self.map)
        else:
            self.logger.critical("Incorrect data in {} while trying to map DB: [{}]".format(p_value, p_db))

    def parseCommandLine(self, p_param):
        try:
            self.logger.debug("In datastore::parseCommandLine")
            p_val = p_param.replace(" ","")
            db, pairs = p_val.split(":")[0], p_val.split(":")[1]
            res = [tuple(pair.split(",")) for pair in pairs.replace(" ","").split(";")]
            return db, res
        except:
            self.logger.critical("Error while trying to parse parameter: {}.".format((p_param)))
            self.logger.critical("Please fix this error and rerun.")
            exit(-1)

    def delete(self, p_db):
        if p_db in self.map:
            del self.map[p_db]
            self.save(self.map)
            self.logger.info("Deleted mapping for {}.".format(p_db))
        else:
            self.logger.info("We don't have mapping for db {}. No action taken.".format(p_db))