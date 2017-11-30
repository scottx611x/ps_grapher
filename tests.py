import mock
import os
import unittest

import ps_grapher
from ps_grapher import PsGrapher


class PsGrapherTests(unittest.TestCase):

    def setUp(self):
        with open("test-data/ps_mock.txt") as f:
            self.ps_mock = mock.patch.object(
                ps_grapher,
                "check_output",
                return_value=f.read()
            ).start()
            self.ouput_filename = "Coffee"
            self.output_file = self.ouput_filename + ".html"

    def tearDown(self):
        for path in ["PsGrapher.html", self.output_file]:
            try:
                os.remove(path)
            except OSError as e:
                pass

    def test_run_works(self):
        PsGrapher(
            iterations=1,
            time_interval=1
        ).run()
        self.assertTrue(self.ps_mock.called)

    def test_custom_filename(self):
        PsGrapher(
            iterations=1,
            time_interval=1,
            output_filename=self.ouput_filename
        ).run()
        self.assertTrue(self.ps_mock.called)
        self.assertTrue(os.path.exists(self.output_file))

if __name__ == "__main__":
    unittest.main()
