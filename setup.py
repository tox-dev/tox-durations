# content of setup.py
from setuptools import setup

if __name__ == "__main__":
    setup(
        name='tox-durations',
        description='tox plugin that measure durations of tasks',
        license="MIT license",
        version='0.1',
        py_modules=['tox_durations'],
        entry_points={'tox': ['durations = tox_durations']},
        install_requires=['tox>=2.0'],
    )
