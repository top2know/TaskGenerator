import os
import tempfile
from subprocess import Popen, PIPE
import shutil

from flask import *
from printer.printing import *
from tasks.factory import TaskFactory
from tasks.simplification import SimplifyTask
from tasks.taskset import TaskSet

import logging.handlers
import configparser

config = configparser.ConfigParser()
config.read("config")

app = Flask(__name__)

# noinspection PyTypeChecker
smtp_handler = logging. \
    handlers.SMTPHandler(mailhost=(config['SMTP']['address'], int(config['SMTP']['port'])),
                         secure=(),
                         fromaddr=config['SMTP']['username'],
                         toaddrs=config['SMTP']['username'],
                         subject=u"[{}] TaskGenerator error!".format(config['ENV']['env']),
                         credentials=(config['SMTP']['username'], config['SMTP']['password']))

smtp_handler.setLevel(logging.ERROR)

logger = logging.getLogger()
logger.addHandler(smtp_handler)


@app.route('/')
def hello_world():
    return render_template('index.html', user='Alex')


@app.route('/taskset')
def taskset():
    return render_template('taskset_menu.html', nums=list(range(1, 10)))


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


def pdflatex_magic(tempdir, tempdir2, file, filename):
    for _ in range(5):
        for _ in range(2):
            process = Popen(
                ['pdflatex', '-output-directory', tempdir],
                stdin=PIPE,
                stdout=PIPE,
            )
            process.communicate(file.encode('utf-8'))
        try:
            shutil.copyfile(os.path.join(tempdir, 'texput.pdf'), os.path.join(tempdir2, filename))
            break
        except:
            continue


def taskset_to_zip(taskset, multiple_files=True):
    with tempfile.TemporaryDirectory() as tempdir, tempfile.TemporaryDirectory() as tempdir2:
        files, answers = taskset.to_tex(multiple_files=multiple_files)
        for i, file in enumerate(files):
            pdflatex_magic(tempdir, tempdir2, file, 'variant{}.pdf'.format(i+1))
        pdflatex_magic(tempdir, tempdir2, answers, 'answers.pdf')
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
    taskset.generate(num=(3 if as_zip else 1), params={
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
                           xmin=xmin, xmax=xmax, rnd=rnd,
                           roots=roots, floats=floats, second_var='second_var' in arg,
                           show_answers=show_answers, text=text)


@app.route('/generate_demo_taskset', methods=['GET'])
def get_example_taskset(rnd=42):
    factory = TaskFactory()
    arg = request.args
    rnd = int(arg.get('rnd')) if 'rnd' in arg else rnd
    np.random.seed(rnd)
    tasks = [factory.get(arg.get('task_{}'.format(i)), arg.get('task_{}_comp'.format(i)))
             for i in range(1, int(arg.get('num_tasks')) + 1)]
    taskset = TaskSet(tasks)
    taskset.generate(num=int(arg.get('num')) if 'num' in arg else 3)
    zip_file = taskset_to_zip(taskset, 'multiple' in arg)
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
