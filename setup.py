from setuptools import setup

setup(
  name='music_indexer',
  version='0.0.1',
  py_modules=['music_indexer'],
  install_requires=[
    'Click',
  ],
  entry_points='''
        [console_scripts]
        music_indexer=command:index
    ''',
)
