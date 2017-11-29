import os
import unittest

from ps_grapher import PsGrapher


class PsGrapherTests(unittest.TestCase):

    def test_html_file_created(self):
        PsGrapher(iterations=2, time_interval=2).run()
        os.remove("MemoryUsage.html")


if __name__ == "__main__":
    unittest.main()
