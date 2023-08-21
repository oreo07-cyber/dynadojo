# DynaDojo
DynaDojo is a playground for testing models in dynamical system idenficiation. 

By iteratively adjusting the number of sample and testing performance generalizes, the platform lets you evaluate your model on a growing number of dynamical systems.

## Table of Contents

- [Installation](#installation)
- [Challenges](#challenges)
- [Systems](#systems)
- [Baselines](#baselines)
- [Citing](#citing)
- [License](#license)


## Installation

You can install DynaDojo with `pip`.

```shell
pip install dynadojo
```

# Challenges
## Pre-Built Challenges

`DynaDojo` comes with three off-the-shelf challenges: `FixedError`, `FixedComplexity`, and `FixedTrainSize`. More information about each can be found in the paper.

For demonstrations, please see:
* [Fixed Error]()
* [Fixed Complexity]()
* [Fixed Train Size]()

# Systems

## Adding Systems

To add new systems to `DynaDojo`, you must subclass from `AbstractSystem`. Some skeleton code is provided below.

```python
import numpy as np

from dynadojo.abstractions import AbstractSystem


class MySystem(AbstractSystem):
    def make_init_conds(self, n: int, in_dist=True) -> np.ndarray:
        pass

    def make_data(self, init_conds: np.ndarray, control: np.ndarray, timesteps: int, noisy=False) -> np.ndarray:
        pass

    def calc_error(self, x, y) -> float:
        pass

    def calc_control_cost(self, control: np.ndarray) -> np.ndarray:
        pass

    def __init__(self, latent_dim, embed_dim):
        super().__init__(latent_dim, embed_dim)
```

Documentation for each of the abstract methods can be found in [dynadojo/abstractions](https://github.com/FlyingWorkshop/DynaScale/blob/c62e1abb0275a8c72931bc10177a8ba9a44424f3/dynadojo/dynadojo/abstractions.py). For controlled systems, developers must also implement the `act` method.

To verify that your system works, try using the `tester.py` module.


## Examples
### Example 1: Comparing DNN activations on LDSs

Nonlinearity is a hallmark of modern deep learning; however, there are some exceptional tasks where linear models actually outperform nonlinear neural networks. In this example, we explore this phenomena through linear dynamical systems (LDSs) and deep neural networks (DNNs).

To start, let's create some LDS data using one of DynaDojo's off-the-shelf `LDSSystem`.

```python

import dynadojo as dd
import numpy as np

latent_dim = 5
embed_dim = 10
n = 5000
timesteps = 50
system = dd.systems.LDSSystem(latent_dim, embed_dim)
x0 = system.make_init_conds(n)
y0 = system.make_init_conds(30, in_dist=False)
x = system.make_data(x0, control=np.zeros((n, timesteps, embed_dim)), timesteps=timesteps)
y = system.make_data(y0, control=np.zeros((n, timesteps, embed_dim)), timesteps=timesteps)
dd.utils.lds.plot([x, y], target_dim=min(latent_dim, 3), labels=["in", "out"], max_lines=15)
```

In the image below, observe how the in distribution trajectories (blue) have a different evolution than the out-of-distribution trajectories (orange). A robust model should be able to predict the orange trajectories even if it's only trained on the blue ones.

<p align="center">
<img src="graphics/lds_example1.png">
</p>

Next, let's create our nonlinear model using DynaDojo's baseline `DNN` class.

```python
nonlinear_model = dd.baselines.DNN(embed_dim, timesteps, activation="tanh", max_control_cost=0)
nonlinear_model.fit(x, epochs=10, verbose='auto')
x_pred = nonlinear_model.predict(x[:, 0], 50)
y_pred = nonlinear_model.predict(y[:, 0], 50)
dd.utils.lds.plot([x_pred, y_pred], target_dim=min(3, latent_dim), labels=["in pred", "out pred"], max_lines=15)
x_err = system.calc_error(x, x_pred)
y_err = system.calc_error(y, y_pred)
print(f"{x_err=}")
print(f"{y_err=}")
```

<b>Out:</b>
```
x_err=203.1404201824185
y_err=346.67112531011145
```

As we can see, the model performs pretty badly. With 10 epochs of training, it struggles to predict both the in and out-of-distribution trajectories!

<p align="center">
<img src="graphics/lds_example2.png">
</p>

Next, let's try `DNN` with a linear activation.

```python
linear_model = dd.baselines.DNN(embed_dim, timesteps, activation=None, max_control_cost=0)
linear_model.fit(x, epochs=10, verbose='auto')
x_pred = linear_model.predict(x[:, 0], 50)
y_pred = linear_model.predict(y[:, 0], 50)
dd.utils.lds.plot([x_pred, y_pred], target_dim=min(3, latent_dim), labels=["in pred", "out pred"], max_lines=15)
x_err = system.calc_error(x, x_pred)
y_err = system.calc_error(y, y_pred)
print(f"{x_err=}")
print(f"{y_err=}")
```
<b>Out:</b>
```
x_err=21.46598299085367
y_err=243.8198349312669
```

As we can see, the linear model does much better! This is because linear models learn linear dynamics faster.

<p align="center">
<img src="graphics/lds_example3.png">
</p>

## Citing

Pending

## License

This software is made available under the terms of the MIT license. See LICENSE for details.

The external dependencies used by this software are available under a variety of different licenses. Review these external licenses before using the software.
