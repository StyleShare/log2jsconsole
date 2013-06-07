try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    with open('README.rst') as readme_file:
        readme = readme_file.read()
except IOError:
    readme = None


setup(name='log2jsconsole',
      version='0.3',
      description='Simple WSGI middleware that helps to log messages into '
                  'JavaScript console object',
      long_description=readme,
      license='MIT License',
      author='Hong Minhee',
      author_email='dahlia' '@' 'stylesha.re',
      url='https://github.com/StyleShare/log2jsconsole',
      py_modules=['log2jsconsole'],
      install_requires=['Werkzeug'],
      entry_points="""
      [paste.filter_app_factory]
      main = log2jsconsole:make_middleware
      """)

