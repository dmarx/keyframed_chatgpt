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