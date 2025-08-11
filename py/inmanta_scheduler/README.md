# taskrunner

Asynchronous scheduler of defined tasks

## Synopsis

Small stand-alone program that can execute a set of tasks with a **maximal level of concurrency** while respecting the dependencies between the tasks. Tasks are defined inside a single JSON file passed as a command-line argument.

## Notes / Requirements

The program uses [jsonschema](https://python-jsonschema.readthedocs.io/en/stable/) which requires **Python 3.9** and higher and uses **python/asyncio** library as a primary concurrency mechanism.

## Usage

If run inside this directory:
```
% python3 taskrunner.py "examples/input1.json"
```

Generally:
```
% python3 taskrunner.py [-s|--schema "schema.json"] <tasks1.json>...
```

## Description

The program expects as an input a json file, conforming to the schema included.

This file contains a list of tasks, each task specifies:
- name
- type (eval or exec)
- arguments
- dependencies (optional)

The following must be respected:
- A task can start executing after all its dependencies have been successfully executed.
- If a dependency fails or is skipped, the task should be skipped.
- A task of type eval has a code snippet as argument, that is to be executed within the main process.
- If the code raises an exception, it is considered failed.
- A task of type exec has a shell command as argument, that is to be executed in a shell. If the return code is none zero, it is considered failed.

The output of the program should provide:
* while executing tasks:
    - a line for the start of a task of the form `Started: %(name)s`
    - a line for the end of a task of the form `Ended : %(name)s`
    - all output produced by the tasks
    - any exception produced by the tasks
* when done:
    - a report with status for each task where the status is either ok, failed or skipped
