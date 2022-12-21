class Keyframed:
    def __init__(self, data=None, interp=None, n=None):
        if data is None:
            data = {0: 0}
        if interp is None:
            interp = {}
        self.data = data
        self.interp = interp
        self.is_bounded = True if n is not None else False
        self.length = n
    
    def __len__(self):
        return self.length
    
    def set_unbounded(self):
        self.is_bounded = False
        self.length = None
    
    def set_length(self, n):
        self.length = n
        self.is_bounded = True
    
    def __getitem__(self, index):
        if index < 0 or (self.is_bounded and index >= self.length):
            raise StopIteration
        if index in self.data:
            return self.data[index]
        sorted_keys = sorted(self.data.keys())
        i = 0
        while i < len(sorted_keys) and sorted_keys[i] < index:
            i += 1
        prev_key = sorted_keys[i-1]
        next_key = sorted_keys[i]
        prev_val = self.data[prev_key]
        next_val = self.data[next_key]
        if prev_key in self.interp:
            interp_type = self.interp[prev_key]
        else:
            interp_type = 'linear'
        if interp_type == 'previous':
            return prev_val
        elif interp_type == 'next':
            return next_val
        elif interp_type == 'linear':
            slope = (next_val - prev_val) / (next_key - prev_key)
            return prev_val + slope * (index - prev_key)
    
    def __setitem__(self, index, value):
        self.data[index] = value[0]
        if len(value) > 1:
            self.interp[index] = value[1]
    
    def append(self, other):
        if self.is_bounded or other.is_bounded:
            raise ValueError("Cannot append a bounded Keyframed object")
        self.data.update(other.data)
        self.interp.update(other.interp)
        self.length = None
    
    @property
    def keyframes(self):
        return self.data.keys()
