from setuptools import setup, find_namespace_packages

version = '2.1'

tests_require = [
    'plone.app.testing',
    'plone.app.contenttypes',
    'plone.app.robotframework',  # imported by plone.app.contenttypes.testing
]

setup(name='plone.app.changeownership',
      version=version,
      description="Change Plone objects ownership",
      long_description=open("README.rst").read() + "\n" +
                       open("CHANGES.rst").read(),
      # Get more strings from https://pypi.org/classifiers/
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: 6.1",
        "Framework :: Plone :: 6.2",
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        ],
      keywords='plone change ownership',
      author='Mustapha Benali',
      author_email='mustapha@headnet.dk',
      url='https://github.com/collective/plone.app.changeownership',
      license='GPL',
      packages=find_namespace_packages(include=['plone', 'plone.*']),
      include_package_data=True,
      zip_safe=False,
      python_requires='>=3.8',
      tests_require=tests_require,
      extras_require=dict(test=tests_require),
      install_requires=[
          'setuptools',
          'Acquisition',
          'Products.CMFCore',
          'Products.CMFPlone',
          'plone.memoize',
          'zope.component',
          'zope.i18nmessageid',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
