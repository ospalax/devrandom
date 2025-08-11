#!/usr/bin/env python3

import asyncio
import time


def all_tasks_done(tasks):
    for name in tasks:
        if tasks[name]['status'] != 'finished':
            return False

    return True


async def shell_runner(task_name, tasks):
    cmd = tasks[task_name]['arguments']
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    if proc.returncode == 0:
        result = 'ok'
    else:
        result = 'failed'

    output = ''

    print(f'   >[{task_name}] CODE: exited with {proc.returncode}')
    if stdout:
        print(f'   >[{task_name}] STDOUT:\n{stdout.decode()}')
        output += str(stdout.decode())
    if stderr:
        print(f'   >[{task_name}] STDERR:\n{stderr.decode()}')
        output += stderr.decode()

    return result, output


def inplace_runner(task_name, tasks):
    cmd = tasks[task_name]['arguments']

    print(f'   >[{task_name}] running inplace python...')

    result = 'ok'
    output = ''
    try:
        output = exec(cmd)
    except:
        result = 'failed'


    if output:
        print(f'   >[{task_name}] OUTPUT:\n{output}')

    return result, output


def remove_dep(task_name, deps):
    for name in deps:
        deps[name].discard(task_name)

    del deps[task_name]


def check_deps(task_name, tasks):
    for dep_name in tasks[task_name]['dependencies']:
        if tasks[dep_name]['result'] == 'failed':
            return False

    return True


async def runner(task_name, tasks, deps):
    if check_deps(task_name, tasks):
        print(f"[+] Started task: {task_name}")

        if tasks[task_name]['type'] == 'exec':
            result, output = await shell_runner(task_name, tasks)
        elif tasks[task_name]['type'] == 'eval':
            loop = asyncio.get_running_loop()
            result, output = await loop.run_in_executor(None,
                                                inplace_runner,
                                                task_name,
                                                tasks)
            output = ''
        else:
            print(f"[!] Unknown execution type: {tasks[task_name]['type']}")
            print("[!] Invalid task execution type - ABORT")
            raise ValueError

        # experiments...
        #time.sleep(1)
        #await asyncio.sleep(1)

        print(f"[-] Ended task  : {task_name}")
        tasks[task_name]['status'] = 'finished'
        tasks[task_name]['output'] = output
        tasks[task_name]['result'] = result
    else:
        print(f"[!] Skipped task (failed deps.): {task_name}")
        tasks[task_name]['status'] = 'finished'
        tasks[task_name]['output'] = None
        tasks[task_name]['result'] = 'failed'

    # remove yourself from active tasklist
    remove_dep(task_name, deps)


def prepare_runners(tasks, deps):
    runners = []

    for task_name, dep_list in deps.items():
        if not dep_list:
            task = asyncio.create_task(runner(task_name,
                                              tasks,
                                              deps))
            runners.append(task)
            tasks[task_name]['status'] = 'started'

    return runners


async def run(tasks, deps):
    while not all_tasks_done(tasks):
        runners = prepare_runners(tasks, deps)

        for runner in runners:
            await runner

        # noticed in the docs about stale references...
        # https://docs.python.org/3/library/asyncio-task.html#creating-tasks
        # ...just to be sure
        runners.clear()
