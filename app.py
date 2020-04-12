from flask import *
from generator.generators import *
from generator.tree import *
from printer.printing import *
from sympy import *

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


def task_generator(mode):
    x = symbols('x')
    if mode == 0:
        arr = [0, 1, 2, 3, 5, 8]
    elif mode == 1:
        arr = [4, 6, 7]
    elif mode == 2:
        arr = [9, 10, 11]
    else:
        arr = range(42)
    tasks = [generator(x + np.random.randint(-5, 6), m)
             for m in arr]
    return tasks


def task_generator_new(type, xmin, xmax):
    x = create_var(can_other_letters=False)
    tasks = [generator(x + np.random.randint(xmin, xmax+1), m) for m in type]
    return tasks


@app.route("/generate/<name>/<int:mode>", methods=['GET'])
def route_generate(name='Tasks', mode=3):
    with app.app_context():
        tasks = task_generator(mode)
        solutions = [expr.simplify() for expr in tasks]
        pdf, _, _ = expr_to_pdf(tasks, name, keep_file=False)
        _, _, _ = expr_to_pdf(solutions, 'Solutions', keep_file=True)
        response = make_response(pdf)
        # response.headers.set('Content-Disposition', 'attachment', filename=name + '.pdf')
        response.headers.set('Content-Type', 'application/pdf')
        return response


@app.route('/generate_html/<int:mode>')
def route_generate_html(mode=3):
    tasks = task_generator(mode)
    s = print_tex_on_html(tasks)
    return render_template('generated.html', data=s)


@app.route('/tree')
def tree(mode=-1):
    arg = request.args
    mode = int(arg.get('mode')) if 'mode' in arg else mode
    x = symbols('x')
    if mode == -1:
        mode = np.random.randint(6, 12)
    mfp = generator(x + np.random.randint(-10, 11), mode)
    tex_html = print_tex_on_html([mfp])
    d = parse_sympy(make_fractions_pretty(mfp), for_print=True)
    res = str_tree(d, 0)
    return render_template('tree.html', expression=tex_html, tree=res)


@app.route('/menu')
def get_menu():
    return render_template('menu.html')


@app.route('/generate_taskset', methods=['GET'])
def route_generate_taskset(num=1, type=0, xmin=-5, xmax=5):
    arg = request.args
    num = int(arg.get('num')) if 'num' in arg else num
    type = int(arg.get('type')) if 'type' in arg else type
    xmin = int(arg.get('xmin')) if 'xmin' in arg else xmin
    xmax = int(arg.get('xmax')) if 'xmax' in arg else xmax
    var = [type]*num if type != 42 else list(range(num))
    tasks = task_generator_new(var, xmin, xmax)
    tex_html = print_tex_on_html(tasks)
    return render_template('generated.html', data=tex_html, num=num, type=type, xmin=xmin, xmax=xmax)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
