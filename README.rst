========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        | |coveralls| |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|



.. |travis| image:: https://travis-ci.org/vbrednikov/op1-loganalyzer.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/vbrednikov/op1-loganalyzer

.. |coveralls| image:: https://coveralls.io/repos/vbrednikov/op1-loganalyzer/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/vbrednikov/op1-loganalyzer

.. |codecov| image:: https://codecov.io/github/vbrednikov/op1-loganalyzer/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/vbrednikov/op1-loganalyzer

.. |version| image:: https://img.shields.io/pypi/v/op1-loganalyzer.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/op1-loganalyzer

.. |commits-since| image:: https://img.shields.io/github/commits-since/vbrednikov/op1-loganalyzer/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/vbrednikov/op1-loganalyzer/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/op1-loganalyzer.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/op1-loganalyzer

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/op1-loganalyzer.svg
    :alt: Supported versions
    :target: https://pypi.org/project/op1-loganalyzer

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/op1-loganalyzer.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/op1-loganalyzer


.. end-badges

access log statistics generator

* Free software: BSD 2-Clause License

Installation
============

::

    pip install https://github.com/vbrednikov/op1-loganalyzer

Documentation
=============


To use the project:

.. code-block:: python

    import op1_loganalyzer
    op1_loganalyzer.longest()


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
