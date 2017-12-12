# ps_grapher
[![Build Status](https://travis-ci.org/scottx611x/ps_grapher.svg?branch=master)](https://travis-ci.org/scottx611x/ps_grapher)
[![codecov](https://codecov.io/gh/scottx611x/ps_grapher/branch/master/graph/badge.svg)](https://codecov.io/gh/scottx611x/ps_grapher)

Graph [`ps`](https://en.wikipedia.org/wiki/Ps_(Unix)) output over time w/ [Plotly](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0ahUKEwi_wO6gmOXXAhVC7yYKHcMiAHIQFggpMAA&url=https%3A%2F%2Fplot.ly%2F&usg=AOvVaw13Djn0jQ81pcw8YNx89IT5)

### Pre-Reqs:
- `python`
- `pip`

### Installation:
- `git clone https://github.com/scottx611x/ps_grapher.git`
- `cd ps_grapher && pip install -r requirements.txt`

### Running Tests:
- `python tests.py`

### Running PsGrapher:
- `pyhton ps_grapher.py`
- Running this will, by default, create an html file in the current working directory called: `PsGrapher.html`, and update the embedded `plotly` graph every minute with info from the top 10 memory hogging processes.

### Why?:
- I was motivated to make this after having trouble debugging a finnicky memory leak that wasn't easy to catch through normal logging practices.

### Sample Output:
![screen shot 2017-12-12 at 5 00 20 pm](https://user-images.githubusercontent.com/5629547/33910824-0c5a41fe-df5e-11e7-8a2b-4f2d305015fc.png)

