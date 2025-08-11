#!/usr/bin/env python3

__all__ = [
    "__title__",
    "__summary__",
    "__version__",
    "__author__",
]

__title__ = "taskrunner"
__summary__ = "Asynchronous Taskrunner"
__version__ = "1.0.0"
__author__ = "Petr Ospalý"

import sys
import argparse
import json
import time
import asyncio
import copy

from jsonschema import validate as json_validate
from jsonschema.exceptions import ValidationError
from pprint import pprint

import scheduler

#
# global defaults
#

DEFAULT_SCHEMA = "schema.json"

#
# exceptions / classes
#

class InvalidJson(Exception):
    pass

class InvalidTask(Exception):
    pass

class DuplicitTask(Exception):
    pass

class InvalidDependencies(Exception):
    pass

#
# functions
#


def get_params():
    """
    Returns params object if CLI arguments are valid or None.

    It will accept a JSON file and validate it against schema.
    """

    parser = argparse.ArgumentParser(
        description="Asynchronous Taskrunner")

    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s ' + __version__)

    parser.add_argument("-s", "--schema",
                        required=False,
                        metavar="<schema-file>",
                        help="Schema filename and path"
                        " (Default: %s)" % DEFAULT_SCHEMA)

    parser.add_argument("-f", "--tasks-file",
                        required=True,
                        metavar="<tasks-file>",
                        help="JSON filename and path with tasks")

    parser.add_argument("tasks",
                        nargs='*',
                        metavar="<task name(s)>",
                        help="Explicit name of tasks to be run (dependencies will be added)")

    # validate arguments and feed them to the params object
    args = parser.parse_args()
    params = vars(args)

    if not params['schema']:
        params['schema'] = DEFAULT_SCHEMA

    return params


def get_json_object(filepath):
    js_object = None
    with open(filepath) as f:
        try:
            js_object = json.load(f)
        except json.JSONDecodeError as e:
            print(f"[!] JSON data is invalid:\n  {e}")
            print("[!] Task file could not be loaded - ABORT")
            raise InvalidJson

    return js_object


def validate(myjson, myschema):
    try:
        json_validate(instance=myjson, schema=myschema)
    except ValidationError as e:
        print(f"[!] JSON does not comply with the schema:\n  {e}")
        print("[!] Tasks file is invalid - ABORT")
        raise InvalidJson


def create_structs(task_list):
    taskstruct = {}
    depstruct = {}
    all_names = set()

    for task in task_list:
        name = task['name']

        if name in all_names:
            print(f"[!] Duplicit task name: {name}")
            print("[!] Conflicting task name(s) - ABORT")
            raise DuplicitTask

        all_names.add(name)

        taskstruct[name] = task
        taskstruct[name]['status'] = None # started, finished
        taskstruct[name]['output'] = None
        taskstruct[name]['result'] = None # ok, failed, skipped

        if 'dependencies' in task:
            deps = set(task['dependencies']) # change it to set
        else:
            deps = set()

        taskstruct[name]['dependencies'] = deps
        depstruct[name] = copy.deepcopy(deps)

    return taskstruct, depstruct


def get_deps(task_name, taskstruct, dep_list=set()):
    if task_name not in taskstruct:
        print(f"[!] Unknown dependency: {task_name}")
        print("[!] Invalid dependencies - ABORT")
        raise InvalidDependencies

    if not taskstruct[task_name]['dependencies']:
        return dep_list

    for dep in taskstruct[task_name]['dependencies']:
        dep_list.add(dep)
        dep_list.union(get_deps(dep, taskstruct, dep_list))

    return dep_list


def filter_structs(taskstruct, depstruct, explicit_tasks):
    all_names = set(x for x in taskstruct)
    check_list = set(explicit_tasks)
    complete_list = set()

    for name in taskstruct:
        if name in explicit_tasks:
            check_list.discard(name)
            complete_list.add(name)
            complete_list = complete_list.union(get_deps(name,
                                                         taskstruct))

    # this should be empty
    if check_list:
        print(f"[!] Unknown task(s):\n  {check_list}")
        print("[!] Invalid task name(s) - ABORT")
        raise InvalidTask

    # double-checking if deps are valid or not
    if not complete_list.issubset(all_names):
        print("[!] Invalid dependencies - ABORT")
        raise InvalidDependencies

    # we want to do this only if we have something in explicit_tasks
    if explicit_tasks:
        # filtering out all unwanted or unneeded tasks
        for task_name in all_names:
            if task_name not in complete_list:
                del taskstruct[task_name]
                del depstruct[task_name]

    return taskstruct, depstruct


def report_summary(taskstruct, mytime):
    print("***************")
    print("*** SUMMARY ***")
    print("***************\n")

    for task_name in taskstruct:
        print(f"[{task_name}]\t:\t{taskstruct[task_name]['result']}")

    runtime = mytime['end'] - mytime['start']
    print(f"\nProgram took {runtime:.2f} secs to finish")


def main():
    params = get_params()

    try:
        tasks = get_json_object(params['tasks_file'])
    except InvalidJson:
        return 1

    try:
        schema = get_json_object(params['schema'])
    except InvalidJson:
        return 1

    try:
        validate(tasks, schema)
    except InvalidJson:
        return 1

    task_list = tasks['tasks'] # dropping dictionary
    explicit_tasks = params['tasks']

    # convert lists to something more useful
    try:
        taskstruct, depstruct = create_structs(task_list)
        if explicit_tasks:
            taskstruct, depstruct = filter_structs(taskstruct,
                                                   depstruct,
                                                   explicit_tasks)
    except InvalidTask:
        return 1
    except InvalidDependencies:
        return 1
    except DuplicitTask:
        return 1

    print("About to run (tasks and dependencies):")
    #pprint(taskstruct)
    print("---")
    pprint(depstruct, width=1)
    print("=================================\n")

    mytime = {}
    mytime['start'] = time.time()
    mytime['start_nice'] = time.strftime('%X',
                                    time.localtime(mytime['start']))
    print("###")
    print(f"### [PROGRAM STARTED]: {mytime['start_nice']}")
    print("###\n")

    asyncio.run(scheduler.run(taskstruct, depstruct))

    mytime['end'] = time.time()
    mytime['end_nice'] = time.strftime('%X',
                                    time.localtime(mytime['end']))

    print("\n###")
    print(f"### [PROGRAM FINISHED]: {mytime['end_nice']}")
    print("###")

    print("\n---\n")
    report_summary(taskstruct, mytime)
    #pprint(taskstruct)

    return 0


if __name__ == "__main__":
    sys.exit(main())
