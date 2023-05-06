from matplotlib import pyplot as plt
from unidecode import unidecode

from ChartParams import ChartParams


class ChartVisualizer:
    results_dir = './results/images'

    @staticmethod
    def bar(chart_params: ChartParams, save: bool = False) -> None:
        plt.figure(figsize=chart_params.fig_size)
        plt.bar(chart_params.x, chart_params.y)

        plt.title(chart_params.fig_title)
        plt.xlabel(chart_params.x_label)
        plt.ylabel(chart_params.y_label)

        if chart_params.x_label_rotation is not None:
            plt.xticks(rotation=chart_params.x_label_rotation, ha='right')

        if not save:
            plt.show()

            return

        filename = 'result.png'

        if chart_params.fig_title:
            title = chart_params.fig_title.replace(' ', '_')
            title = unidecode(title)
            filename = f"{title}.png"

        plt.savefig(f'{ChartVisualizer.results_dir}/{filename}')

