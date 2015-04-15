Pyap: Python address parser
===========================


Pyap is an MIT Licensed text processing library, written in Python, for
detecting and parsing addresses. Currently it supports USA and Canadian
addresses. 


.. code-block:: python

    >>> import pyap
    >>> test_address = """
        Lorem ipsum
        225 E. John Carpenter Freeway, 
        Suite 1500 Irving, Texas 75062
        Dorem sit amet
        """
    >>> addresses = pyap.parse(test_address, country='US')
    >>> for address in addresses:
            # shows found address
            print(address)
            # shows address parts
            print(address.as_dict())
    ...




Installation
------------

To install Pyap, simply:

.. code-block:: bash

    $ pip install pyap



About
-----
This library has been created because i couldn't find any reliable and
opensource solution for detecting addresses on web pages when writing my
web crawler. Currently available solutions have drawbacks when it comes
to using them to process really large amounts of data fast. You'll
either have to buy some proprietary software; use third-party
pay-per-use services or use address detecting which is slow and
unsuitable for real-time processing.

Pyap is an alternative to all these methods. It is really fast because
it is based on using regular expressions and it allows to find addresses
in text in real time with low error rates.


Future work
-----------
- Add rules for parsing UK addresses
- Add rules for parsing FR addresses
- ...


Typical workflow
----------------
Pyap should be used as a first thing when you need to detect an address
inside a text when you don't know for sure whether the text contains
addresses or not.

To achieve the most accuracy Pyap results could be reverified using
geocoding process.


Limitations
-----------
Because Pyap is based on regular expressions it provides fast results.
This is also a limitation because regexps intentionally do not use too
much context to detect an address.

In other words in order to detect US address, the library doesn't
use any list of US cities or a list of typical street names. It
looks for a pattern which is most likely to be an address.

For example the string below would be detected as a valid address: 
"1 SPIRITUAL HEALER DR SHARIF NSAMBU SPECIALISING IN"

It happens because this string has all the components of a valid
address: street number "1", street name "SPIRITUAL HEALER" followed
by a street identifier "DR" (Drive), city "SHARIF NSAMBU SPECIALISING"
and a state name abbreviation "IN" (Indiana).

The good news is that the above mentioned errors are **quite rare**.


