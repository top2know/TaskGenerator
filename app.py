from flask import *
from generator.generators import *
from generator.tree import *
from printer.printing import *
from sympy import *

from tasks.simplification import SimplifyTask
from tasks.taskset import TaskSet

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html', user='Alex')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/news')
def news():
    return 'To be done'


@app.route('/tree')
def tree(mode=-1):
    arg = request.args
    mode = int(arg.get('mode')) if 'mode' in arg else mode
    if mode == -1:
        mode = np.random.randint(0, 6)
    task = SimplifyTask(var=mode)
    task.generate()
    tex_html = task.to_html()
    mfp = task.get().get_task()
    d = parse_sympy(make_fractions_pretty(mfp), for_print=True)
    res = str_tree(d, 0)
    return render_template('tree.html', expression=tex_html, tree=res)


@app.route('/menu')
def get_menu():
    return render_template('menu.html')


@app.route('/generate_taskset', methods=['GET'])
def route_generate_taskset(num=1, type=0, xmin=-5, xmax=5, rnd=42):
    arg = request.args
    num = int(arg.get('num')) if 'num' in arg else num
    type = int(arg.get('type')) if 'type' in arg else type
    xmin = int(arg.get('xmin')) if 'xmin' in arg else xmin
    xmax = int(arg.get('xmax')) if 'xmax' in arg else xmax
    rnd = int(arg.get('rnd')) if 'rnd' in arg else rnd
    roots = 'roots' in arg
    floats = 'floats' in arg
    check_complex = 'check_complex' in arg
    count = 2 if 'second_var' in arg else 1
    if xmin >= xmax:
        return render_template('generated.html', num=num, type=type,
                               xmin=xmin, xmax=xmax, rnd=rnd, roots=roots, floats=floats,
                               check_complex=check_complex, second_var='second_var' in arg)
    np.random.seed(rnd)
    var = [type] * num if type != 42 else list(range(num))
    tasks = [SimplifyTask(var=var[i]) for i in range(num)]
    taskset = TaskSet(tasks, seed=rnd)
    taskset.generate(params={
            'xmin': xmin,
            'xmax': xmax,
            'roots': roots,
            'floats': floats,
            'vars': count
        })
    tex_html = taskset.to_html(0, check_complex)
    return render_template('generated.html', data=tex_html, num=num, type=type,
                           xmin=xmin, xmax=xmax, rnd=rnd, roots=roots, floats=floats,
                           check_complex=check_complex, second_var='second_var' in arg)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
