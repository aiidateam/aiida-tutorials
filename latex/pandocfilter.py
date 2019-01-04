#!/usr/bin/env python
"""
Filters for conversion from LaTeX to MarkDown.

 * handle bash/python code blocks
"""
import sys
from pandocfilters import toJSONFilter, Link, CodeBlock

def log(foo):
    with open('/tmp/dump', 'w') as f:
        f.write(foo)


def caps(key, value, format, meta):
    if key == "CodeBlock":
        properties = value[0]
        attributes = properties[2]

        # this signifies python codeblock
        if ['frame', 'leftline'] in attributes:
            # set 'python' class
            properties[1] = ['python']
        else:
            # set 'terminal' class
            properties[1] = ['terminal']

        # unset attrs
        properties[2] = []

        value[0] = properties

        #log(str(value))
        return CodeBlock(*value)

if __name__ == "__main__":
    toJSONFilter(caps)
