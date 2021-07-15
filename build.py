#!/usr/bin/env python3

# If you are just trying to run the server, ignore that this script exists.
# I'm writing this assuming you're on Linux

import subprocess
import argparse
import os
import shutil


def shell(command, allow_nonzero=False):
    if isinstance(command, str):
        print("$ " + command)
        proc = subprocess.run(command.split())
    elif isinstance(command, list):
        print("$ " + " ".join(command))
        proc = subprocess.run(command)
    else:
        raise ValueError("Not sure how to interpret: " + str(command))

    if proc.returncode != 0 and not allow_nonzero:
        raise RuntimeError("exit code: " + str(proc.returncode))


def clear_folder(folder):
    # https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def cd(dir):
    work_dir = os.getcwd()
    abspath = os.path.abspath(dir)
    print('change to: ' + abspath)
    os.chdir(abspath)
    return work_dir


def build_react():
    go_back = cd('react-app')
    shell('npm run build')
    cd(go_back)


def build():
    print("Build...")
    os.makedirs('build', exist_ok=True)
    clear_folder('build')

    build_react()
    shell('cp -r react-app/build build/static')

    shell('cp -r build-static/. build')

    shell('cp -r flask-server/. build')


def run():
    print("Run...")

    with open('build_key.txt', 'r') as file:
        key = file.read().strip()

    go_back = cd('build')
    shell(['python3', '__main__.py',
           '-r', '../my-rules', 'my-rules', 'default-rules',
           '-k', key])
    cd(go_back)


if __name__ == "__main__":
    argp = argparse.ArgumentParser()

    argp.add_argument(
        "--build", default=True,
        help="Rebuilds the project into the build folder")

    argp.add_argument(
        "--run", default=False,
        help="Runs the flask server once built")

    args = argp.parse_args()

    if args.build:
        build()

    if args.run:
        run()

    print('Done')
