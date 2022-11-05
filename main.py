import os
from os.path import curdir
import time
from re import findall

import PySimpleGUI as gui
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from numba import njit

from xlsx_parser import XLSXParser
from graph_drawer import PlotHelper

def timeit(method):
    """Метод-декоратор для подсчета времени выполнения функции"""
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print(f'{method.__name__}  {(te - ts) * 1000}')
        return result
    return timed

PLUGIN_EXTENSION = 'py'
usr_model_layout = []
usr_model_functions = dict()
usr_common_layout = []
usr_common_functions = dict()

def analyze_plugs():
    is_model = False
    for files in os.listdir(os.getcwd()):
        if files.endswith(PLUGIN_EXTENSION):
            with open(files,'rt') as f:
                func_code = ''
                is_func = False
                user_action = ''
                for num, line in enumerate(f):
                    if num == 0 and line != '#!PLUGIN_SPECIFICATION':
                        break
                    if num == 1 and len(findall('\[MODEL_LAYOUT\]', line)) >= 1:
                        is_model = True
                    else:
                        is_model = False
                    if num == 2:
                        user_action = findall('\'.*\'', line)
                        user_action = user_action[1:-1] # убрать кавычки
                        user_layout_str = 'user_layout = ' + line
                        user_layout = None
                        _local = locals()
                        exec(user_layout_str, globals(), _local)
                        user_layout = _local['user_layout']
                        if is_model:
                            usr_model_layout.append(user_layout)
                        else:
                            usr_common_layout.append(user_layout)
                    if len(findall('Controller', line)) >= 1:
                        is_func = True
                        continue
                    if is_func:
                        func_code += line + '\n'
                func_code = '  '.join(('\n' + func_code.lstrip()).splitlines(True))
                func_code = f'def {files.split(".")[0]}(evt, val):\n' + func_code
                func_code = func_code + f'\nfunc_code_obj = {files.split(".")[0]}'
                func_code_obj = None
                _local = locals()
                exec(func_code, globals(), _local)
                func_code_obj = _local['func_code_obj']
                if is_model:
                    usr_model_functions.update({user_action: func_code_obj})
                else:
                    usr_common_functions.update({user_action: func_code_obj})
        else:
            continue

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


layout = [[gui.In(key='input-file'), gui.FileBrowse(button_text='Выберите xlsx файл',
                                                    file_types=(('Excel files', '*.xlsx'),), target='input-file')],
          [gui.Button('Создание модели')],
          [gui.Button('Нарисовать график')]]
window = gui.Window('Тестирование результатов', layout)
file = window['input-file']
while True:
    event, values = window.read()
    if event == 'Нарисовать график':
        xlsx = XLSXParser(values['input-file'])
        x_list = xlsx.get_column_values(1)
        y_list = xlsx.get_column_values(2)
        PlotHelper.plot_array(x_list, y_list)
    if event == 'Создание модели':
        model_layout = [[gui.Multiline(key='-MODEL-', size=(100, 20), font='Monospaced 16'),
                         gui.Button('Create', visible=True)],
                        [gui.Button('Text table', visible=True)],
                        [gui.Text('Мин'), gui.In(key='-MIN-X-', size=(15, 10), default_text='0'),
                         gui.Text('Макс'), gui.In(key='-MAX-X-', size=(15, 10), default_text='100'),
                         gui.Text('Сложность'), gui.In(key='-COMPLEXITY-', size=(15, 10), default_text='100')],
                        [gui.InputText(key='-SAVE-MOD-', enable_events=True, visible=False),
                         gui.FileSaveAs('Save', target='-SAVE-MOD-', file_types=(('PYDATA', '.pydat'),),
                                        initial_folder=curdir),
                         gui.InputText(key='-LOAD-MOD-', enable_events=True, visible=False),
                         gui.FileBrowse('Load', target='-LOAD-MOD-', file_types=(('PYDATA', '.pydat'),),
                                        initial_folder=curdir)]]
        mod_window = gui.Window('Создайте модель', model_layout)
        while True:
            mod_evt, mod_val = mod_window.read()
            if mod_evt == 'Create':
                min_x = int(mod_val['-MIN-X-'])
                max_x = int(mod_val['-MAX-X-'])
                complexity = int(mod_val['-COMPLEXITY-'])
                plot = PlotHelper(min_x, max_x, complexity)
                model = mod_val['-MODEL-']
                plot_layout = [[gui.Text('Model')], [gui.Canvas(key='-CANVAS-')]]
                fig = plot.get_figure(model)
                canv_window = gui.Window('Graph from model', plot_layout, finalize=True,
                                         element_justification='center', font='Monospace 18')
                fig_agg = draw_figure(canv_window['-CANVAS-'].TKCanvas, fig)
                fig_agg.draw()
            if mod_evt == 'Text table':
                min_x = int(mod_val['-MIN-X-'])
                max_x = int(mod_val['-MAX-X-'])
                complexity = int(mod_val['-COMPLEXITY-'])
                plot = PlotHelper(min_x, max_x, complexity)
                model = mod_val['-MODEL-']
                out = plot.get_text(model)
                with open('out.txt', 'wt') as f:
                    f.write(out)
            if mod_evt == '-SAVE-MOD-':
                plot = PlotHelper()
                model = mod_val['-MODEL-']
                filename = mod_val['-SAVE-MOD-']
                plot.save_to_file(model, filename)
            if mod_evt == '-LOAD-MOD-':
                plot = PlotHelper()
                filename = mod_val['-LOAD-MOD-']
                if filename != '':
                    model = plot.read_from_file(filename)
                    mod_window['-MODEL-'].update(model)
            for key, func in usr_model_functions:
                if mod_evt == key:
                    func(mod_evt, mod_val)
            if mod_evt == gui.WINDOW_CLOSED:
                break
        break
    if event == gui.WINDOW_CLOSED:
        break

window.close()
