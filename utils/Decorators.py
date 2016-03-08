# -*- coding: utf-8 -*-



def Singleton(class_):
    """
    Create a Singleton class by using @Singleton
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