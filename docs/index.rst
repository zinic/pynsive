Pronounced, "Pensive"
=====================

**Pynsive** is a simple plugin library that uses the **sys.meta\_path** list
along with custom finder and loader definitions to hook into the Python
import process. This means that when directores or other plugin search targets
are added in Pynsive, future import statements will now search the newly added
path for plugin modules and classes.

For more information on the import process hooks, please see:

-  `Python 3 Import Process <http://docs.python.org/3/reference/import.html>`_
-  `PEP-302 <http://www.python.org/dev/peps/pep-0302/>`_


Getting Started
~~~~~~~~~~~~~~~

Below are some helpful documents to help get you started in using Pynsive.

- `[Blog Post] Getting started with Pynsive by Chad Lung <http://www.giantflyingsaucer.com/blog/?p=4634>`_


Pynsive Documentation
~~~~~~~~~~~~~~~~~~~~~

.. toctree::
    :maxdepth: 2

    usage


.. toctree::
    :maxdepth: 2

    pynsive

.. toctree::
    :maxdepth: 2

    changelog


That Legal Thing...
~~~~~~~~~~~~~~~~~~~

This software library is released to you under the
`MIT Software License <http://opensource.org/licenses/MIT>`_
. See `LICENSE <https://github.com/zinic/pynsive/blob/master/LICENSE>`_ for
more information.

