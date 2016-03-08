# -*- coding: utf-8 -*-
import os
import sys
import warnings
import functools
import inspect



BASEPATH = os.path.dirname(sys.argv[0])



def singleton(class_):
    """
    @singleton
    class
    
    Create a Singleton class
    """
    
    class class_w(class_):
        
        _instance = None
        
        def __new__(class_, *args, **kwargs):
            
            if class_w._instance is None:
                class_w._instance = super(class_w,
                                          class_).__new__(class_, 
                                                          *args, 
                                                          **kwargs)
                class_w._instance._sealed = False
            return class_w._instance
            
            
        def __init__(self, *args, **kwargs):
            
            if self._sealed:
                return
            super(class_w, self).__init__(*args, **kwargs)
            self._sealed = True
            
            
    class_w.__name__ = class_.__name__
    return class_w
    
    
    
    
def toStr(obj):
    
    if isinstance(obj, str):
        return "'"+obj+"'"
    else:
        return str(obj)
    
    
def log(func_):
    """
    @log
    function(*args, **kwargs)
    
    Write the function to a log file
    """
    
    def wrapper(*args, **kwargs):
        otp = func_(*args, **kwargs)
        argsStrLst = []
        for arg in args:
            argsStrLst.append(toStr(arg))
        for name, kwarg in kwargs.items():
            argsStrLst.append(name+"="+toStr(kwarg))
        argStr = ", ".join(argsStrLst)
        inf = "[Module: "+func_.__module__+"]" if "__module__" in dir(func_) else ""
        if inf != "":
            inf += " "*(30-len(inf))
        fun = func_.__name__+"("+argStr+")"
        logstring = inf+fun
        print(logstring)
        logfile = open(BASEPATH+"/log.txt", "a")
        logfile.write(logstring+"\n")
        logfile.close()
        return otp
    
    wrapper.__name__ = func_.__name__
    wrapper.__doc__ = func_.__doc__
    wrapper.__dict__.update(func_.__dict__)
    return wrapper
    
    
    
    
    
def deprecated(func_):
    """
    @deprecated
    function(*args, **kwargs)
    
    Write out a warnng if a marked function is used.
    """
    
    @functools.wraps(func_)
    def wrapper(*args, **kwargs):
        warnings.warn_explicit("Call to deprecated function "+func_.__name__,
                               category=DeprecationWarning,
                               filename=func_.func_code.co_filename,
                               lineno=func_.code.co_firstlineno+1)
        return func_(*args, **kwargs)
        
    wrapper.__name__ = func_.__name__
    wrapper.__doc__ = func_.__doc__
    wrapper.__dict__.update(func_.__dict__)
    return wrapper
    
    
    
    
    
def ignore_deprecation_warnings(func_):
    """
    @ignore_deprecation_warnings
    function(*args, **kwargs)
    
    Catch any deprecation warnngs of the marked function.
    """
    
    def wrapper(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            return func_(*args, **kwargs)
            
    wrapper.__name__ = func_.__name__
    wrapper.__doc__ = func_.__doc__
    wrapper.__dict__.update(func_.__dict__)
    return wrapper
    
    
    
    
    
def accepts(*argtypes, **kwargtypes):
    """
    @accepts(*argtypes, **kwargtypes)
    function(*args, **kwargs)
    
    Define which types are accepted by a function.
    Each argument of the function needs to have a partner in the decorator's arguments.
    Tuples may be given as an argument, if multiple types are allowed.
    """
    
    def wrap(func_):
        
        def wrapper(*args, **kwargs):
            if inspect.getargspec(func_)[0][0] == "self":
                toCheck = args[1:]
            else:
                toCheck = args
            for arg, argtype in zip(toCheck, argtypes):
                if not issubclass(arg.__class__, argtype):
                    raise TypeError("Wrong argument: Expected "+str(argtype.__name__)+", got "+str(arg.__class__.__name__))
            for key in kwargs.keys():
                if key in kwargtypes:
                    if not issubclass(kwargs[key].__class__, kwargtypes[key]):
                        raise TypeError("Wrong argument: Expected "+str(kwargtypes[key].__name__)+", got "+str(kwargs[key].__class__.__name__))
            return func_(*args, **kwargs)
            
        wrapper.__name__ = func_.__name__
        wrapper.__doc__ = func_.__doc__
        wrapper.__dict__.update(func_.__dict__)
        return wrapper
    return wrap
    
    
    
    
if __name__ == "__main__":
    
    pass