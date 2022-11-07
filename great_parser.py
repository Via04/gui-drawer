import numpy as np


class SeriousParser:
    x = None
    y = None
    _locals = None

    def __init__(self, x):
        self.x = x
        self.y = np.array([])
        self._locals = locals()

    def parse_exp(self, expr):
        py_code = compile(expr,'<string>','exec')
        exec(py_code,globals(),self._locals)
        self.y = self._locals['y']
        return self.y