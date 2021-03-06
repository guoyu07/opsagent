'''
VisualOps agent exceptions
(c) 2014 - MadeiraCloud LTD.

@author: Thibault BRONCHAIN
'''


# Configuration Parser exceptions
class ConfigFileFormatException(Exception): pass
class ConfigFileException(Exception): pass

# Network exceptions
class NetworkConnectionException(Exception): pass

# CLOUD exception
class CLOUDNotFoundException(Exception): pass

# Manager exceptions
class ManagerInvalidStateFormatException(Exception): pass
class ManagerInvalidUpdateFormatException(Exception): pass
class ManagerInvalidWaitFormatException(Exception): pass
class ManagerInvalidStatesRepoException(Exception): pass
class ManagerInvalidStatesCompatException(Exception): pass
class ManagerInitDirDeniedException(Exception): pass

# StatesWorker exceptions
class SWWaitFormatException(Exception): pass
class SWNoManagerException(Exception): pass
class SWNoWaitFileException(Exception): pass

# State exceptions
class StateException(Exception): pass

# Execution exceptions
class ExecutionException(Exception): pass

# General Exception
class OpsAgentException(Exception): pass


# Custom imports
from opsagent.utils import log


# Decorators
def GeneralException(func):
    def __action_with_decorator(self, *args, **kwargs):
        try:
            class_name = self.__class__.__name__
            func_name = func.__name__
            return func(self, *args, **kwargs)
        except Exception as e:
            log("ERROR", "Uncaught error '%s'"%(str(e)),(func_name,class_name))
            raise OpsAgentException(e)
    return __action_with_decorator

def ThrowNoException(func):
    def __action_with_decorator(self, *args, **kwargs):
        try:
            class_name = self.__class__.__name__
            func_name = func.__name__
            return func(self, *args, **kwargs)
        except Exception as e:
            log("ERROR", "Uncaught error '%s'"%(str(e)),(func_name,class_name))
    return __action_with_decorator
