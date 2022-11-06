from re import findall

import matplotlib.pyplot as plt
import numpy as np  # do not change np as it used as pattern addon


# x = linspace(0, 2 * pi, 100)
# y = sin(x)
# plt.plot(x, y, 'ro-')
# plt.show()

class PlotHelper:
    """ Класс для построения графиков по математическому описанию"""
    param_marker = ''
    val_marker = ''
    usr_func_marker = ''
    min_x = 0
    max_x = 0
    complexity = 0
    x = None
    fig = None
    ax = None

    def __init__(self, min_x=0, max_x=0, complexity=100, param_marker='p_', val_marker='v_',
                 usr_func_marker='u_'):
        self.param_marker = param_marker
        self.val_marker = val_marker
        self.usr_func_marker = usr_func_marker
        self.min_x = min_x
        self.max_x = max_x
        self.complexity = complexity
        self.x = np.linspace(min_x, max_x, complexity)
        self.fig = plt.figure(figsize=(6, 5))
        self.ax = self.fig.add_subplot(1, 1, 1)
    #@timeit
    def ans_expr(self, expr: str) -> list:
        code = self.gen_pycode(expr)
        x = self.x
        y = None
        _local = locals()
        exec(code, globals(), _local)
        y = _local['y']
        return y

    def gen_pycode(self, expr: str):
        command = self.parse_expression(expr)
        x = self.x
        y = None
        # command = 'y = ' + command  # if you change y name variable, also change this line
        py_code = compile(command, '<string>', 'exec')
        return py_code

    def save_to_file(self, expr: str, filename):
        # expr = self.parse_expression(expr)
        with open(filename, 'w') as f:
            f.write(expr)

    def read_from_file(self, filename):
        with open(filename, 'r') as f:
            expr = ''.join(f.readlines())
            return expr

    def parse_expression(self, expr: str) -> str:
        final_expr = ''
        python_mode = False
        if expr is not None:
            for e in expr.split('\n'):
                if e != '':
                    if e[0] == '!':
                        python_mode = not python_mode
                        final_expr += '\n'
                        continue
                    if not python_mode:
                        # op_pattern = '\\s[A-XZa-xz]+\\s(?<!\\spow\\s)'
                        #  '\\s[^' + self.param_marker[:1] + self.val_marker[:1] + self.usr_func_marker[:1] + 'y' + \
                        #  '\\W\\d][^' + self.param_marker + self.val_marker + self.usr_func_marker + ']?\\w*\\s'
                        # op_pattern = '\s[^pv\W][^__]?\w*\s'
                        val_pattern = '\\s' + self.val_marker + '\\w*\\s'
                        param_pattern = '\\s' + self.param_marker + '\\w*\\s'
                        # ops = findall(op_pattern, expr)
                        vals = findall(val_pattern, e)
                        params = findall(param_pattern, e)
                        # for op in ops:
                        #     new_op = op[:1] + 'np.' + op[1:]
                        #     expr = expr.replace(op, new_op)
                        for val in vals:
                            new_val = ' ' + val[3:-1] + ' '
                            e = e.replace(val, new_val)
                        for param in params:
                            new_param = ' ' + param[3:-1] + ' '
                            e = e.replace(param, new_param)
                        expr_without_space = e.replace(' ', '')
                    else:
                        expr_without_space = e
                    final_expr += expr_without_space + '\n'
            # final_expr += 'return y'
            # final_expr = '  '.join(('\n' + final_expr.lstrip()).splitlines(True))
            # if is_parallel:
            #     final_expr = '@njit(parallel=True)\ndef myfunc(x):' + final_expr + '\ny = myfunc(x)'
            # else:
            #     final_expr = 'def myfunc(x):' + final_expr + '\ny = myfunc(x)'

            return final_expr

    def plot_expr(self, expr: str):
        y = self.ans_expr(expr)
        x = self.x
        plt.plot(x, y, 'ro-')
        plt.show()

    def get_text(self, expr: str) -> str:
        out = ''
        exprs = expr.split(';')
        for e in exprs:
            y = self.ans_expr(e)
            x = self.x
            for j in range(len(x)):
                print(f'{y[j]}\t{x[j]}\n')
                out += f'{y[j]}\t{x[j]}\n'
        return out

    def get_figure(self, expr: str):
        exprs = expr.split(';')
        for e in exprs:
            y = self.ans_expr(e)
            x = self.x
            ca = plt.gca()
            ca.set_ylim([min(y), max(y)])
            self.ax.grid(True)
            self.ax.plot(x, y, (self.max_x - self.min_x) / self.complexity)
        return self.fig

    @classmethod
    def plot_array(cls, x_list, y_list):
        plt.plot(x_list, y_list, 'ro-')
        plt.show()
# test = PlotHelper(0, 2 * np.pi)
# test.plot_expr(' -1 * log ( v_x )')
