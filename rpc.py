import pexpect, string, random
from timeout import timeout

class rpc:

    @timeout(100)
    def _exec(self, cmd, p_expect):
        if p_expect is not None:
            what_to_expect = p_expect
        else:
            what_to_expect = self.CMDLINE

        self.logger.debug("Executing command: {}".format(cmd))
        if what_to_expect is not None:
            self.logger.debug("Changing expectations: {}".format(what_to_expect))
            p_expect = self.CMDLINE
        self.conn.sendline(cmd)
        self.logger.debug("Current expectation: {}".format(what_to_expect))
        self.conn.expect(what_to_expect)
        res = self.conn.before
        return res

    @timeout(100)
    def _connect(self, host):
        try:
           res = pexpect.spawn("ssh oracle@{}".format(host), timeout=10, maxread=10000000, searchwindowsize=20000)
           return res
        except :
            self.logger.critical("Can't connect to host: {}".format(item[0]))
            return None


    def __init__(self, p_params, logger):
        self.CMDLINE = r"\[PEXPECT\]\$"
        self.SQLLINE = r"SQL>"
        self.TERMINAL_TYPE = 'vt100'
        self.logger = logger
        self.conn = None
        self.connected = False
        self.logger.debug("Connection parameters are: {}".format(p_params))
        self.hostname = None
        self.pmon = None
        self.USERNAME= "testunlock"
        for item in p_params:
            # let's try to spawn session to any of hosts
            self.hostname = item[0]
            self.pmon = item[1]
            self.logger.debug("Connecting to host: {}".format(self.hostname))
            self.conn = self._connect(self.hostname)
            if self.conn is not None:
                self.conn.logfile = open("pexpect.log", "w")
                self.logger.debug("Setting command line for expect")
                self.conn.sendline("PS1=" + self.CMDLINE)
                self.conn.expect(self.CMDLINE)
                self.connected = True
                break
        if not self.connected:
            self.logger.critical("Can't connect to ANY of the hosts, please check if hosts alive or mapping is correct.")
            exit(-1)

    def _genPass(self, pass_len=8):
        characters = string.ascii_letters + string.digits
        first = random.choice(string.ascii_letters)
        return first + ''.join(random.choice(characters) for i in range(pass_len-1))

    def proceed_changes(self, p_unlock, p_reset):
        prepare_sql_plus = ['set heading off', 'set echo off']
        sql2run = "alter user {} account unlock".format(self.USERNAME)
        new_pass = self._genPass()
        try:
            if p_unlock:
                self.logger.info("Changes are: UNLOCK")
                sql2run +=":"
            elif p_reset:
                self.logger.info("Changes are: RESET")
                sql2run += " identified by {};".format(new_pass)
            else:
                self.logger.critical("Not sure what to do, talk to developer.")
                exit(-1)
            self._exec(". oraenv", "ORACLE_SID")
            self._exec(self.pmon, None)
            self._exec("sqlplus / as sysdba", self.SQLLINE)
            for ln in prepare_sql_plus:
                self._exec(ln, self.SQLLINE)
            res = self._exec(sql2run, self.SQLLINE)
            self.logger.debug(res)
            self._exec("exit;", self.CMDLINE)
            self.logger.info("User new password is: {}".format(new_pass))
        except:
            self.logger.critical("Exception in proceed_changes. Please review log file.")