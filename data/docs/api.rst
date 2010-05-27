=======================
 Transparency Data API
=======================	

License
=======

Data returned by this service is subject to the use restrictions set by the Federal Election Commission. By accessing this data, you understand that you are using the data subject to all applicable local, state and federal law, including FEC restrictions.

All data licensed under the Creative Commons BY-NC-SA license. By downloading data and accessing the API you are agreeing to the terms of the license.

Federal campaign contribution and lobbying records must be attributed to OpenSecrets.org.

State campaign contribution records must be attributed to FollowTheMoney.org.

Authentication
==============

An API key is required to access the Transparency Data API. `Registration is easy <http://services.sunlightlabs.com/accounts/register/>`_ and if you already have a `Sunlight Data Services <http://services.sunlightlabs.com/accounts/register/>`_ key you can use it here.

The API key *must* be as either an ``apikey`` query string parameter or as a ``X-APIKEY`` HTTP request parameter. Example::

	http://transparencydata.com/api/1.0/contributions.csv?apikey=<key>&...

Common Parameters
=================

These parameters are common to all API methods.

apikey
    Required if the ``X-APIKEY`` HTTP header is not used.

page
    The page of results to return; defaults to 1.

per_page
    The number of results to return per page, defaults to 1,000. The maximum number of records per page is 100,000.
