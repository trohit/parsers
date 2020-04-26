/usr/bin/python3.7
# hoping you have aliased python to python3.7
# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility
import sys
import os
import re

knob_debug = False
class LogParser:
    line_num = 0
    gdict = dict()
    date = None
    nas_mem = None
    regex = r"(?P<date>(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{1,2}\s\d{2}:\d{2}:\d{2})\.\d{6}\s(?P<host>[a-zA-Z0-9]*)-(?P<nodeid>[A|B])\sblackbox.*CONTAINER ID.*PIDS$"
    #regex_dr = r"^\s+(?P<drid>\w+)\s+(?P<drname>\w+)\s+(?P<cpupct>\d+\.\d*)%\s+(?P<curmem>\d+\.\d*)\w+\s+/\s+(?P<maxmem>\d+.\d*)\w+\s+(?P<mempct>\d+.\d*)%\s+(?P<netrx>\d+.\d*)\s+/\s+(?P<nettx>\d+.\d*)\s+(?P<blkrx>\d+.\d*)\w+\s+/\s(?P<blktx>\d+.\d*)\w+\s+(?P<pids>\d+$)"
    # for some strange reason, BSC docker does not print block i/o and pids
    regex_dr = r"^\s+(?P<drid>\w+)\s+(?P<drname>\w+)\s+(?P<cpupct>\d+\.\d*)%\s+(?P<curmem>\d+\.\d*)\w+\s+/\s+(?P<maxmem>\d+.\d*)\w+\s+(?P<mempct>\d+.\d*)%\s+(?P<netrx>\d+.\d*)\s+/\s+(?P<nettx>\d+.\d*).*$"
#    test_str = "Apr 06 19:45:14.189868 snoopy-B dockermon[68339]: CONTAINER ID        NAME                CPU %               MEM USAGE / LIMIT     MEM %               NET I/O             BLOCK I/O           PIDS
    cre = None
    cre_dr = None
    first_time = True
    fields = ["cpupct","curmem","mempct","netrx","nettx","blkrx","blktx","pids"]

    def __init__(self):
        self.cre = re.compile(self.regex)
        self.cre_dr = re.compile(self.regex_dr)

    def processLine(self, line, docker_id, attr):
        self.line_num += 1
        m= self.cre.match(line)
        m_dr = self.cre_dr.match(line)

        if m is not None:
            #print("blackbox:matched line:" + str(self.line_num))
            pdict = m.groupdict()
#            print(pdict)
            self.date = pdict["date"]

        if m_dr is not None:
            pdict = m_dr.groupdict()
            pdict["date"] = self.date
            #print(str(docker_id) + " found : " + str(pdict) + ":matched line:" + str(self.line_num))
#            print(pdict)
            #if pdict["drname"] == "cyc_nas_docker":
            if docker_id is None or pdict["drname"] == docker_id:
                if self.first_time:
                    if attr == None:
                        # print all fields
                        #print("date,drname, cpupct,curmem,mempct,netrx,nettx,blkrx,blktx,pids")
                        #print("date,drname,cpupct,curmem,maxmem,mempct,netrx,nettx")
                        print("date,drname,cpupct,curmem,maxmem,mempct")
                    else:
                        print("date," + attr)
                    self.first_time = False

                # print values
                if attr == None:
                    print(self.date + \
                            "," + pdict["drname"] +\
                            "," + pdict["cpupct"] +\
                            "," + pdict["curmem"] +\
                            "," + pdict["maxmem"] +\
                            "," + pdict["mempct"])
                            #"," + pdict["nettx"] +\
                            #"," + pdict["blkrx"] +\
                            #"," + pdict["blktx"] +\
                            #"," + pdict["pids"])
                else:
                    print("unsupported")
                    self.nas_mem = pdict[attr]
                    print(self.date + "," + str(self.nas_mem))

#        else:
#            print(str(self.line_num) + line + " duck dr\n")
#            return

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
    # default options
    #docker_id = "cyc_nas_docker"
    #attr = "mempct"
    docker_id = None
    attr = None

    # needs at least 1 arg
    if len(sys.argv) < 2:
        sys.stderr.write('Usage: ' + str(sys.argv[0]) + ' <file> [docker_name] [cpupct|curmem|mempct|netrx|nettx|blkrx|blktx|pids]\n')
        sys.exit(2)

    file_path = sys.argv[1]
    #print("file_path:" + file_path)
    #print(str(len(sys.argv)))
    #import pdb; pdb.set_trace()
    if len(sys.argv) > 2:
        docker_id = sys.argv[2]
        #print("docker_id:" + str(docker_id))

    if len(sys.argv) > 3:
        attr = sys.argv[2]
        print("attr:" + str(attr))

    if not isExistsFile(file_path):
        sys.stderr.write(sys.argv[0] + ': cannot access ' + file_path + ': No such file\n')
        sys.exit(1)

    if not isFileReadable(file_path):
        sys.stderr.write(sys.argv[0] + ': cannot access ' + file_path + ': Cannot read file\n')
        sys.exit(2)

    lp = LogParser()
    with open(file_path) as f:
        for line in f:
            if (line == '\n'):
                pass
            else:
                #print(line)
                res = lp.processLine(line, docker_id, attr)
