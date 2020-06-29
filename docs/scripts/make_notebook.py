#!/usr/bin/env python
"""Prepare teaching + solution version of querybuilder notebook"""
# pylint: disable=invalid-name
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


def make_markdown(template_file_name,
                  tutorial_file_name=None,
                  solution_file_name=None):
    """ Master function to create requested notebooks, in markdown format."""
    # pylint: disable=too-many-branches
    from myst_nb.converter import myst_to_notebook
    import nbformat

    if tutorial_file_name is None and solution_file_name is None:
        print("Nothing to do")
        return

    with open(template_file_name) as f:
        template = f.readlines()

    if tutorial_file_name is not None:
        in_solution = False
        tutorial_lines = []
        for i, line in enumerate(template):
            if line.startswith("#TUT_SOLUTION_START"):
                in_solution = True
            elif line.startswith("#TUT_SOLUTION_END"):
                in_solution = False
            elif line.startswith("#TUT_USER"):
                if in_solution:
                    raise Exception(
                        "Line {}: In solution, but found user end/start".
                        format(i))
            elif not in_solution:
                tutorial_lines.append(line)
        with open(tutorial_file_name, 'w') as f:
            f.writelines(tutorial_lines)

    if solution_file_name is not None:
        in_tutorial = False
        solution_lines = []
        for i, line in enumerate(template):
            if line.startswith("#TUT_USER_START"):
                in_tutorial = True
            elif line.startswith("#TUT_USER_END"):
                in_tutorial = False
            elif line.startswith("#TUT_SOLUTION"):
                if in_tutorial:
                    raise Exception(
                        "Line {}: In tutorial, but found solution end/start".
                        format(i))
            elif not in_tutorial:
                solution_lines.append(line)
        # for the solution, since we are not going to parse it in sphinx,
        # we just convert it straight to a notebook
        notebook = myst_to_notebook("\n".join(solution_lines))
        with open(solution_file_name, 'w') as f:
            nbformat.write(notebook, solution_file_name)


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
    parser.add_argument('-m',
                        '--markdown',
                        action='store_true',
                        help='Parse as markdown file')
    pa = parser.parse_args(sys.argv[1:])

    func = make_notebook
    if pa.markdown:
        func = make_markdown

    func(template_file_name=pa.template,
         tutorial_file_name=pa.tutorial,
         solution_file_name=pa.solution)
