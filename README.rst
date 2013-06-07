log2jsconsole
=============

.. image:: http://i.imgur.com/jkYMB.png
   :alt: Safari Web Inspector

.. image:: http://i.imgur.com/AWba1.png
   :alt: Opera Dragonfly

It provides a simple WSGI middleware that helps to log messages into
JavaScript ``console`` object. For example, if you log messages like::

    logger = logging.getLogger('my.logger')
    logger.warning('warning message')
    logger.debug('debug message')

The middleware automatically appends codes like following JavaScript::

    <script>
    // <![CDATA[
    if (console) {
      console.warn('my.logger: warning message');
      console.debug('my.logger: debug message');
    }
    // ]]>
    </script>


Installation
------------

You can install it by downloading from PyPI_ through ``pip`` or
``easy_install``::

    $ pip install log2jsconsole

.. _PyPI: http://pypi.python.org/pypi/log2jsconsole


How to use
----------

Assume that your WSGI application name is ``app``::

    from yourapp import app
    from log2jsconsole import LoggingMiddleware

    app = LoggingMiddleware(app)

Or you can add this as a filter of `Python Paste`_:

.. code-block:: ini

   [filter:log]
   use = egg:log2jsconsole
   auto_install = True

.. _Python Paste: http://pythonpaste.org/


Changelog
---------

Version 0.4
```````````

To be released.

- Support for `Python Paste`_ filter entry point. [`#1`_ by Roberto De Almeida]
- Fixed incompatibile signature (according to PEP 333) of ``start_response``.
  [`#1`_ by Roberto De Almeida]

.. _#1: https://github.com/StyleShare/log2jsconsole/pull/1


Version 0.3
```````````

Released on November 28, 2011.

- Fixed a bug of ``Content-Type`` detection.


Version 0.2
```````````

Released on November 28, 2011.

- Fixed a bug of ``Content-Type`` detection.


Version 0.1
```````````

Initially released on November 26, 2011.
