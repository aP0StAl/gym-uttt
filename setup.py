from os import path

from setuptools import setup

extras = {
    'test': ['pytest'],
}

# Meta dependency groups.
extras['all'] = [item for group in extras.values() for item in group]


setup(
    name='gym_uttt',
    version='0.0.1',
    description='Ultimate Tic-Tac-Toe game based on OpenAI gym.',
    long_description_content_type='text/markdown',
    long_description=open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8').read(),
    url='https://github.com/aP0StAl/gym-uttt',
    author='Stanislav Poryadnyi',
    author_email='sporyadnyi@gmail.com',
    license='MIT License',
    install_requires=[
        'gym==0.26.2',
        'Pillow'
    ],
    extras_require=extras,
    tests_require=extras['test'],
    python_requires='>=3.7,<3.8',
)
