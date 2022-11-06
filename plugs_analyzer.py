
class PlugAnalyzer:
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