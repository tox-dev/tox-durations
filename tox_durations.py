from collections import defaultdict
from datetime import datetime

from tox import hookimpl


class Report(object):
    def __init__(self):
        self.found_python = None
        self.create_venv = None
        self.install_deps = None
        self.run_test = None
        self.config = None

    def __str__(self):
        return 'config {}, found {}, create {}, install {}, run {}'.format(self.config, self.found_python,
                                                                           self.create_venv, self.install_deps,
                                                                           self.run_test)


class Duration(object):
    def __init__(self):
        self.reports = defaultdict(Report)
        self.enabled = False
        self._time = datetime.now()

    @property
    def diff(self):
        t = datetime.now()
        d = t - self._time
        self._time = t
        return d


DURATION = Duration()


@hookimpl
def tox_addoption(parser):
    parser.add_argument('--durations', action='store_true', help='measure time passed between operations')


@hookimpl
def tox_configure(config):
    DURATION.enabled = config.option.durations


@hookimpl()
def tox_get_python_executable(envconfig):
    DURATION.reports[envconfig.envname].config = DURATION.diff


@hookimpl
def tox_testenv_create(venv, action):
    DURATION.reports[venv.name].get_python = DURATION.diff


@hookimpl
def tox_testenv_install_deps(venv, action):
    DURATION.reports[venv.name].create_venv = DURATION.diff


@hookimpl
def tox_runtest_pre(venv):
    DURATION.reports[venv.name].install_deps = DURATION.diff


@hookimpl
def tox_runtest_post(venv):
    DURATION.reports[venv.name].run_test = DURATION.diff
    print('{} => {}'.format(venv.name, DURATION.reports[venv.name]))
