# [MODEL_LAYOUT]
[gui.Button('Text table', visible=True)]

# Controller
min_x = int(mod_val['-MIN-X-'])
max_x = int(mod_val['-MAX-X-'])
complexity = int(mod_val['-COMPLEXITY-'])
plot = PlotHelper(min_x, max_x, complexity)
model = mod_val['-MODEL-']
y = plot.ans_expr(model)
x = plot.x
with open('out.txt','wt') as f:
    for i, j in y, x:
        f.write(f'{i}\t{j}')