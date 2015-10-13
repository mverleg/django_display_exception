
Django Display Exception
---------------------------------------

This app can (sligtly) encourage modularity and readability, as well as decrease code repetition and length, by using Exceptions to handle exceptional (non-standard) situations.

Specifically, it offers an alternative way to handle a failing check in a view fails (object not found, access denied, etc). It let's you throw an special exception that is shown to the user in a pretty way. No need to worry about returning error messages up the chain.

The 'problem' (or 'inconvenience' really) that this solves is explained in my programmers.stackexchange_ question, which is where the idea for started.

Example usage
---------------------------------------

There is a simple example (the whole app is simple, really) contained in the demo directory of this repository.


Configuration
---------------------------------------




Built-in displayable exceptions
---------------------------------------

* `PermissionDenied` (550 Permission Denied): the current account doesn't have access to this resource.
* `NotFound` (404 Not Found): whatever the user requested could not be found (temporarily or permanently).
* `BadRequest` (400 BadRequest): what the user sent is not correctly formatted (e.g. non-integer id).
* `NotImplemented` (501 Not Implemented): the requested functionality isn't supported yet.
* `Notification` (200 Ok): no error, just display something.

If there's no suitable exception in the list, you can subclass `DisplayableException` yourself.

Arguments
---------------------------------------

The exceptions take several arguments that influence their rendering:

* `message`: The message to be displayed, describing what went wrong.
* `caption`: If set, overrules the default caption for the error display page.
* `next`: The url of the page the user should continue, or a callable to generate said url.
* `status_code`: If set, overrules the default http status code of this exception.
* `template`: If set, overrules the default template used to render this exception.
* `context`: Any extra context for the template (only useful for custom templates).

Check out the docstring for `DisplayableException` for all the arguments.



.. _programmers.stackexchange: http://programmers.stackexchange.com/questions/276302/how-to-handle-django-get-single-instance-in-view-pattern



# should be high in apps list (so others can overwrite templates)
# where in middleware list?

# DISPLAY_EXCEPTIONS_BASE_TEMPLATE

# license

# versions

# does not print all exceptions, just specific ones


! make sure these exceptions are not logged

! setup.py and pip etc


