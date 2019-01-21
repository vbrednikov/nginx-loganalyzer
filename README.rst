========
Overview
========

.. start-badges

.. image:: https://travis-ci.org/vbrednikov/nginx-loganalyzer.svg?branch=master
    :target: https://travis-ci.org/vbrednikov/nginx-loganalyzer

.. image:: https://coveralls.io/repos/github/vbrednikov/nginx-loganalyzer/badge.svg?branch=master
    :target: https://coveralls.io/github/vbrednikov/nginx-loganalyzer?branch=master


.. end-badges

Collection of parser and report utilities for Nginx (and other web-servers) logs in different formats.

* Free software: BSD 2-Clause License

Installation
============

::

    pip install git+https://github.com/vbrednikov/nginx-loganalyzer

Documentation
=============


To use the project:

Create config file ~/.analyzer.cfg with the following contents:

.. code-block:: bash
    [main]
    # report_size: how many urls to include in the report
    REPORT_SIZE: 100
    # where to put the reports (will be created automatically if not exist)
    REPORT_DIR: ./reports
    # where to search for the logs
    LOG_DIR: ./log

    # report won't be generated if the percent of good lines is less then $threshold
    threshold: 60


.. code-block:: bash

    nginx_loganalyzer [ --config /path/to/analyzer.cfg ]


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
