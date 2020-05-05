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
def tree():
    task = SimplifyTask()
    task.generate()
    tex_html = task.to_html()
    mfp = task.get().get_task()
    t = create_tree(make_fractions_pretty(mfp))
    res = t.print()
    return render_template('tree.html', expression=tex_html, tree=res)


@app.route('/menu')
def get_menu():
    return render_template('menu.html')


@app.route('/generate_taskset', methods=['GET'])
def route_generate_taskset(num=1, min_comp=10, max_comp=30, xmin=-5, xmax=5, rnd=42):
    arg = request.args
    num = int(arg.get('num')) if 'num' in arg else num
    min_comp = int(arg.get('min_comp')) if 'min_comp' in arg else min_comp
    max_comp = int(arg.get('max_comp')) if 'max_comp' in arg else max_comp
    xmin = int(arg.get('xmin')) if 'xmin' in arg else xmin
    xmax = int(arg.get('xmax')) if 'xmax' in arg else xmax
    rnd = int(arg.get('rnd')) if 'rnd' in arg else rnd
    text = arg.get('text')
    roots = 'roots' in arg
    floats = 'floats' in arg
    count = 2 if 'second_var' in arg else 1
    show_answers = 'show_answers' in arg
    if xmin >= xmax:
        return render_template('menu.html', num=num, min_comp=min_comp, max_comp=max_comp,
                               xmin=xmin, xmax=xmax, rnd=rnd, roots=roots, floats=floats,
                               second_var='second_var' in arg,
                               show_answers=show_answers, text=text)
    np.random.seed(rnd)
    tasks = [SimplifyTask() for i in range(num)]
    taskset = TaskSet(tasks, seed=rnd)
    taskset.generate(params={
            'xmin': xmin,
            'xmax': xmax,
            'roots': roots,
            'floats': floats,
            'vars': count,
            'text': text,
            'min_comp': min_comp,
            'max_comp': max_comp
        })
    tex_html = taskset.to_html(0, show_answers=show_answers)
    return render_template('generated.html', data=tex_html, num=num,
                           min_comp=min_comp, max_comp=max_comp,
                           xmin=xmin, xmax=xmax, rnd=rnd, roots=roots, floats=floats, second_var='second_var' in arg,
                           show_answers=show_answers, text=text)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()
