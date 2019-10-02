# force-bdss-plugin-gromacs
Gromacs BDSS data sources, as well as a stand-alone wrappers around Gromacs tools.

Installation requirements include an up-to-date version of ``force-bdss``.

Additional modules that can contribute to the ``force-wfmanager`` UI are also included,
but a local version of ``force-wfmanager`` is not required in order to complete the 
installation.


Installation Instructions
-------------------------
To install ``force-bdss`` and the ``force-wfmanager``, please see the following 
[instructions](https://github.com/force-h2020/force-bdss/blob/master/doc/source/installation.rst).

After completing at least the ``force-bdss`` installation steps, clone the git repository::

    git clone https://github.com/force-h2020/force-bdss-plugin-gromacs

After downloading, enter the source directory and run:

    python -m ci install

This will allow install the plugin in the `force-py36` edm environment, allowing the contributed BDSS objects to be visible by both ``force-bdss``
 and ``force-wfmanager`` applications.
