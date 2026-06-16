# DIM (Directory Integrity Monitor)
## A CLI tool that monitors directories for any changes

---

## Information

### DIM is a python CLI tool that monitors directories in real-time and looks for changes/modifications. It does that by hashing all files existing in folders and sub-folders using SHA-256 then compares each file's current hash to the originial hash. It's also optimized by checking files metadata to determine whether the file was changed since the last scan or not. It also has changable interval time(How many seconds until the next scan) which can help for performance and to let the user customize.

---

## Why This Tool Exists
### Important files can be modified, replaced and deleted without the user knowing. This tool combats that with its extremely fast detection speed and accuracy when verifiyng file integrity

---

## Features
 * Detects new files
 * Detects file modifications using SHA256 hashing
 * Detects deleted files
 * Configure scan interval
 * Recursive directory scanning
 * Lightweight and dependency-free

---
## Example
![alt text](image.png)

---

## AI Usage
### I used AI in this project for assistance on how to use argparse. I was unfamiliar with the external package and i have never made a CLI tool with flags like this before. With the help of YouTube tutorials and AI, I was able to make use argparse and make a good CLI tool

---

## How To Use

### Prerequisites
Because DIM relies entirely on built-in Python modules, there are **no external dependencies** to install. Simply download the script and run it directly.

## DIM uses flags to choose directories and scan interval time

## Choosing A directory
### To choose a directory you use **-d** or **--dir**

```bash
python main.py -d /path/to/directory
```

## Choosing An Interval Time
### To choose an interval Time, you use **-i** or **--interval**
```bash
python main.py -d /path/to/directory -i 3
```

----
## Achnowledgments 
### I really enjoyed building this project and learned an incredible amount about file systems and cryptographic hashing that will definitely help me in my future development journey. Huge thanks to OwlSec for organizing this competition
