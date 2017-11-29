import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

import time
import datetime
from subprocess import check_output
import sys
import os

PS_DATA = {}
GRAPH_DATA = {}
TIME_INTERVAL = 60  # seconds


def get_ps_output():
    output = [item.lstrip().rstrip() for item in check_output(
        "ps -e -o pid,%cpu,%mem,rss,command --sort -rss".split(" ")).split("\n")]
    output.pop(0)
    new = [a.split() for a in output[:10] if a]
    newer = [[x[0], x[1], x[2], x[3], " ".join(x[4:])] for x in new]
    return newer


def create_layout(title):
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


def update_graph_data():
    for command in PS_DATA.keys():
        dates = sorted([date for date in PS_DATA[command].keys() if not date == "trace"])
	if not PS_DATA[command]["trace"]:
            PS_DATA[command]["trace"] = go.Scatter(
                x=dates,
                y=[PS_DATA[command][date] for date in dates],
                name=command[0:100],
                opacity=0.8,
                connectgaps=True,
                line=dict(shape='spline')
            )
        else:
            PS_DATA[command]["trace"].x = dates
            PS_DATA[command]["trace"].y = [PS_DATA[command][date] for date in dates]
	GRAPH_DATA[command] = PS_DATA[command]["trace"]

def update_plotly_graph(extend_existing_plot=False):
    global GRAPH_DATA
    global PS_DATA
    fig = go.Figure(
        data=GRAPH_DATA.values(),
        layout=create_layout("Memory Usage (kb)")
    )
    plot(fig, filename="MemoryUsage.html", auto_open=False)

def main():
    global INITIAL_PLOT
    global PS_DATA
    global TIME_INTERVAL
    while True:
        date = datetime.datetime.now()
        for row in get_ps_output():
            pid, cpu_percentage, mem_percentage, resident_set_size, process = row
            command_id = pid + " " + process

            if not PS_DATA.get(command_id):
                PS_DATA[command_id] = {
                    date: resident_set_size,
                    "trace": None
		}
            else:
                PS_DATA[command_id][date] = resident_set_size
    	update_graph_data()
    	update_plotly_graph()
        time.sleep(TIME_INTERVAL)

if __name__ == "__main__":
    main()
