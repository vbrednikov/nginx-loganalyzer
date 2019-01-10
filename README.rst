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



.. |travis| image:: https://travis-ci.org/vbrednikov/nginx-loganalyzer.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/vbrednikov/nginx-loganalyzer

.. |coveralls| image:: https://coveralls.io/repos/vbrednikov/nginx-loganalyzer/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/vbrednikov/nginx-loganalyzer

.. |codecov| image:: https://codecov.io/github/vbrednikov/nginx-loganalyzer/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/vbrednikov/nginx-loganalyzer

.. |version| image:: https://img.shields.io/pypi/v/nginx-loganalyzer.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/nginx-loganalyzer

.. |commits-since| image:: https://img.shields.io/github/commits-since/vbrednikov/nginx-loganalyzer/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/vbrednikov/nginx-loganalyzer/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/nginx-loganalyzer.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/nginx-loganalyzer

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/nginx-loganalyzer.svg
    :alt: Supported versions
    :target: https://pypi.org/project/nginx-loganalyzer

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/nginx-loganalyzer.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/nginx-loganalyzer


.. end-badges

access log statistics generator

* Free software: BSD 2-Clause License

Installation
============

::

    pip install https://github.com/vbrednikov/nginx-loganalyzer

Documentation
=============


To use the project:

.. code-block:: python

    import nginx_loganalyzer
    nginx_loganalyzer.longest()


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
