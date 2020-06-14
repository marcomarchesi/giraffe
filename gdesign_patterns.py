'''
gdesign_patterns.py
'''
import time
from functools import wraps
import inspect
from termcolor import colored

# singleton
class Singleton:
   __instance = None
   @staticmethod 
   def getInstance():
      ''' Static access method. '''
      if Singleton.__instance == None:
         Singleton()
      return Singleton.__instance
   def __init__(self):
      ''' Virtually private constructor. '''
      if Singleton.__instance != None:
         raise Exception(colored('This is a singleton!', 'red'))
      else:
         Singleton.__instance = self

# decorators
def TODO(message):
    def inner_function(func):
        if inspect.isclass(func):
            orig_init = func.__init__
            # Make copy of original __init__, so we can call it without recursion
            def __init__(self, *args, **kws):
                name = self.__class__.__name__
                print("TODO: " + colored("{}".format(name), 'magenta') + 
                colored(" {}".format(message),'yellow'))
                orig_init(self, *args, **kws) # Call the original __init__
            func.__init__ = __init__ # Set the class' __init__ to the new one
            return func
        else:
            @wraps(func)
            def wrapper(*args, **kwargs):
                name = func.__name__
                print("TODO: " + colored("{}".format(name), 'magenta') + 
                        colored(" {}".format(message),'yellow'))
                values = func(*args, **kwargs)
                return values
            return wrapper
    return inner_function

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        value = func(*args, **kwargs)
        print("Elapsed time: {:.2f}s.".format(time.time() - start_time))
        return value
    return wrapper