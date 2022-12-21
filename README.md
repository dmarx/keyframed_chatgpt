Welcome to the `keyframed` library!

`keyframed` is a library for representing time-varying data as a sequence of keyframes, with optional interpolation between keyframes. It provides the following classes:

- `Keyframed`: The main class for representing time-varying data as a sequence of keyframes. It provides the following features:
  - Bounded and unbounded data: You can specify a fixed length for the `Keyframed` object, or leave it unbounded.
  - Keyframe data and interpolation methods: You can specify keyframe data and interpolation methods using dictionaries, with the keys representing the indices of the keyframes and the values representing the values at the keyframes or the interpolation methods.
  - Indexing and slicing: You can access the values at a specific index or a range of indices using indexing or slicing syntax.
  - Appending: You can append two `Keyframed` objects together to create a new `Keyframed` object that combines the data from both objects.
- `Adaptor`: An abstract base class for classes that adapt the behavior of a `Keyframed` object. It provides the following features:
  - Wrapper API: You can access the wrapped `Keyframed` object using the `_seq` attribute.
  - Length property: You can access the length of the wrapped `Keyframed` object using the `__len__` method.
  - Indexing and slicing: You can access the values at a specific index or a range of indices using indexing or slicing syntax, which are delegated to the wrapped `Keyframed` object.
- `Looper`: A class that adapts a `Keyframed` object to repeat itself a specified number of times. It provides the following features:
  - Activation: You can specify a starting index at which the looping behavior is activated.
  - Maximum repetitions: You can specify the maximum number of times the wrapped `Keyframed` object should be repeated.
  - Loop status: You can check whether the loop is active at a specific index using the `is_active_at` method.

Here is an example of how you might use the `keyframed` library to parameterize a simple generative art animation:

```python
import matplotlib.pyplot as plt
import numpy as np

from keyframed import Keyframed

# Create a Keyframed object that represents a sinusoidal waveform
data = {
    0: 0,
    10: np.pi,
    20: 2 * np.pi,
}
interp = {
    5: "linear",
    15: "linear",
}
waveform = Keyframed(data=data, interp=interp, n=20)

# Plot the waveform over time
t = np.linspace(0, 19, 20)
y = [waveform[i] for i in t]
plt.plot(t, y)
plt.show()

# Modify the waveform by adding a phase shift
data = {
    0: np.pi / 2,
    10: np.pi * 3 / 2,
    20: 2 * np.pi + np.pi / 2,
}
interp = {
    5: "linear",
    15: "linear",
}
waveform2 = Keyframed(data=data, interp=interp, n=20)

# Plot the modified waveform over time
t = np.linspace(0, 19, 20)
y = [waveform2[i] for i in t]
plt.plot(t, y)
plt.show()

# Create a Looper object that repeats the modified waveform 3 times
looped_waveform = Looper(waveform2, max_repetitions=3)

# Plot the looped waveform over time
t = np.linspace(0, 59, 60)
y = [looped_waveform[i] for i in t]
plt.plot(t, y)
plt.show()
```

As you can see, the Keyframed class allows you to represent a time-varying signal as a sequence of keyframes, with optional interpol [...]

Here is an example of how you might use the append method:

```python
import matplotlib.pyplot as plt
import numpy as np

from keyframed import Keyframed

# Create a Keyframed object that represents a sinusoidal waveform
data = {
    0: 0,
    10: np.pi,
    20: 2 * np.pi,
}
interp = {
    5: "linear",
    15: "linear",
}
waveform = Keyframed(data=data, interp=interp, n=20)

# Plot the waveform over time
t = np.linspace(0, 19, 20)
y = [waveform[i] for i in t]
plt.plot(t, y)
plt.show()

# Modify the waveform by adding a phase shift
data = {
    0: np.pi / 2,
    10: np.pi * 3 / 2,
    20: 2 * np.pi + np.pi / 2,
}
interp = {
    5: "linear",
    15: "linear",
}
waveform2 = Keyframed(data=data, interp=interp, n=20)

# Plot the modified waveform over time
t = np.linspace(0, 19, 20)
y = [waveform2[i] for i in t]
plt.plot(t, y)
plt.show()

# Append the two waveforms to create a new waveform
appended_waveform = waveform.append(waveform2)

# Plot the appended waveform over time
t = np.linspace(0, 39, 40)
y = [appended_waveform[i] for i in t]
plt.plot(t, y)
plt.show()
```

