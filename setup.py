from setuptools import setup

setup(name='EmelbeeStats',
      version='0.3',
      description='Returns MLB Scores and Standings by querying APIs',
      url='https://github.com/codemunkee/emelbee',
      author='Russ',
      author_email='codemunkee@gmail.com',
      license='BSD',
      packages = ['EmelbeeStats'],
      scripts = ['bin/get_stats', 'bin/emelbee_api'],
      install_requires=['requests>=2.7.0'],
      zip_safe=False)
