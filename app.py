from flask import *
from generator.generators import *
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


@app.route("/generate/<name>/<mode>", methods=['GET'])
def route_generate(name='Tasks', mode=6):
    mode = int(mode)
    with app.app_context():
        x = symbols('x')
        pdf, _, _ = expr_to_pdf([generator(x + np.random.randint(-5, 6), 1 + np.random.randint(0, 121) % mode)
                                 for _ in range(12)], name, keep_file=False)
        response = make_response(pdf)
        # response.headers.set('Content-Disposition', 'attachment', filename=name + '.pdf')
        response.headers.set('Content-Type', 'application/pdf')
        return response


if __name__ == '__main__':
    app.run()
