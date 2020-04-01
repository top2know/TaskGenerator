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


@app.route("/generate/<name>/<int:mode>", methods=['GET'])
def route_generate(name='Tasks', mode=3):
    with app.app_context():
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
        solutions = [expr.simplify() for expr in tasks]
        pdf, _, _ = expr_to_pdf(tasks, name, keep_file=False)
        _, _, _ = expr_to_pdf(solutions, 'Solutions', keep_file=True)
        response = make_response(pdf)
        # response.headers.set('Content-Disposition', 'attachment', filename=name + '.pdf')
        response.headers.set('Content-Type', 'application/pdf')
        return response


@app.route('/tree/', defaults={'mode': -1})
@app.route('/tree/<int:mode>')
def tree(mode=-1):
    x = symbols('x')
    if mode == -1:
        mode = np.random.randint(6, 12)
    mfp = make_fractions_pretty(generator(x + np.random.randint(-10, 11), mode))
    d = parse_sympy(mfp, for_print=True)
    res = str_tree(d, 0)
    return res


if __name__ == '__main__':
    app.run()
