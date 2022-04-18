# Python-Fiery-API-Functions [![CodeFactor](https://www.codefactor.io/repository/github/seanmrice/python-fiery-api-functions/badge)](https://www.codefactor.io/repository/github/seanmrice/python-fiery-api-functions)
Generic repository of various preformatted API call functions for Fiery print servers, written in Python and updated for Fiery API v5

NOTES: Unless otherwise stated, "serverName" accepts the IP address of the Fiery server *or* the DNS name of the Fiery Server
It is highly recommended to supply the IP address and not the DNS address of the Fiery since DNS can tend to be flaky
Fiery API documentation is available at https://developer.efi.com/ - but in my opinion it is extremely unclear and incomplete
I recommend running the FieryPullHeld() function on a few jobs first, so you can see what options and attributes are actually
available in your environment - then modifying the FieryJobUpdate() to reflect your needs.
