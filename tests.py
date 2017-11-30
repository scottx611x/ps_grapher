import __builtin__
import datetime
import mock
import os
import unittest

import ps_grapher
from ps_grapher import PsGrapher


class PsGrapherTests(unittest.TestCase):

    def setUp(self):
        self.fake_datetime = datetime.datetime(
            2017, 11, 29, 21, 50, 26, 369898
        )
        mock.patch.object(
            PsGrapher,
            "_get_date",
            return_value=self.fake_datetime
        ).start()

        with open("test-data/ps_mock.txt") as f:
            self.ps_mock = mock.patch.object(
                ps_grapher,
                "check_output",
                return_value=f.read()
            ).start()
        self.maxDiff = None
        self.output_filename = "Coffee"
        self.output_file = self.output_filename + ".html"
        self.ps_grapher = PsGrapher(
            iterations=1,
            time_interval=.01,
            output_filename=self.output_filename,
            n_top_processes=3
        )

    def tearDown(self):
        try:
            os.remove(self.output_file)
        except OSError as e:
            pass

    def test_run_works(self):
        self.ps_grapher.run()
        self.assertTrue(self.ps_mock.called)

    def test_custom_filename(self):
        self.ps_grapher.run()
        self.assertTrue(os.path.exists(self.output_file))

    def test__format_ps_output(self):
        self.assertEqual(
            self.ps_grapher._format_ps_output(),
            [
                ['5832', '0.3', '15.4', '316144',
                    'python /vagrant/refinery/manage.py runserver 0.0.0.0:8000 --noreload'],
                ['1246', '1.8', '8.8', '181116', '/usr/bin/java'],
                ['2382', '4.8', '6.9', '143116',
                    'java -server -Xss256k -Xms32m -Xmx32m']
            ]
        )

    def test__get_ps_output(self):
        self.assertEqual(
            self.ps_grapher._get_ps_output(),
            [
                'PID %CPU %MEM   RSS COMMAND',
                '5832  0.3 15.4 316144 python /vagrant/refinery/manage.py runserver 0.0.0.0:8000 --noreload',
                '1246  1.8  8.8 181116 /usr/bin/java',
                '2382  4.8  6.9 143116 java -server -Xss256k -Xms32m -Xmx32m',
                '1257  0.0  5.9 122192 postgres: checkpointer process',
                '5355  0.1  5.5 114244 python /vagrant/refinery/manage.py celeryd -c 1 -Q file_import --events',
                '3350  0.2  4.0 82088 /usr/lib/erlang/erts-5.10.4/bin/beam -W w -A 64 -P 1048576 -t 5000000 -stbt db -zdbbl 32000 -K true -B i -- -root /usr/lib/erlang -progname erl -- -home /var/lib/rabbitmq -- -pa /usr'
            ]
        )

    def test__get_iterations(self):
        self.assertTrue(PsGrapher()._get_iterations(None))
        self.assertTrue(PsGrapher(iterations=1)._get_iterations(0))
        self.assertFalse(PsGrapher(iterations=10)._get_iterations(11))

    def test__create_layout(self):
        self.assertEqual(
            PsGrapher()._create_layout(),
            {'xaxis': {'rangeselector': {'buttons': [{'count': 1, 'step': 'minute', 'stepmode': 'backward', 'label': '1 min'}, {'count': 1, 'step': 'hour', 'stepmode': 'backward', 'label': '1 hour'}, {
                'count': 1, 'step': 'day', 'stepmode': 'backward', 'label': '1 day'}, {'step': 'all'}]}, 'tickformat': '%H:%M:%S', 'type': 'date', 'rangeslider': {}}, 'title': 'Memory Usage (kb)'}
        )

    def test__get_graph_data(self):
        self.assertEqual(self.ps_grapher._get_graph_data(), {})

    def test__get_ps_data(self):
        self.assertEqual(self.ps_grapher._get_ps_data(), {})

    def test__update_graph_data(self):
        self.ps_grapher._update_ps_data()
        self.ps_grapher._update_graph_data()
        self.assertEqual(
            self.ps_grapher._get_graph_data(),
            {
                '5832 python /vagrant/refinery/manage.py runserver 0.0.0.0:8000 --noreload': {
                    'opacity': 0.8,
                    'name': '5832 python /vagrant/refinery/manage.py runserver 0.0.0.0:8000 --noreload',
                    'connectgaps': True,
                    'y': ['316144'],
                    'x': [self.fake_datetime],
                    'line': {'shape': 'spline'},
                    'type': 'scatter'
                },
                '2382 java -server -Xss256k -Xms32m -Xmx32m': {
                    'opacity': 0.8,
                    'name': '2382 java -server -Xss256k -Xms32m -Xmx32m',
                    'connectgaps': True,
                    'y': ['143116'],
                    'x': [self.fake_datetime],
                    'line': {'shape': 'spline'},
                    'type': 'scatter'
                },
                '1246 /usr/bin/java': {
                    'opacity': 0.8,
                    'name': '1246 /usr/bin/java',
                    'connectgaps': True,
                    'y': ['181116'],
                    'x': [self.fake_datetime],
                    'line': {'shape': 'spline'},
                    'type': 'scatter'}
            }
        )

    def test__update_ps_data(self):
        self.ps_grapher._update_ps_data()
        self.assertEqual(
            self.ps_grapher._get_ps_data(),
            {'5832 python /vagrant/refinery/manage.py runserver 0.0.0.0:8000 --noreload': {'trace': None, self.fake_datetime: '316144'}, '2382 java -server -Xss256k -Xms32m -Xmx32m': {
                'trace': None, self.fake_datetime: '143116'}, '1246 /usr/bin/java': {'trace': None, self.fake_datetime: '181116'}}
        )

    def test__update_plotly_graph(self):
        self.ps_grapher._update_ps_data()
        self.ps_grapher._update_graph_data()
        self.ps_grapher._update_plotly_graph()

if __name__ == "__main__":
    unittest.main()
