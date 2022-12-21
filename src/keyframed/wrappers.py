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


# I like your suggestions for future improvements: please modify the `Looper` class to have the ability to add a delay or pause between loop repetitions. Give the user the ability to parameterize how the Looper interpolates between loops during that pause/delay, defaulting to 'previous' as usual
# NB: New implementation doesn't inherit from Adaptor, possibly for the better.
class Looper(Keyframed):
    def __init__(self, keyframed, max_repetitions=float('inf'), activate_at=0, delay=0, delay_interp='previous'):
        super().__init__()

        self.keyframed = keyframed
        self.max_repetitions = max_repetitions
        self.activate_at = activate_at
        self.delay = delay
        self.delay_interp = delay_interp

        # Initialize the internal loop counter
        self.current_repetition = 0

        # Initialize the internal keyframe index
        self.current_keyframe_index = 0

        # Calculate the length of the Looper object
        self.length = self.calculate_length()

    def calculate_length(self):
        # Calculate the length of the base Keyframed object
        base_length = len(self.keyframed)

        # Calculate the total number of repetitions
        total_repetitions = self.max_repetitions

        # Calculate the total number of frames in the delay periods
        total_delay_frames = self.delay * (total_repetitions - 1)

        # Calculate the total length of the Looper object
        total_length = base_length * total_repetitions + total_delay_frames

        return total_length

    # ChatGPT dropped this method. no parent_kf attr, commenting out for now.    
    # def is_active_at(self, k):
    #     if k < self.activate_at:
    #         return False
    #     n_repetitions = (k - self.activate_at) // len(self.parent_kf)
    #     return n_repetitions <= self.max_repetitions


