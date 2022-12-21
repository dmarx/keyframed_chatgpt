# please re-implement the `keyframed` library we've been working on here by building on top of the `traces` library

import abc
import traces
import scipy.interpolate

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
# NB: Now ChatGPT dropped all inheritance for this class, but was focused on __getitem__ implementation
#     so let's chalk that up to it being "distracted" and assume the only change is the __getitem__ method.
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
    
    # Please re-implement the `append` method such that 1. both `self` and `other` must be bounded, 2. a new object is returned rather than mutating either `self` or `other`, 3. the length of the returned Keyframed object is `len(self) + len(other)` (satisfying this requirement is why both self and other must be bounded objects)
    # this is a good start, but the indices of the right object in the append should be offset by the length of the left object. Please fix your implementation of the append method to satisfy this or request additional clarification. Respond with working code only, no additional unit tests required
    def append(self, other):
        if not self.is_bounded or not other.is_bounded:
            raise ValueError("Cannot append unbounded TimeSeries")
        
        data = {}
        for i, (t, v) in enumerate(self.items()):
            data[t] = v
        for i, (t, v) in enumerate(other.items()):
            data[t + len(self)] = v
        
        interp = {**self.interp, **other.interp}
        n = len(self) + len(other)
        
        return Keyframed(data, interp=interp, n=n)
    
    # i've noticed that `scipy.interpolate.interp1d` has a lot of useful interpolation methods I'd like to support. please modify your implementation of the Keyframed class to use `scipy.interpolate.interp1d` to perform interpolations between keyframes. respond with working python code which implements the Keyframed class only, no unit tests.
    def __getitem__(self, t):
        if t in self.keyframes:
            return self.data[t]
        
        interp_method = self.interp.get(t, "linear")
        if interp_method == "linear":
            x = list(self.keyframes)
            y = [self.data[x_] for x_ in x]
            f = scipy.interpolate.interp1d(x, y, kind="linear")
            return f(t)
        elif interp_method == "previous":
            x = list(self.keyframes)
            y = [self.data[x_] for x_ in x]
            f = scipy.interpolate.interp1d(x, y, kind="previous")
            return f(t)
        elif interp_method == "next":
            x = list(self.keyframes)
            y = [self.data[x_] for x_ in x]
            f = scipy.interpolate.interp1d(x, y, kind="next")
            return f(t)
        else:
            raise ValueError(f"Invalid interpolation method: {interp_method}")

    def __setitem__(self, index, value):
        if self.is_bounded and index >= len(self):
            raise IndexError("Index out of range")
        
        super().__setitem__(index, value)
    
    # NB: ChatGPT dropped this property. Leaving it for now, no idea if it still works
    @property
    def keyframes(self):
        return self.data.keys()
    


