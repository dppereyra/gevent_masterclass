from setuptools import setup, find_packages

VERSION = '1.0.0'


setup(name='cbo-demo',
      version=VERSION,
      packages=find_packages('src'),
      include_package_data=True,
      zip_safe=False,
      package_dir={'': 'src'},
      namespace_packages=['demo'],
      install_requires=[],
      entry_points="""\
      [console_scripts]
      demo = demo.coroutines.console:main
      """,
      )
