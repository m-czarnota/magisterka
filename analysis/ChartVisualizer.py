import itertools
import os

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Patch
from unidecode import unidecode
import random

from ChartTypeEnum import ChartTypeEnum
from ChartParams import ChartParams


class ChartVisualizer:
    images_dir = './results/images'
    pdf_dir = './results/pdf'

    @staticmethod
    def visualize(chart_type: ChartTypeEnum, chart_params: ChartParams, save: bool = False, sub_dir: str = None) -> None:
        plt.figure(figsize=chart_params.fig_size)
        plt.rcParams.update({'font.size': 14})
        ChartVisualizer.__draw_chart(chart_type, chart_params)

        plt.title(chart_params.fig_title)
        plt.xlabel(chart_params.x_label)
        plt.ylabel(chart_params.y_label)

        if chart_params.x_label_rotation is not None:
            plt.xticks(rotation=chart_params.x_label_rotation, ha='right')

        if chart_params.classes is not None:
            plt.legend()

        if not save:
            plt.show()

            return

        filename = 'result.png'
        sub_dir = f'/{sub_dir}' if sub_dir is not None else ''
        sub_dir = sub_dir.replace("_", "-").replace("favourite", "fav")

        image_dir_path = f'{ChartVisualizer.images_dir}{sub_dir}'
        if not os.path.exists(image_dir_path):
            os.makedirs(image_dir_path)

        pdf_dir_path = f'{ChartVisualizer.pdf_dir}{sub_dir}'
        if not os.path.exists(pdf_dir_path):
            os.makedirs(pdf_dir_path)

        if chart_params.fig_title:
            filename = ChartVisualizer.save_encode_filename(chart_params.fig_title)

        plt.savefig(f'{image_dir_path}/{filename}')
        plt.savefig(f'{pdf_dir_path}/{filename.replace("png", "pdf")}', format="pdf", bbox_inches="tight")

    @staticmethod
    def __draw_chart(chart_type: ChartTypeEnum, chart_params: ChartParams) -> None:
        x = chart_params.x
        y = chart_params.y
        colors, labels = ChartVisualizer.__generate_colors_amd(chart_params.classes.to_numpy()) if chart_params.classes is not None else (None, None)

        if chart_type == ChartTypeEnum.BAR:
            x = list(map(str.capitalize, x))

            if colors is not None:
                # not working, not labels. works probably with axis
                uniques_colors = np.unique(colors)
                rgb_colors = ChartVisualizer.__get_random_colors(len(uniques_colors))

                bars = plt.bar(x, y, width=chart_params.bar_width, color=rgb_colors._segmentdata)

                handles = [plt.Rectangle((0, 0), 1, 1, color=rgb_color) for rgb_color in rgb_colors._segmentdata]
                plt.legend(handles, labels)
            else:
                bars = plt.bar(x, y, width=chart_params.bar_width)

            if chart_params.y_val_bar_label:
                max_height = np.max([bar.get_height() for bar in bars])

                for bar in bars:
                    plt.text(
                        bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + max_height * 0.01,
                        round(bar.get_height(), 1),
                        horizontalalignment='center',
                    )

            return

        if chart_type == ChartTypeEnum.SCATTER:
            if colors is not None:
                uniques_colors = np.unique(colors)
                rgb_colors = ChartVisualizer.__get_random_colors(len(uniques_colors))
                symbols = itertools.cycle(('.', 'o', '1', '2', 'h', 's', 'p', 'P', '*', 'x', 'D', '+', 'X', 'v', '^'))

                for color_unique in np.unique(colors):
                    values = y[color_unique == colors]

                    plt.scatter(x[color_unique == colors], values, color=rgb_colors(color_unique),
                                label=labels[color_unique == colors][0], marker=next(symbols),
                                edgecolors='black' if chart_params.line_in_mean else None)

                    if chart_params.line_in_mean:
                        plt.plot(np.linspace(np.min(x), np.max(x), values.shape[0]), np.full(values.shape[0], np.mean(values)), color=rgb_colors(color_unique))
                        plt.plot(np.linspace(np.min(x), np.max(x), values.shape[0]), np.full(values.shape[0], np.median(values)), color=rgb_colors(color_unique), linestyle='dashed')
            else:
                plt.scatter(x, y, c=colors, cmap=plt.get_cmap('rainbow'), edgecolors='black' if chart_params.line_in_mean else None)

                if chart_params.line_in_mean:
                    plt.plot(np.mean(chart_params.y))
                    plt.plot(np.median(chart_params.y), linestyle='dashed')

            return

        plt.plot(x, y)

    @staticmethod
    def save_encode_filename(title: str) -> str:
        title = title.replace(' ', '_')
        title = unidecode(title)

        return f"{title}.png"

    @staticmethod
    def __generate_colors_amd(class_labels: np.array):
        colors = np.empty(len(class_labels), dtype=int)
        labels = np.empty_like(colors, dtype=object)
        classes_number = {}

        for class_type_iter, class_type in enumerate(class_labels):
            if class_type not in classes_number.keys():
                classes_number[class_type] = len(classes_number)

            colors[class_type_iter] = classes_number[class_type]
            labels[class_type_iter] = class_type

        return colors, labels

    @staticmethod
    def __get_random_colors(n: int) -> np.array:
        # return np.array(["#%06x" % random.randint(0, 0xFFFFFF) for _ in range(n)])
        return plt.cm.get_cmap('rainbow', n)
