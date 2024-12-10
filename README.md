# ASYC
An LLM-powered command line assistant for generating bash commands to accomplish tasks. 

# Quick start

```bash
export OPENAI_API_KEY = "..."
```

Make `main.py` executable, rename to **asyc** and add to `PATH` (MacOS/Linux):
```bash
chmod +x main.py
mv main.py asyc
export PATH="/path/to/execuable/asyc"
```

# Features

* The default `asyc` command will allow the user to provide a prompt for the task they wish to accomplish to receive a suggested bash command.
* The `bg` argument allows a version of `asyc` to run in the background, allowing the user to enter terminal commands as normal.
* In background mode, the user can use the command `!help` to analyse any error messages from the latest command and provide suggestions to correct it.
* Users can switch to prompt mode with the `!ask` command. 
* The `exit` command quits ASYC. 
