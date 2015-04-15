from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='pyap',
      version='0.1',
      description='Library for detecting and parsing addresses.'
      ' Currently supports US and Canadian addresses.',
      long_description=readme(),
      keywords='adress detection, address parsing',
      url='http://github.com/vladimarius/pyap',
      author='Vladimir Goncharov',
      author_email='vladimarius@gmail.com',
      license='MIT',
      packages=['pyap', 'pyap.packages', 'pyap.source_CA', 'pyap.source_US'],
      zip_safe=False,
      classifiers=(
          'Intended Audience :: Developers',
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.1',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Topic :: Software Development :: Libraries',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Utilities'
      ),
      )
