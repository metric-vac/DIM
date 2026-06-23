# DIM (Directory Integrity Monitor)
## A CLI tool that monitors directories for any changes

---

## Information

### DIM is an event-driven Python CLI tool that monitors directories in real-time for changes, modifications, and renames. Instead of constantly scanning files and burning CPU cycles, DIM hooks directly into your Operating System's kernel ledger (using `inotify` on Linux, `FSEvents` on macOS, and `ReadDirectoryChangesW` on Windows) via the `watchdog` library. It stays completely idle at 0% CPU until the OS notifies it of a change. When a file is modified, it dynamically hashes only that specific file using your choice of cryptographic algorithm (SHA-256, SHA-1, or MD5) to verify integrity.

---

## Why This Tool Exists
### Important files can be modified, replaced, and deleted without the user knowing. This tool combats that by utilizing OS-level event listeners, offering hardware-accelerated detection speed and absolute precision without impacting system performance.

---

## Features
 * **Event-Driven Architecture:** Uses native OS kernel tracking instead of heavy file-system loops.
 * **Native Rename Detection:** Tracks file renames and moves seamlessly without false "delete/create" triggers.
 * **Dynamic Hashing:** Choose between SHA-256, SHA-1, or MD5 verification on demand.
 * **Persistent Logging:** Automatically records all filesystem events with precise timestamps to `dim.log`.
 * **Recursive Deep Scanning:** Automatically monitors all sub-folders and nested files within the target path.
 * **Ultra Lightweight:** Uses near-zero background memory and CPU resources while idling.

---

## Example
![alt text](image.png)

---

## AI & Package Usage
### I used AI and community tutorials during this project for assistance on how to use `argparse` and how to pivot from a manual polling loop to an event-driven design using `watchdog`. This project helped me bridge the gap between simple script-writing and building optimized, event-driven command-line interfaces.

---

## How To Use
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

## Choosing a hash algorithm

### DIM uses hashing to see if the contents inside a file are modified. To choose from a hash algorithm, you use **-a** or **-algo**
```bash
python main.py -d /path/to/directory -a sha1
```
### You can choose from 3 different hashing algorithms, Sha256, Sha1 and md5

---

### Prerequisites
DIM relies on the `watchdog` library to speak directly to your operating system's kernel. Install it before running the script:

```bash
pip install watchdog
