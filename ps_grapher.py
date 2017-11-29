import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

import time
import datetime
from subprocess import check_output
import sys
import os


class PsGrapher:

    def __init__(self, iterations=None, time_interval=60):
        self.ps_data = {}
        self.graph_data = {}
        self.time_interval = time_interval  # seconds
        self.iterations = iterations
        self.output_filename = "MemoryUsage.html"

    def _get_iterations(self, count):
        if self.iterations is None:
            return True
        elif count <= self.iterations:
            return True
        else:
            return False

    def get_ps_output(self):
        output = [item.lstrip().rstrip() for item in check_output(
            "ps -e -o pid,%cpu,%mem,rss,command --sort -rss".split(" ")).split("\n")]
        output.pop(0)
        new = [a.split() for a in output[:10] if a]
        newer = [[x[0], x[1], x[2], x[3], " ".join(x[4:])] for x in new]
        return newer

    def _create_layout(self, title):
        return dict(
            title=title,
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(
                            count=1,
                            label='1 min',
                            step='minute',
                            stepmode='backward'
                        ),
                        dict(
                            count=1,
                            label='1 hour',
                            step='hour',
                            stepmode='backward'
                        ),
                        dict(
                            count=1,
                            label='1 day',
                            step='day',
                            stepmode='backward'
                        ),
                        dict(step='all')
                    ])
                ),
                rangeslider=dict(),
                type='date',
                tickformat='%H:%M:%S'
            )
        )

    def run(self):
        i = 0
        while self._get_iterations(i):
            date = datetime.datetime.now()
            for row in self.get_ps_output():
                pid, cpu_percentage, mem_percentage, resident_set_size, process = row
                command_id = pid + " " + process

                if not self.ps_data.get(command_id):
                    self.ps_data[command_id] = {
                        date: resident_set_size,
                        "trace": None
                    }
                else:
                    self.ps_data[command_id][date] = resident_set_size
            self.update_graph_data()
            self.update_plotly_graph()
            time.sleep(self.time_interval)
            i += 1

    def update_graph_data(self):
        for command in self.ps_data.keys():
            dates = sorted([date for date in self.ps_data[
                           command].keys() if not date == "trace"])
            if not self.ps_data[command]["trace"]:
                self.ps_data[command]["trace"] = go.Scatter(
                    x=dates,
                    y=[self.ps_data[command][date] for date in dates],
                    name=command[0:100],
                    opacity=0.8,
                    connectgaps=True,
                    line=dict(shape='spline')
                )
            else:
                self.ps_data[command]["trace"].x = dates
                self.ps_data[command]["trace"].y = [
                    self.ps_data[command][date] for date in dates]
            self.graph_data[command] = self.ps_data[command]["trace"]

    def update_plotly_graph(self, extend_existing_plot=False):
        fig = go.Figure(
            data=self.graph_data.values(),
            layout=self._create_layout("Memory Usage (kb)")
        )
        plot(fig, filename=self.output_filename, auto_open=False)


if __name__ == "__main__":
    PsGrapher().run()