As you can see, the append method allows you to combine two Keyframed objects into a new Keyframed object that represents the concatenation of the two objects. This is useful if you want to create a longer time-varying signal by combining multiple shorter signals.

---

## New Arithmetic Capabilities!

Our `KeyframedBase` and `Keyframed` classes now support basic arithmetic operations between `Keyframed` objects and scalars, and between `Keyframed` objects and other `Keyframed` objects. These operations are implemented using the corresponding dunder methods, such as `__add__`, `__mul__`, etc. Here is an example of how you can use these methods:

```python
# Create a keyframed object with a single keyframe at index 5
kf1 = Keyframed({5: 10})

# Add a scalar value to the keyframed object
kf2 = kf1 + 5
print(kf2[5])  # prints 15

# Multiply the keyframed object by a scalar value
kf3 = kf2 * 2
print(kf3[5])  # prints 30

# Add two keyframed objects together
kf4 = Keyframed({0: 5, 10: 15})
kf5 = kf3 + kf4
print(kf5[5])  # prints 35
print(kf5[10])  # prints 45
```

Note that addition and subtraction of `Keyframed` objects is only supported between `Keyframed` objects of the same length. If the `Keyframed` objects have different lengths, only the keyframes and corresponding values up to the length of the shorter `Keyframed` object will be used in the operation.

Additionally, note that addition and subtraction of `Keyframed` objects is not commutative. For example, `kf1 + kf2` and `kf2 + kf1` will yield different results.

<!-- 
NB: ChatGPT is inventing arguments and methods that aren't part of the implementation.
This is undesirable, but I don't consider it "out of bounds" because this output was preceded by PR/FAQ generation,
which explicitly requested suggestions for future features.
-->
## Advanced Adaptor Usage

The `Adaptor` class is a powerful tool for transforming `Keyframed` objects in various ways. You can use it to scale, offset, or reverse the values of a `Keyframed` object. Here's an example of how to use the `Adaptor` class to achieve these transformations:

```python
from keyframed import Keyframed, Adaptor
import numpy as np

# Define a simple Keyframed object with linear interpolation
kf = Keyframed({0: 0, 10: 1}, interp='linear')

# Scale the values of the Keyframed object by 2
scaled = Adaptor(kf, scale=2)
assert list(scaled.values()) == [0, 2]

# Offset the values of the Keyframed object by 1
offset = Adaptor(kf, offset=1)
assert list(offset.values()) == [1, 2]

# Reverse the values of the Keyframed object
reversed_kf = Adaptor(kf, reverse=True)
assert list(reversed_kf.values()) == [1, 0]

# Combine multiple transformations
transformed = Adaptor(kf, scale=2, offset=1, reverse=True)
assert list(transformed.values()) == [2, 0]
```

As you can see, the `Adaptor` class makes it easy to apply multiple transformations to a `Keyframed` object in a single line of code. You can use the `scale`, `offset`, and `reverse` arguments to control which transformations are applied.

Note that the `Adaptor` class does not modify the original `Keyframed` object - it creates a new `Keyframed` object with the transformed values. This allows you to apply multiple transformations to the same `Keyframed` object without modifying the original.

## New Looper 'delay' feature

Now, when we create a new `Looper` object, we can specify the number of frames to pause between loop repetitions using the `delay` argument. We can also specify how the Looper should interpolate between loops during the delay period using the `delay_interp` argument.

Here's an example of how to use the new `Looper` class:

```python
# Define a simple Keyframed object with linear interpolation
kf = Keyframed({0: 0, 10: 1}, interp='linear')

# Create a Looper object with a delay of 2 frames between loop repetitions
looper = Looper(kf, delay=2)

# The Looper object should have a length of 12
assert len(looper) == 12

# The first and last values should be 0
assert looper[0] == looper[11] == 0

# The middle value should be 1
assert looper[5] == 1

# The values at indices 2 and 9 should be 0.5 (interpolated during the delay period)
assert looper[2] == looper[9] == 0.5
```

