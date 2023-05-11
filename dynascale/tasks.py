from .abstractions import Task, Challenge
import pandas as pd

from dynascale.utils.plotting import plotMetric, plot_target_error, plot_metric
class TargetLoss(Task):
    def __init__(self, N: list[int], L: list[int], E: list[int], T: list[int], control_horizons: int,
                 challenge_cls: type[Challenge], trials: int, test_size: int, target_loss: float):
        self._target_loss = target_loss
        # TODO: Tommy transfer summer code by overloading evaluate if necessary
        super().__init__(N, L, E, T, control_horizons, challenge_cls, trials, test_size)

    def plot(self, data: pd.DataFrame):
        plot_target_error(data, "latent_dim", "n", target_error=self._target_loss)

class FixedComplexity(Task):
    def __init__(self, N: list[int], l: int, E: list[int], T: list[int], control_horizons: int,
                 challenge_cls: type[Challenge], trials: int, test_size: int):
        L = [l] * len(N)
        super().__init__(N, L, E, T, control_horizons, challenge_cls, trials, test_size)

    def plot(self, *data):
        plot_metric(data, x_col="n", y_col="error")


class FixedTrainSize(Task):
    def __init__(self, n: int, L: list[int], E: list[int], T: list[int], control_horizons: int,
                 challenge_cls: type[Challenge], trials: int, test_size: int):
        N = [n] * len(L)
        super().__init__(N, L, E, T, control_horizons, challenge_cls, trials, test_size)

    def plot(self, data: pd.DataFrame):
        plotMetric(data, "latent_dim", "error")