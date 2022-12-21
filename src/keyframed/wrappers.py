# ChatGPT didn't request this import, but I haven't been explicit to it about how the
# package is structured so it's not cheating that much.
from keyframed import KeyframedBase

# Please reimplement the Adaptor and Looper classes to use your most recent versions of the KeyframedBase and Keyframed classes.
class Adaptor(KeyframedBase):
    def __init__(self, parent_kf):
        self.parent_kf = parent_kf
    
    def __getitem__(self, k):
        return self.parent_kf[k]
    
    def __setitem__(self, k, v):
        self.parent_kf[k] = v


class Looper(Adaptor):
    def __init__(self, parent_kf, max_repetitions=float('inf'), activate_at=0):
        super().__init__(parent_kf)
        self.max_repetitions = max_repetitions
        self.activate_at = activate_at
    
    def is_active_at(self, k):
        if k < self.activate_at:
            return False
        n_repetitions = (k - self.activate_at) // len(self.parent_kf)
        return n_repetitions <= self.max_repetitions
    
    def __getitem__(self, k):
        if not self.is_active_at(k):
            raise StopIteration
        return self.parent_kf[k % len(self.parent_kf)]
