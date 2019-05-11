#!/usr/bin/env python
"""Prepare teaching + solution verison of querybuilder notebook"""
# pylint: disable=invalid-name
from __future__ import print_function
import copy
import json
import sys


def remove_lines_from_cell(cell, remove_from_string, remove_to_string,
                           remove_string):
    """remove lines from cell of notebook"""
    indices_to_remove = set()
    first_line_solution = None
    last_line_solution = None
    for idx, line in enumerate(cell['source']):
        if line.startswith(remove_string):
            indices_to_remove.add(idx)
        elif line.startswith(remove_from_string):
            if first_line_solution is not None:
                raise Exception(
                    "I only support the removal of one block per cell")
            first_line_solution = idx
        elif line.startswith(remove_to_string):
            if first_line_solution is None:
                raise Exception("I have no line for starting this block")
            last_line_solution = idx
    if first_line_solution is not None:
        if last_line_solution is None:
            raise Exception(
                "I found a start for the block but no end of the block")
        else:
            indices_to_remove |= set(
                range(first_line_solution, last_line_solution + 1))

    for idx in sorted(indices_to_remove, reverse=True):
        cell['source'].pop(idx)


def make_notebook(template_file_name,
                  tutorial_file_name=None,
                  solution_file_name=None):
    """
    Master function to create requested notebooks

    """
    if tutorial_file_name is None and solution_file_name is None:
        print("Nothing to do")
        return

    with open(template_file_name) as f:
        template = json.load(f)

    if tutorial_file_name is not None:
        tutorial = copy.deepcopy(template)
        for cell in tutorial['cells']:
            remove_lines_from_cell(cell, '#TUT_SOLUTION_START',
                                   '#TUT_SOLUTION_END', '#TUT_USER')
        with open(tutorial_file_name, 'w') as f:
            json.dump(tutorial, f)

    if solution_file_name is not None:
        solution = copy.deepcopy(template)
        for cell in solution['cells']:
            remove_lines_from_cell(cell, '#TUT_USER_START', '#TUT_USER_END',
                                   '#TUT_SOLUTION')
        with open(solution_file_name, 'w') as f:
            json.dump(solution,
                      f,
                      indent=1,
                      sort_keys=True,
                      separators=(',', ': '))


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(
        "To make the user version and a solution version:" +
        "\npython make_notebook.py template.ipynb -t tutorial.ipynb -s solution.ipynb"
    )
    parser.add_argument(
        'template',
        help=
        'Provide the template the contains both versions, tutorial and solution',
        type=str)
    parser.add_argument(
        '-t',
        '--tutorial',
        help='Make version for the tutorial and store in this file',
        type=str)
    parser.add_argument('-s',
                        '--solution',
                        help='Make the solution and store in this file',
                        type=str)
    pa = parser.parse_args(sys.argv[1:])
    make_notebook(template_file_name=pa.template,
                  tutorial_file_name=pa.tutorial,
                  solution_file_name=pa.solution)
