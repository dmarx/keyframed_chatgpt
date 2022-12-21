# ChatGPT didn't request this import, but I haven't been explicit to it about how the
# package is structured so it's not cheating that much.
from keyframed import KeyframedBase

class Adaptor(KeyframedBase):
    def __init__(self, seq):
        super().__init__()
        self._seq = seq
    
    def __getitem__(self, index):
        return self._seq[index]
    
    def __setitem__(self, index, value):
        raise NotImplementedError
    
    @property
    def keyframes(self):
        return self._seq.keyframes


class Looper(Adaptor):
    def __init__(self, seq, max_repetitions=float('inf'), activate_at=0):
        super().__init__(seq)
        self.max_repetitions = max_repetitions
        self.activate_at = activate_at
        if max_repetitions != float('inf'):
            self.is_bounded = True
        else:
            self.is_bounded = False

    def __len__(self):
        if self.is_bounded:
            return len(self._seq) * self.max_repetitions
        else:
            return None

    def __getitem__(self, index):
        if self.is_bounded:
            return self._seq[index % len(self._seq)]
        else:
            return self._seq[index]

    def __setitem__(self, index, value):
        raise NotImplementedError

    @property
    def keyframes(self):
        return self._seq.keyframes

    def is_active_at(self, index):
        if self.is_bounded:
            return index >= self.activate_at and index < self.activate_at + len(self)
        else:
            return index >= self.activate_at