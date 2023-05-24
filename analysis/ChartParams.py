from typing import Iterable

import numpy as np


class ChartParams:
    def __init__(self, x: np.array, y: np.array, fig_size: tuple = None, fig_title: str = None,
                 x_label: str = None, y_label: str = None, x_label_rotation: int = None, bar_width: float = 0.8,
                 y_val_bar_label: bool = True, classes: np.array = None, line_in_mean: bool = False):
        self.x = x
        self.y = y
        self.fig_size = fig_size
        self.fig_title = fig_title
        self.x_label = x_label
        self.y_label = y_label
        self.x_label_rotation = x_label_rotation
        self.bar_width = bar_width
        self.y_val_bar_label = y_val_bar_label
        self.classes = classes
        self.line_in_mean = line_in_mean
