## Voxpush
This utility lets you run a specific command based on speech recognition which is completely local and is based on [Vosk](https://alphacephei.com/vosk/)

**Note:** In this case this program commits and pushes code to your current branch of the most recently updated local repo and it is not very sophisticated atm as it was created in a matter of an hour or so

## Setup

Install required libraries
`pip install -r requirements. txt`

Set `ROOT_DIR` to desired path where all your git repos are placed, this is reqiured in order to detect changes as and when they are made

The required model is already placed in the repo which is `vosk-model-small-en-in-0.4`
You can use any model from [here](https://alphacephei.com/vosk/models) you will have to extract the zip and mention the path to model in the code

Then set `MODEL_PATH` to the path where the extracted model is located

Then run the script | **Important Note**: You will have to give mic permissions for this right after you run it
`sudo python3 speechkey.py`

## How to start with this tool

```
+-------------------------------+
|         Start Script          |
+-------------------------------+
               |
               | User initiates
               v
+-------------------------------+
|  Display Instructions:        |
|  "Press and hold '`' to       |
|   start speech recognition."  |
+-------------------------------+
               |
               | User action
               v
+-------------------------------+
|  User presses '`' key         |
+-------------------------------+
               |
               | Script action
               v
+-------------------------------+
|  Script listens for speech    |
+-------------------------------+
               |
               | User speaks
               v
+-------------------------------+
|  User says a Git command      |
|  (e.g., "commit and push")    |
+-------------------------------+
               |
               | User releases key
               v
+-------------------------------+
|  Script processes audio       |
|  and converts to text         |
+-------------------------------+
               |
               | Command recognized
               v
+-------------------------------+
|  Find most recently           |
|  modified directory           |
+-------------------------------+
               |
               | Git operations
               v
+-------------------------------+
|  Execute Git command in       |
|  the directory (commit, push) |
+-------------------------------+
               |
               | Wait or Exit
               v
+-------------------------------+
|  Script awaits further        |
|  commands or script           |
|  termination                  |
+-------------------------------+
               |
               | Repeat or Terminate
               v
+-------------------------------+
|  User may press '`' again or  |
|  exit the script              |
+-------------------------------+
```

After you run, you will have to press "`" key on the keyboard for speech to be detected and the tool listens to the speech until the key is pressed.

Once the detection is completed, the script should do its job and should push your code to desired repo's current branch


