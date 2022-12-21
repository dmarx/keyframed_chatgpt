# please re-implement the `keyframed` library we've been working on here by building on top of the `traces` library

import abc
import traces
import scipy.interpolate
import sortedcontainers

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

# Please modify the `Keyframed` class such that it still uses the `traces` library and `scipy.interpolate`, but such that a user can provide a custom defined callable as a keyframe valuable. Let's assume that the callable must take the keyframe index (k) as the first positional argument, and the Keyframed object itself (parent_kf) as the second positional argument.
class Keyframed:
    def __init__(self, data=None, interp=None, n=None):
        if data is None:
            data = {}
        self._data = sortedcontainers.SortedDict()
        self._interp = sortedcontainers.SortedDict()
        self._interp_func = {}
        self.is_bounded = False
        self.n = n
        if n is not None:
            self.is_bounded = True
        for k, v in data.items():
            self[k] = v
        for k, v in interp.items():
            self.set_interp(k, v)
    
    def __getitem__(self, k):
        if self.is_bounded:
            if k < 0 or k >= self.n:
                raise StopIteration
        if k in self._data:
            return self._data[k]
        if k in self._interp:
            return self._interp_func[k](k, self)
        floor_key = self._data.floor_key(k)
        ceil_key = self._data.ceiling_key(k)
        if floor_key is None and ceil_key is None:
            return 0
        if floor_key is None:
            return self._data[ceil_key]
        if ceil_key is None:
            return self._data[floor_key]
        if floor_key == ceil_key:
            return self._data[floor_key]
        if ceil_key in self._interp:
            return self._interp_func[ceil_key](k, self)
        x = [floor_key, ceil_key]
        y = [self._data[floor_key], self._data[ceil_key]]
        interp_func = scipy.interpolate.interp1d(x, y)
        return interp_func(k)
    
    def __setitem__(self, k, v):
        if isinstance(v, tuple):
            self._data[k] = v[0]
            self.set_interp(k, v[1])
        else:
            self._data[k] = v
            self._interp.pop(k, None)
            self._interp_func.pop(k, None)

    # NB output stopped at setitem and getitem. assuming rest is still kosher.
    
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
    
    @property
    def keyframes(self):
        return self.data.keys()
    