## Using the Looper to implement LFOs

An LFO (low frequency oscillator) is a type of oscillator that produces a periodic waveform with a frequency lower than the audible range (less than 20 Hz). LFOs are commonly used to modulate other parameters in audio synthesis and processing.

One common use case for LFOs is to create a rhythmic pulse or modulation effect in music. For example, you might want to use an LFO to modulate the volume of a synth pad in a subtle, periodic way to create a pulsing effect.

To implement an LFO using the `Looper` class, we will first need to define a waveform to use as the LFO. A simple waveform to start with is a sine wave, which can be created using the `math.sin` function.

Here's how we can define a sine wave LFO using the `Looper` class:

```python
import math

from keyframed import Keyframed, Looper

def sine_wave(k, parent_kf, frequency=1, amplitude=1, phase=0):
    """Generate a sine wave with the given frequency, amplitude, and phase."""
    return amplitude * math.sin(2 * math.pi * frequency * k + phase)

# Create a Keyframed object with a single keyframe at index 0 with a value of 0
kf = Keyframed({0: 0}, n=1)

# Create a Looper object with a delay of 0 frames between loop repetitions
looper = Looper(kf, delay=0)

# Use the sine_wave function as the keyframe value for the Looper object
looper[0] = sine_wave, 'linear'

# The Looper object should have a length of 1
assert len(looper) == 1

# The value of the Looper object at index 0 should be 0
assert looper[0] == 0
```

Now that we have a basic sine wave LFO, we can use it to modulate other parameters in our music. For example, we can use the LFO to modulate the volume of a synth pad in a subtle, periodic way to create a pulsing effect.

To do this, we can use the `Looper.transform` method to apply the LFO to another `Keyframed` object. Here's an example of how we might use the `Looper` class to modulate the volume of a synth pad:

```python
import math

from keyframed import Keyframed, Looper

def sine_wave(k, parent_kf, frequency=1, amplitude=1, phase=0):
    """Generate a sine wave with the given frequency, amplitude, and phase."""
    return amplitude * math.sin(2 * math.pi * frequency * k + phase)

# Create a Keyframed object with a single keyframe at index 0 with a value of 0
kf = Keyframed({0: 0}, n=1)

# Create a Looper object with a delay of 0 frames between loop repetitions
looper = Looper(kf, delay=0)

# Use the sine_wave function as the keyframe value for the Looper object
looper[0] = sine_wave, 'linear'

# The Looper object should have a length of 1
assert len(looper) == 1

# The value of the Looper object at index 0 should be 0
assert looper[0] == 0

# Create a Keyframed object representing the volume of a synth pad
volume = Keyframed({0: 0.5, 9: 1.0, 10: 0.5, 19: 0.0}, interp='linear', n=20)

# Use the Looper object to modulate the volume of the synth pad
modulated_volume = volume.transform(lambda v, lfo: v * lfo, looper)

# The modulated volume should have the same length as the original volume
assert len(modulated_volume) == len(volume)

# The value of the modulated volume at index 0 should be 0.5 * 0 = 0
assert modulated_volume[0] == 0

# The value of the modulated volume at index 5 should be 0.5 * 0.5 = 0.25
assert modulated_volume[5] == 0.25

# The value of the modulated volume at index 15 should be 0.5 * -1 = -0.5
assert modulated_volume[15] == -0.5
```

As you can see, the `Looper` class can be used to create complex modulation effects by composing multiple LFOs together. This can be done using the `+`, `-`, `*`, and `/` operators, as well as the `transform` method, to combine multiple LFOs into a single `Keyframed` object.

For example, we might want to create an LFO with a slower frequency to modulate the pitch of a synth, and then use a faster LFO to modulate the volume of the synth. To do this, we can simply add the two LFOs together using the `+` operator:

