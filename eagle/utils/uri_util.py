# -*- coding: utf-8 -*-

import re

# NOTE(kgriffs): Published method; take care to avoid breaking changes.


def compile_uri_template(template):
    """Compile the given URI template string into a pattern matcher.

    This function can be used to construct custom routing engines that
    iterate through a list of possible routes, attempting to match
    an incoming request against each route's compiled regular expression.

    Each field is converted to a named group, so that when a match
    is found, the fields can be easily extracted using
    :py:meth:`re.MatchObject.groupdict`.

    This function does not support the more flexible templating
    syntax used in the default router. Only simple paths with bracketed
    field expressions are recognized. For example::

        /
        /books
        /books/{isbn}
        /books/{isbn}/characters
        /books/{isbn}/characters/{name}

    Also, note that if the template contains a trailing slash character,
    it will be stripped in order to normalize the routing logic.

    Args:
        template(str): The template to compile. Note that field names are
            restricted to ASCII a-z, A-Z, and the underscore character.

    Returns:
        tuple: (template_field_names, template_regex)
    """

    if not isinstance(template, str):
        raise TypeError('uri_template is not a string')

    if not template.startswith('/'):
        raise ValueError("uri_template must start with '/'")

    if '//' in template:
        raise ValueError("uri_template may not contain '//'")

    if template != '/' and template.endswith('/'):
        template = template[:-1]

    # template names should be able to start with A-Za-z
    # but also contain 0-9_ in the remaining portion
    expression_pattern = r'{([a-zA-Z]\w*)}'

    # Get a list of field names
    fields = set(re.findall(expression_pattern, template))

    # Convert Level 1 var patterns to equivalent named regex groups
    escaped = re.sub(r'[\.\(\)\[\]\?\*\+\^\|]', r'\\\g<0>', template)
    pattern = re.sub(expression_pattern, r'(?P<\1>[^/]+)', escaped)
    pattern = r'\A' + pattern + r'\Z'

    return fields, re.compile(pattern, re.IGNORECASE)
