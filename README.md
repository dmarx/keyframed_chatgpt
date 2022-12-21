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
