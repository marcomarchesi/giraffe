

from termcolor import colored
import yaml
# import os
import sys
from gdesign_patterns import TODO, Singleton
import logging

'''
logger
'''
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.DEBUG)

fileHandler = logging.FileHandler("neural_rt.log")
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

@TODO("it's not writing to file correctly")
def log(string):
    return logging.debug(colored(string, 'yellow'))




logo = '''
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,/%%%,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,*/(#&&&,,,###(%,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,/#%&@%,,,,(#####,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,((%%%%%##,,,,,,,,,//%&&&&###/#/%#(%,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,*((#%%@&((,,,,,,*(%##%#(%#&&&@%(%&,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,((#%%@@%//(,,,/%%&%#(####%%&@&&&&,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,.*((#&@&&#( ,###%%###(###%%@@@&@@&,,*#&@&&%%###(,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,,,,.//((#(..(#((#%%%%%###%%&&@@@@&&#&@@%%#(///(,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,*%&&&&%%%####%#((#%&@&@&&&&%@&%%#((/,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,.............,,*(,(%##/#//*((((((%&&&&&@%&%%##((,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,........,,*(/**(%#.*,*#(///,////(%%&&&&@@@&@,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,.....,,*(*,,((.#,%#, */********//((%%&&%&/,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,//*,(#%(#,,(%//*#./(/(*.*,*,*/(%%&&%,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,**,,./,/#%##,/%*.*%#&(#**(//..*#(**/#%&%,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,**,..(#(*,/#%%%//&&,*&#*(((*/,(*.(#@@/(#&&&,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,*,,*,../#(.(%###*,#%%%/,%%/**%%(.,*/.,,/(*//((/////,,,,,,,,,,,,,,,,,,,,,,,,,
,,,.*,,,.*#%#*#%%&##****,*,*/(//,,*(#%#(.*///(##//(%###%#*,,,,,,,,,,,,,,,,,,,,,,
,,/.(%#(,,**##%&&%,,(##(**%&&&&**#&&,*,*/(@@#(((#%%&&&%,,,,,,,,,,,,,,,,,,,,,,,,,
(,(#%%%(//(#/**,,,*/%&&&&/#&@&@&%,,,,*/(((@&//%@,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
*#%&&&#/*(%%%#***%(#(#&&&/(%&.,,,,,,((/(%(&%/%%,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
/%%###/*/%&&%/((%&&&%/(#&&,,,,.,,,,.,,%%%&&&&&*,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
/*****/*(((#(((%&&&&&&*,,,,,,,,,,,,,,..,**,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
%%%%%((&@@&&#*/%&@(,,,,,,,,,,,,,,,,,,,,,,,.,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
'''

class Giraffe (Singleton):
    '''
Here to setup the build
    '''
    def __init__(self, logo=False, build=True):
        super().__init__()
        self.build = 0
        self.version = 0
        path = '.giraffe'
        with open(path, 'r+') as f:
            config = yaml.load(f, Loader = yaml.FullLoader)
            self.build = config['build'] + 1
            self.version = config['version']
            config = {'build':self.build,'version':self.version}
        # write the update .giraffe version
        with open(path, 'w+') as f:
            f.write(yaml.dump(config))
        # some more output
        if logo:
            show_logo()
        if build:
            show_build(self)
    
    def update_version(self, version):
        self.version = version
        path = '.giraffe'
        with open(path, 'r+') as f:
            config = yaml.load(f, Loader = yaml.FullLoader)
            config = {'build':self.build,'version':self.version}
        # write the update .giraffe version
        with open(path, 'w+') as f:
            f.write(yaml.dump(config))

def show_logo():
    print(colored(logo, 'yellow'))

def show_build(app):
    print(colored('b{} v{}'.format(app.build, app.version), 'green'))

if __name__ == "__main__":
    # if len(sys.argv) > 1:
    #     giraffe = Giraffe(sys.argv[1])
    pass
