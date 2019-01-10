========
Overview
========

.. start-badges

image:: https://travis-ci.org/vbrednikov/nginx-loganalyzer.svg?branch=master
  :alt: Travis-CI Build Status
  :target: https://travis-ci.org/vbrednikov/nginx-loganalyzer

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

.. code-block:: bash

    nginx_loanalyzer


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
