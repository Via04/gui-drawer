import matplotlib.pyplot as plt
import matplotlib.figure
from re import findall
import numpy as np  # do not change np as it used as pattern addon


# x = linspace(0, 2 * pi, 100)
# y = sin(x)
# plt.plot(x, y, 'ro-')
# plt.show()

class PlotHelper:
    param_marker = ''
    val_marker = ''
    usr_func_marker = ''
    min_x = 0
    max_x = 0
    complexity = 0
    x = None

    def __init__(self, min_x=0, max_x=0, complexity=100, param_marker='p_', val_marker='v_',
                 usr_func_marker='u_'):
        self.param_marker = param_marker
        self.val_marker = val_marker
        self.usr_func_marker = usr_func_marker
        self.min_x = min_x
        self.max_x = max_x
        self.complexity = complexity
        self.x = np.linspace(min_x, max_x, complexity)

    def ans_expr(self, expr: str) -> list:
        code = self.gen_pycode(expr)
        x = self.x
        _local = locals()
        exec(code, globals(), _local)
        y = _local['y']
        return y

    def gen_pycode(self, expr: str):
        command = self.parse_expression(expr)
        y = None
        x = self.x
        # command = 'y = ' + command  # if you change y name variable, also change this line
        py_code = compile(command, '<string>', 'exec')
        return py_code

    def save_to_file(self, expr: str, filename):
        expr = self.parse_expression(expr)
        with open(filename, 'w') as f:
            f.write(expr)

    def read_from_file(self, filename):
        with open(filename, 'rb') as f:
            code = '\n'.join(f.readlines())
            return code

    def parse_expression(self, expr: str) -> str:
        if expr is not None:
            op_pattern = '\\s[A-XZa-xz]+\\s'
            #  '\\s[^' + self.param_marker[:1] + self.val_marker[:1] + self.usr_func_marker[:1] + 'y' + \
                          #  '\\W\\d][^' + self.param_marker + self.val_marker + self.usr_func_marker + ']?\\w*\\s'
            # op_pattern = '\s[^pv\W][^__]?\w*\s'
            val_pattern = '\\s' + self.val_marker + '\\w*\\s'
            param_pattern = '\\s' + self.param_marker + '\\w*\\s'
            ops = findall(op_pattern, expr)
            vals = findall(val_pattern, expr)
            params = findall(param_pattern, expr)
            for op in ops:
                new_op = op[:1] + 'np.' + op[1:]
                expr = expr.replace(op, new_op)
            for val in vals:
                new_val = ' ' + val[3:-1] + ' '
                expr = expr.replace(val, new_val)
            for param in params:
                new_param = ' ' + param[3:-1] + ' '
                expr = expr.replace(param, new_param)
            expr_without_space = ''
            for line in expr:
                if line[0:1] == ' ':
                    expr_without_space += line[1:]
                else:
                    expr_without_space += line
            return expr_without_space

    def plot_expr(self, expr: str):
        y = self.ans_expr(expr)
        x = self.x
        plt.plot(x, y, 'ro-')
        plt.show()

    def get_figure(self, expr):
        y = self.ans_expr(expr)
        x = self.x
        fig = plt.figure(figsize=(5, 4))
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(x, y, (self.max_x - self.min_x) / self.complexity)
        return fig


    @classmethod
    def plot_array(cls, x_list, y_list):
        plt.plot(x_list, y_list, 'ro-')
        plt.show()

# test = PlotHelper(0, 2 * np.pi)
# test.plot_expr(' -1 * log ( v_x )')
