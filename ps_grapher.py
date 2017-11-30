import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

import time
import datetime
from subprocess import check_output
import sys
import os


class PsGrapher:

    def __init__(self,
                 iterations=None,
                 time_interval=60,
                 output_filename="PsGrapher",
                 n_top_processes=10):
        self.ps_data = {}
        self.graph_data = {}
        self.time_interval = time_interval
        self.iterations = iterations
        self.n_top_processes = n_top_processes
        self.output_filename = "{}.html".format(output_filename)

    def _format_ps_output(self):
        process_info_list = [process_info.split() for process_info in self.get_ps_output()[
            :self.n_top_processes] if process_info]
        return [
            [process_info[0], process_info[1], process_info[2],
                process_info[3], " ".join(process_info[4:])]
            for process_info in process_info_list
        ]

    def _get_iterations(self, count):
        if self.iterations is None:
            return True
        elif count <= self.iterations:
            return True
        return False

    def get_ps_output(self):
        ps_command = "ps -e -o pid,%cpu,%mem,rss,command --sort -rss"
        return [item.lstrip().rstrip()
                for item in check_output(ps_command.split(" ")).split("\n")]

    def _create_layout(self, title):
        return {
            "title": title,
            "xaxis": {
                "rangeselector": {
                    "buttons": [
                        {
                            "count": 1,
                            "label": '1 min',
                            "step": 'minute',
                            "stepmode": 'backward'
                        },
                        {
                            "count": 1,
                            "label": '1 hour',
                            "step": 'hour',
                            "stepmode": 'backward'
                        },
                        {
                            "count": 1,
                            "label": '1 day',
                            "step": 'day',
                            "stepmode": 'backward'
                        },
                        {"step": 'all'}
                    ]
                },
                "rangeslider": {},
                "type": "date",
                "tickformat": "%H:%M:%S"
            }
        }

    def run(self, count=0):
        while self._get_iterations(count):
            date = datetime.datetime.now()
            for row in self._format_ps_output():
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
            count += 1

    def update_graph_data(self):
        for command in self.ps_data.keys():
            dates = sorted([date for date in self.ps_data[
                           command].keys() if not date == "trace"])
            memory_usage = [self.ps_data[command][date] for date in dates]
            if not self.ps_data[command]["trace"]:
                self.ps_data[command]["trace"] = go.Scatter(
                    x=dates,
                    y=memory_usage,
                    name=command[0:100],
                    opacity=0.8,
                    connectgaps=True,
                    line=dict(shape='spline')
                )
            else:
                self.ps_data[command]["trace"].x = dates
                self.ps_data[command]["trace"].y = memory_usage
            self.graph_data[command] = self.ps_data[command]["trace"]

    def update_plotly_graph(self, extend_existing_plot=False):
        fig = go.Figure(
            data=self.graph_data.values(),
            layout=self._create_layout("Memory Usage (kb)")
        )
        plot(fig, filename=self.output_filename, auto_open=False)


if __name__ == "__main__":
    PsGrapher().run()
