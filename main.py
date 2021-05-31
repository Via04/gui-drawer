import PySimpleGUI as gui

from xlsx_parser import XLSXParser
from graph_drawer import PlotHelper


layout = [[gui.In(key='input-file'), gui.FileBrowse(button_text='Выберите xlsx файл', file_types=(('Excel files', '*.xlsx'),), target='input-file')],
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
        break
    if event == 'Создание модели':
        model_layout = [[gui.In(key='-MODEL-'), gui.Button('Create', bind_return_key=True, visible=False)]]
        mod_window = gui.Window('Создайте модель', model_layout)
        while True:
            mod_evt, mod_val = mod_window.read()
            if mod_evt == 'Create':
                plot = PlotHelper(0, 100, 100)
                model = mod_val['-MODEL-']
                plot.plot_expr(model)
                break
            if mod_evt == gui.WINDOW_CLOSED:
                break
        break
    if event == gui.WINDOW_CLOSED:
        break

window.close()

