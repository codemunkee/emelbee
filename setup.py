from setuptools import setup

setup(name='EmelbeeStats',
      version='0.3.1',
      description='Returns MLB Scores and Standings by querying APIs',
      url='https://github.com/codemunkee/emelbee',
      author='Russ',
      author_email='codemunkee@gmail.com',
      license='BSD',
      py_modules = ['EmelbeeStats'],
      scripts = ['bin/emelbee_stats', 'bin/emelbee_api'],
      data_files= [('/etc/emelbee', ['conf/team_names.txt'])],
      install_requires=['requests>=2.7.0', 'flask', 'twilio'],
      zip_safe=False)
