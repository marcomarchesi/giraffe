

from termcolor import colored
import yaml
import os
import sys
import time
from functools import wraps
import inspect

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

# decorators
def TODO(arg1):
    def inner_function(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            name = func.__name__
            print("TODO: " + colored("{}".format(name), 'magenta') + 
                    colored(" {}".format(arg1),'yellow'))
            values = func(*args, **kwargs)
            return values
        return wrapper
    return inner_function

def todo(original_class):
    orig_init = original_class.__init__
    # Make copy of original __init__, so we can call it without recursion

    def __init__(self, *args, **kws):
        name = self.__class__.__name__
        print("TODO: " + colored("{}".format(name), 'magenta'))
        orig_init(self, *args, **kws) # Call the original __init__

    original_class.__init__ = __init__ # Set the class' __init__ to the new one
    return original_class


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        value = func(*args, **kwargs)
        print("Elapsed time: {:.2f}s.".format(time.time() - start_time))
        return value
    return wrapper

class Giraffe:
    '''
Here to setup the build
    '''
    @TODO("make it a singleton")
    def __init__(self):
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
    
    def update_version(self, version):
        self.version = version
        path = '.giraffe'
        with open(path, 'r+') as f:
            config = yaml.load(f, Loader = yaml.FullLoader)
            config = {'build':self.build,'version':self.version}
        # write the update .giraffe version
        with open(path, 'w+') as f:
            f.write(yaml.dump(config))

def show_logo(build, version):
    print(colored(logo, 'yellow'))

def show_build(app):
    print(colored('b{} v{}'.format(app.build, app.version), 'green'))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        giraffe = Giraffe(sys.argv[1])
