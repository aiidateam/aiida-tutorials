#!/usr/bin/env python
"""
Filters for conversion from LaTeX to MarkDown.

 * handle bash/python code blocks
"""
from __future__ import absolute_import
from pandocfilters import toJSONFilter, CodeBlock


def log(msg):
    """Log message to file."""
    with open('/tmp/dump', 'w') as f:
        f.write(msg)


def code(key, value, format, meta):  # pylint: disable=unused-argument,redefined-builtin
    """Handle python/console code blocks."""
    if key == "CodeBlock":
        properties = value[0]
        attributes = properties[2]

        # this signifies python codeblock
        if ['frame', 'leftline'] in attributes:
            # set 'python' class
            properties[1] = ['python']
        else:
            # set class
            #  - for markdown: use 'terminal'
            #  - for rst: use 'console'
            properties[1] = ['console']

        # unset attrs
        properties[2] = []

        value[0] = properties

        #log(str(value))

    return CodeBlock(*value)


if __name__ == "__main__":
    toJSONFilter(code)
