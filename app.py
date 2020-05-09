import os
import tempfile
from subprocess import Popen, PIPE
import shutil


from flask import *
from generator.tree import *
from printer.printing import *
from tasks.equation import EquationTask
from tasks.factory import TaskFactory
from tasks.simple_task import SimpleTask
from tasks.simplification import SimplifyTask
from tasks.taskset import TaskSet

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html', user='Alex')


@app.route('/taskset')
def taskset():
    return render_template('taskset_menu.html')


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


def taskset_to_zip(taskset):
    with tempfile.TemporaryDirectory() as tempdir, tempfile.TemporaryDirectory() as tempdir2:
        files = taskset.to_tex()
        for i, file in enumerate(files):
            for _ in range(2):
                process = Popen(
                    ['pdflatex', '-output-directory', tempdir],
                    stdin=PIPE,
                    stdout=PIPE,
                )
                process.communicate(file.encode('utf-8'))
            shutil.copyfile(os.path.join(tempdir, 'texput.pdf'), os.path.join(tempdir2, 'variant{}.pdf'.format(i)))
        shutil.make_archive(os.path.join(tempdir, 'archive'), 'zip', tempdir2)
        with open(os.path.join(tempdir, 'archive.zip'), 'rb') as f:
            zip_file = f.read()
    return zip_file


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
    as_zip = 'as_zip' in arg
    if xmin >= xmax:
        return render_template('menu.html', num=num, min_comp=min_comp, max_comp=max_comp,
                               xmin=xmin, xmax=xmax, rnd=rnd, roots=roots, floats=floats,
                               second_var='second_var' in arg,
                               show_answers=show_answers, text=text)
    np.random.seed(rnd)
    tasks = [SimplifyTask() for i in range(num)]
    taskset = TaskSet(tasks, seed=rnd)
    taskset.generate(num=3, params={
        'xmin': xmin,
        'xmax': xmax,
        'roots': roots,
        'floats': floats,
        'vars': count,
        'text': text,
        'min_comp': min_comp,
        'max_comp': max_comp
    })

    if as_zip:
        zip_file = taskset_to_zip(taskset)
        response = make_response(zip_file)
        response.headers.set('Content-Type', 'zip')
        response.headers.set('Content-Disposition', 'attachment', filename='archive.zip')
        return response

    tex_html = taskset.to_html(0, show_answers=show_answers)
    return render_template('generated.html', data=tex_html, num=num,
                           min_comp=min_comp, max_comp=max_comp,
                           xmin=xmin, xmax=xmax, rnd=rnd, roots=roots, floats=floats, second_var='second_var' in arg,
                           show_answers=show_answers, text=text)


@app.route('/generate_demo_taskset', methods=['GET'])
def get_example_taskset():
    factory = TaskFactory()
    arg = request.args
    tasks = [factory.get(arg.get('task_{}'.format(i))) for i in range(1, len(arg))]
    taskset = TaskSet(tasks)
    taskset.generate(num=int(arg.get('num')) if 'num' in arg else 3)
    zip_file = taskset_to_zip(taskset)
    response = make_response(zip_file)
    response.headers.set('Content-Type', 'zip')
    response.headers.set('Content-Disposition', 'attachment', filename='archive.zip')
    return response


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()
