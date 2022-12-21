# please modify this to inherit from a `KeyframedBase` abstract base class which will be used to extend the core API to the Adaptor and Looper classes
import abc
import scipy.interpolate
import sortedcontainers

# please add dunder methods to KeyframedBase and/or Keyframed/Looper to permit basic arithmetic operations between Keyframed objects and scalars, and between Keyframed objects and other Keyframed objects
class KeyframedBase(abc.ABC):
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

    @abc.abstractmethod
    def __getitem__(self, k):
        pass

    @abc.abstractmethod
    def __setitem__(self, k, v):
        pass

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return self.__add_scalar(other)
        if isinstance(other, KeyframedBase):
            return self.__add_kf(other)
        raise TypeError('unsupported operand type(s) for +: Keyframed and {}'.format(type(other)))
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return self.__add_scalar(-other)
        if isinstance(other, KeyframedBase):
            return self.__add_kf(-other)
        raise TypeError('unsupported operand type(s) for -: Keyframed and {}'.format(type(other)))
    
    def __rsub__(self, other):
        return (-self).__add__(other)
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return self.__mul_scalar(other)
        if isinstance(other, KeyframedBase):
            return self.__mul_kf(other)
        raise TypeError('unsupported operand type(s) for *: Keyframed and {}'.format(type(other)))
    
    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return self.__mul_scalar(1 / other)
        if isinstance(other, KeyframedBase):
            return self.__mul_kf(1 / other)
        raise TypeError('unsupported operand type(s) for /: Keyframed and {}'.format(type(other)))
    def __rtruediv__(self, other):
        return self.__rdiv_scalar(other)
    
    def __add_scalar(self, other):
        result = Keyframed(n=self.n)
        result._data = sortedcontainers.SortedDict(self._data)
        result._interp = sortedcontainers.SortedDict(self._interp)
        for k in self._data:
            result._data[k] += other
        return result
    
    def __add_kf(self, other):
        if self.is_bounded != other.is_bounded:
            raise ValueError('Cannot add bounded and unbounded Keyframed objects')
        if self.is_bounded:
            if self.n != other.n:
                raise ValueError('Cannot add Keyframed objects of different lengths')
        result = Keyframed(n=self.n)
        result._data = sortedcontainers.SortedDict(self._data)
        result._interp = sortedcontainers.SortedDict(self._interp)
        for k in other._data:
            if k in result._data:
                result._data[k] += other._data[k]
            else:
                result._data[k] = other._data[k]
        for k in other._interp:
            if k in result._interp:
                raise ValueError('Cannot add Keyframed objects with overlapping keyframes')
            result._interp[k] = other._interp[k]
        return result
    
    def __mul_scalar(self, other):
        result = Keyframed(n=self.n)
        result._data = sortedcontainers.SortedDict(self._data)
        result._interp = sortedcontainers.SortedDict(self._interp)
        for k in self._data:
            result._data[k] *= other




class Keyframed(KeyframedBase):
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
    


