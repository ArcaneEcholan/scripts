#!/usr/bin/python3

import argparse
import pathlib
import subprocess
import os
from pathlib import Path
import json5
import shutil


def get_git_version():
    version = subprocess.check_output(
        ['git', 'describe', '--tags', '--always', '--long', '--abbrev=8']).strip().decode()
    branch_name = subprocess.check_output(
        ['git', 'rev-parse', '--abbrev-ref', 'HEAD']).strip().decode()
    return version, branch_name


def copy_jar_to_remote(jar_name, address, remote_password, remote_directory):
    try:
        # Check if sshpass is installed
        if subprocess.call(['which', 'sshpass']) != 0:
            print("sshpass is not installed, installing it...")
            subprocess.run(['sudo', 'apt-get', 'install',
                           'sshpass', '-y'], check=True)

        # Copy the JAR file to the remote machine
        print(f"Copying JAR file to {address}...")
        scp_command = [
            'sshpass', '-p', remote_password, 'scp',
            f'gw-center-main/target/{jar_name}', f'{address}:{remote_directory}'
        ]
        subprocess.run(scp_command, check=True)

        # Run the command to rename the jar on the remote machine
        print(f"Executing command on the remote machine to rename the JAR file...")
        ssh_command = [
            'sshpass', '-p', remote_password, 'ssh',
            f'{address}', f'cp {remote_directory}/{jar_name} {remote_directory}/ndsec_gw_center.jar'
        ]
        subprocess.run(ssh_command, check=True)

        print("JAR file successfully copied and renamed on the remote machine.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        exit(1)


if __name__ == "__main__":
    version, branch_name = get_git_version()
    jar_name = f"ndsec_gw_center-{version}.jar"

    # Copy the JAR file locally with the new name
    src_jar = "gw-center-main/target/ndsec_gw_center.jar"
    dest_jar = f"gw-center-main/target/{jar_name}"
    if os.path.exists(src_jar):
        print(f"Copying local JAR file to {dest_jar}...")
        shutil.copyfile(src_jar, dest_jar)
    else:
        print(f"Source JAR file {src_jar} not found.")
        exit(1)

    parser = argparse.ArgumentParser(
        description="Read pdfname.json from the parent folder.")
    parser.add_argument(
        "--parent-dir", "-p",
        type=str,
        default=pathlib.Path.cwd(),  # Default to current working directory
        help="The path to the parent directory (optional, defaults to current working directory)"
    )
    args = parser.parse_args()

    pd = pathlib.Path(args.parent_dir)

    config_file = pd / "tcd.json"

    if config_file.exists() and config_file.is_file():
        # Read the JSON file into a dictionary
        with open(config_file, 'r') as file:
            config_data = json5.load(file)
        print("Config file content:", config_data)

        for entry in config_data:
            copy_jar_to_remote(jar_name, entry['address'],
                               entry['credential'], remote_directory="/home/admin")

    else:
        print(f"Config file {config_file} not found.")
