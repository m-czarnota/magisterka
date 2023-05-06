import numpy as np


class ChartParams:
    def __init__(self, x: np.array, y: np.array, fig_size: tuple = None, fig_title: str = None,
                 x_label: str = None, y_label: str = None, x_label_rotation: int = None):
        self.x = x
        self.y = y
        self.fig_size = fig_size
        self.fig_title = fig_title
        self.x_label = x_label
        self.y_label = y_label
        self.x_label_rotation = x_label_rotation
