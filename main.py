import os
from os.path import curdir
import time
from re import findall

import PySimpleGUI as gui
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from numba import njit

from xlsx_parser import XLSXParser
from graph_drawer import PlotHelper
from plugs_analyzer import PlugAnalyzer
from service_funcs import timeit


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
            # for key, func in usr_model_functions:
            #     if mod_evt == key:
            #         func(mod_evt, mod_val)
            if mod_evt == gui.WINDOW_CLOSED:
                break
        break
    if event == gui.WINDOW_CLOSED:
        break

window.close()
