#!/usr/bin/python3
# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility
import sys
import os
import re
import logging

knob_debug = False
class LogParser:
    gdict = dict()
    regex = r"(?P<mon>Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s(?P<dd>\d{1,2})\s(?P<hh>\d{2}):(?P<mm>\d{2}):(?P<ss>\d{2})\s(?P<host>\w+)\s(?P<unit>\w+)(\[(?P<pid>\d+)\])?:\s(?P<str>.*)"
    test_str = "Nov 14 11:31:37 geeklab systemd[1]: Stopping user-5006.slice."
    def processLine(self, line):
        cre = re.compile(self.regex)
        #m= cre.match(test_str)
        m= cre.match(line)
        if m is not None:
            pdict = m.groupdict()
            print(pdict['mon'])
            print(pdict)
            print('over')
        else:
            print("boohoo")
def isExistsFile(file_path):
    res = os.path.exists(file_path)
#     print(res)
    return res

def isFileReadable(file_path):
    if os.access(file_path, os.R_OK):
        return True
    else:
        return False
if __name__ == "__main__":

    if knob_debug:
        logging.basicConfig(filename='.debug.log',level=logging.DEBUG)

    # needs at least 1 arg
    if len(sys.argv) < 2:
        logging.error('Usage: ' + str(sys.argv[0]) + ' <file>')
        sys.stderr.write('Usage: ' + str(sys.argv[0]) + ' <file>\n')
        sys.exit(2)

    file_path = sys.argv[1]
    if not isExistsFile(file_path):
        logging.error(sys.argv[0] + ': cannot access ' + file_path + ': No such file')
        sys.stderr.write(sys.argv[0] + ': cannot access ' + file_path + ': No such file\n')
        sys.exit(1)

    if not isFileReadable(file_path):
        logging.error(sys.argv[0] + ': cannot access ' + file_path + ': Cannot read file')
        sys.stderr.write(sys.argv[0] + ': cannot access ' + file_path + ': Cannot read file\n')        
        sys.exit(2)

    lp = LogParser()
    with open(sys.argv[1]) as f:
        for line in f:
            if (line == '\n'):
                pass
            else:  
                res = lp.processLine(line)
