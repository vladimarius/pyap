from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='pyap',
      version='0.2.0',
      description='Library for detecting and parsing addresses.'
      ' Currently supports US, Canadian and British addresses.',
      long_description=readme(),
      long_description_content_type="text/x-rst",
      keywords='address detection, address parsing',
      url='http://github.com/vladimarius/pyap',
      author='Vladimir Goncharov',
      author_email='vladimarius@gmail.com',
      license='MIT',
      packages=['pyap', 'pyap.packages', 'pyap.source_CA', 'pyap.source_US', 'pyap.source_GB'],
      download_url='https://github.com/vladimarius/pyap',
      zip_safe=False,
      classifiers=[
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
      ],
      )
