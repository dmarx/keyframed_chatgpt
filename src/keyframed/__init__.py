# please re-implement the `keyframed` library we've been working on here by building on top of the `traces` library

import abc
import traces

class KeyframedBase(abc.ABC):
    def __init__(self):
        self.is_bounded = False
        self.length = None
    
    def __len__(self):
        return self.length
    
    def set_unbounded(self):
        self.is_bounded = False
        self.length = None
    
    def set_length(self, n):
        self.length = n
        self.is_bounded = True
    
    @abc.abstractmethod
    def __getitem__(self, index):
        pass
    
    @abc.abstractmethod
    def __setitem__(self, index, value):
        pass
    
    @property
    @abc.abstractmethod
    def keyframes(self):
        pass

# NB: request for implementation "using" traces dropped the ABC inheritance
class Keyframed(traces.TimeSeries):
    def __init__(self, data=None, interp=None, n=None):
        if data is None:
            data = {}
        if interp is None:
            interp = {}
        
        self.is_bounded = (n is not None)
        self.interp = interp
        
        # Initialize the TimeSeries with the data and interpolation methods
        super().__init__(data, interp=interp)
        
        if n is not None:
            self.set_length(n)
    
    def __len__(self):
        if self.is_bounded:
            return self.end - self.start
        else:
            return None
    
    def set_length(self, n):
        self.is_bounded = True
        self.end = self.start + n
    
    def set_unbounded(self):
        self.is_bounded = False
        self.end = None
    
    def append(self, other):
        if self.is_bounded or other.is_bounded:
            raise ValueError("Cannot append bounded TimeSeries")
        
        self.update(other)
    
    def __setitem__(self, index, value):
        if self.is_bounded and index >= len(self):
            raise IndexError("Index out of range")
        
        super().__setitem__(index, value)
    
    # NB: ChatGPT dropped this property. Leaving it for now, no idea if it still works
    @property
    def keyframes(self):
        return self.data.keys()
    


