from time import gmtime, strftime
from enum import Enum

file_name = 'logs.log'

class Log_level(Enum):
    VERBOSE = 5
    DEBUG = 4
    WARN = 3
    STANDARD = 2
    CONCISE = 1

def log(message, log_level):
    with open(file_name, 'a+') as f:
        f.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '[Log level: ' + str(log_level) + '] ' + message + '\n')
