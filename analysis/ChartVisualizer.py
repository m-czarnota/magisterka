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
    def visualize(chart_type: ChartTypeEnum, chart_params: ChartParams, save: bool = False) -> None:
        plt.figure(figsize=chart_params.fig_size)
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

        if chart_params.fig_title:
            title = chart_params.fig_title.replace(' ', '_')
            title = unidecode(title)
            filename = f"{title}.png"

        plt.savefig(f'{ChartVisualizer.images_dir}/{filename}')
        plt.savefig(f'{ChartVisualizer.pdf_dir}/{filename.replace("png", "pdf")}', format="pdf", bbox_inches="tight")

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

                for color_unique in np.unique(colors):
                    plt.scatter(x[color_unique == colors], y[color_unique == colors], color=rgb_colors(color_unique),
                                label=labels[color_unique == colors][0], cmap=plt.get_cmap('magma'))
            else:
                plt.scatter(x, y, c=colors, cmap=plt.get_cmap('rainbow'))

            return

        plt.plot(x, y)

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
