#!/usr/bin/env python3

from openai import OpenAI
import subprocess
import os
import argparse
import sys

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

ERROR_FILE = "last_error.txt"

def get_command(task_description):
    prompt = f"Given this description of a task: '{task_description}', suggest a safe and effective bash command to accomplish it."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True)
    
    if result.returncode != 0:
        with open(ERROR_FILE, "w") as f:
            f.write(result.stderr.decode())
    else:
        if os.path.exists(ERROR_FILE):
            os.remove(ERROR_FILE)
   
    if result.stdout:
        print(result.stdout.decode())
    
    if result.stderr:
        print(result.stderr.decode(), file=sys.stderr)

def suggest_fix():
    if os.path.exists(ERROR_FILE):
        with open(ERROR_FILE, "r") as f:
            error_message = f.read().strip()

        if error_message:
            prompt = f"The following is an error message from a recent command:\n\n{error_message}\n\nSuggest a fix for this error in a condensed and brief form."
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            print("\nSuggested fix for the error:")
            print(response.choices[0].message.content.strip())
        else:
            print("No error message found.")
    else:
        print(f"No error message file found at {ERROR_FILE}.")

def main():
    parser = argparse.ArgumentParser(description="ASY Command Line Assistant")
    parser.add_argument("command", nargs="?", help="Run tool in the background.")

    args = parser.parse_args()

    if args.command == "bg":
        while True:
            cmd = input("(ASYC) ")
            if cmd.lower() == 'exit':
                return 
            elif cmd.lower() == '!help':
                suggest_fix()
            elif cmd.lower() == '!ask':
                break
            else:
                run_command(cmd)

    print("Hello, I am ASYC :)")
    autonomous_mode = input("Enable autonomous mode? (y/n): ").strip().lower() == 'y'
    
    while True:
        task_description = input("\nDescribe the task you'd like to accomplish (or type 'exit' to quit): ")
        if task_description.lower() == 'exit':
            break
        
        command = get_command(task_description)
        print(f"\nSuggested command: {command}")
        
        if autonomous_mode:
            print(f"Executing command: {command}")
            subprocess.run(command, shell=True)
        else:
            action = input("Accept and run the command? (y/n/edit): ").strip().lower()
            if action == 'y':
                subprocess.run(command, shell=True)
            elif action == 'edit':
                command = input("Edit the command: ").strip()
                subprocess.run(command, shell=True)
            else:
                print("Command rejected.")

if __name__ == "__main__":
    main()
