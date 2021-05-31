import matplotlib.pyplot as plt
from re import findall
import numpy as np  # do not change np as it used as pattern addon


# x = linspace(0, 2 * pi, 100)
# y = sin(x)
# plt.plot(x, y, 'ro-')
# plt.show()

class PlotHelper:
    param_marker = ''
    val_marker = ''
    min_x = 0
    max_x = 0
    complexity = 0

    def __init__(self, min_x: float, max_x: float, complexity=100, param_marker='p_', val_marker='v_'):
        self.param_marker = param_marker
        self.val_marker = val_marker
        self.min_x = min_x
        self.max_x = max_x
        self.complexity = complexity

    def plot_expr(self, expr: str):
        command = self.parse_expression(expr)
        x = np.linspace(self.min_x, self.max_x, 100)
        y = None
        command = 'y = ' + command  # if you change y name variable, also change this line
        py_code = compile(command, '<string>', 'exec')
        _local = locals()
        exec(py_code, globals(), _local)
        y = _local['y']
        plt.plot(x, y, 'ro-')
        plt.show()

    def parse_expression(self, expr: str) -> str:
        if expr is not None:
            op_pattern = '\s[^' + self.param_marker[:1] + self.val_marker[:1] + '\W\d][^' + self.param_marker + \
                      self.val_marker + ']?\w*\s'
            # op_pattern = '\s[^pv\W][^__]?\w*\s'
            val_pattern = '\s' + self.val_marker + '\w*\s'
            param_pattern = '\s' + self.param_marker + '\w*\s'
            ops = findall(op_pattern, expr)
            vals = findall(val_pattern, expr)
            params = findall(param_pattern, expr)
            for op in ops:
                new_op = op[:1] + 'np.' + op[1:]
                expr = expr.replace(op, new_op)
            for val in vals:
                new_val = val[3:]
                expr = expr.replace(val, new_val)
            for param in params:
                new_param = param[3:]
                expr = expr.replace(param, new_param)
            return expr

    @classmethod
    def plot_array(cls, x_list, y_list):
        plt.plot(x_list, y_list, 'ro-')
        plt.show()

# test = PlotHelper(0, 2 * np.pi)
# test.plot_expr(' -1 * log ( v_x )')