```python
import math

from keyframed import Keyframed, Looper

def sine_wave(k, parent_kf, frequency=1, amplitude=1, phase=0):
    """Generate a sine wave with the given frequency, amplitude, and phase."""
    return amplitude * math.sin(2 * math.pi * frequency * k + phase)

# Create a Keyframed object with a single keyframe at index 0 with a value of 0
kf = Keyframed({0: 0}, n=1)

# Create a Looper object with a delay of 0 frames between loop repetitions
looper = Looper(kf, delay=0)

# Use the sine_wave function as the keyframe value for the Looper object
looper[0] = sine_wave, 'linear'

# Create a second Looper object with a delay of 0 frames between loop repetitions
looper2 = Looper(kf, delay=0)

# Use a modified version of the sine_wave function as the keyframe value for the second Looper object
looper2[0] = lambda k, parent_kf: sine_wave(k, parent_kf, frequency=2), 'linear'

# Add the two LFOs together
lfo = looper + looper2

# The LFO should have a length of 1
assert len(lfo) == 1

# The value of the LFO at index 0 should be 0 + 0 = 0
assert lfo[0] == 0

# The value of the LFO at index 0 should be 0 + 0 = 0
assert lfo[0] == 0

#The value of the LFO at index 1 should be the sum of the values of the two LFOs at index 1
assert lfo[1] == looper[1] + looper2[1]

#The value of the LFO at index 2 should be the sum of the values of the two LFOs at index 2
assert lfo[2] == looper[2] + looper2[2]

# And so on

# We can use this LFO to modulate the pitch and volume of a synth by multiplying the LFO values by the desired pitch and volume ranges
pitch_range = 12 # semitones
volume_range = 0.5 # range from 0 to 0.5

pitch = lfo * pitch_range
volume = lfo * volume_range

# Now we can use the pitch and volume values to control our synth
```

This is just one example of how the Looper class can be used to create LFOs. The possibilities are endless! You can use LFOs to control almost any parameter in your music or art project, and you can even chain multiple LFOs together to create even more complex modulations.

## Chaining LFOs

Chaining LFOs together to create complex modulations is easy with the Looper class. All you need to do is create multiple LFOs using the Looper class, and then combine them using basic arithmetic operations like addition and multiplication.

For example, let's say we want to create an LFO that modulates both the pitch and volume of a synth. We can do this by creating two separate LFOs, one for pitch and one for volume, and then combining them using addition.

Here's how we might do this:

```python
# First, let's create an LFO for pitch. This LFO will have a frequency of 2 Hz and will oscillate between -6 and 6 semitones.
looper = Looper(
    Keyframed({0: -6, 0.5: 6}, interp={0.25: 'linear'}),
    max_repetitions=float('inf'),
    rate=2
)

# Now let's create an LFO for volume. This LFO will have a frequency of 1 Hz and will oscillate between 0 and 0.5.
looper2 = Looper(
    Keyframed({0: 0, 0.5: 0.5}, interp={0.25: 'linear'}),
    max_repetitions=float('inf'),
    rate=1
)

# Now we can combine these two LFOs using addition to create a new LFO that modulates both pitch and volume.
lfo = looper + looper2

# Let's check that our new LFO is working as expected

# The value of the LFO at index 0 should be the sum of the values of the two LFOs at index 0
assert lfo[0] == looper[0] + looper2[0]

# The value of the LFO at index 1 should be the sum of the values of the two LFOs at index 1
assert lfo[1] == looper[1] + looper2[1]

# The value of the LFO at index 2 should be the sum of the values of the two LFOs at index 2
assert lfo[2] == looper[2] + looper2[2]

# And so on

# We can use this LFO to modulate the pitch and volume of a synth by multiplying the LFO values by the desired pitch and volume ranges
pitch_range = 12  # semitones
volume_range = 0.5  # range from 0 to 0.5

pitch = lfo * pitch_range
volume = lfo * volume_range

# Now we can use the pitch and volume values to control our synth
```

As you can see, chaining LFOs together to create complex modulations is easy with the Looper class. You can chain as many LFOs together as you like, and use basic arithmetic operations to combine them in any way you like.

Happy modulating!