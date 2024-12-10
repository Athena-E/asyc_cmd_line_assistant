#!/usr/bin/env python3

from openai import OpenAI
import subprocess
import os

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def get_command(task_description):
    prompt = f"Given this description of a task: '{task_description}', suggest a safe and effective bash command to accomplish it."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def main():
    print("Hello, I am ASYC")
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
