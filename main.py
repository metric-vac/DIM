import argparse
import hashlib
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer
except ModuleNotFoundError:
    print("Packages are missing, run 'pip install watchdog'")
    sys.exit()


def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("dim.log", "a") as f:
        f.write(f"[{timestamp}] {message}\n")


def hash_file(filepath, algo="sha256"):
    """Only hashes a file when an event actually triggers, saving massive disk I/O."""
    try:
        hasher = hashlib.new(algo)
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (FileNotFoundError, PermissionError):
        return None
    except ValueError:
        return None


class DirectoryMonitorHandler(FileSystemEventHandler):
    def __init__(self, algo):
        self.algo = algo

    def on_created(self, event):
        if not event.is_directory:
            print(f"[+] File created: {event.src_path}")
            log(f"File created: {event.src_path}")

    def on_deleted(self, event):
        if not event.is_directory:
            print(f"[-] File deleted: {event.src_path}")
            log(f"File deleted: {event.src_path}")

    def on_modified(self, event):
        if not event.is_directory:
            # We only hash the single file that actually changed!
            f_hash = hash_file(event.src_path, self.algo)
            print(
                f"[!] File modified: {event.src_path} (New {self.algo.upper()}: {f_hash})"
            )
            log(f"File modified: {event.src_path}")

    def on_moved(self, event):
        if not event.is_directory:
            print(f"[*] File renamed: {event.src_path} -> {event.dest_path}")
            log(f"File renamed from {event.src_path} to {event.dest_path}")


def main():
    parser = argparse.ArgumentParser(
        description="DIM. An event-driven CLI tool to monitor directory integrity."
    )
    parser.add_argument(
        "-d", "--dir", type=str, required=True, help="Directory to monitor"
    )
    parser.add_argument(
        "-a",
        "--algo",
        type=str,
        default="sha256",
        choices=["sha256", "sha1", "md5"],
        help="Hash algorithm",
    )

    args = parser.parse_args()
    directory = Path(args.dir)

    if not directory.exists():
        print("Error: Path doesn't exist")
        return

    print("========================================================")
    print("  DIM (Directory Integrity Monitor) v2.0 - metric_vac")
    print("========================================================\n")
    print(f"Watching: {directory} using {args.algo.upper()}")
    print("Press Ctrl+C to exit...\n")

    log(f"Starting event monitor on {directory} using {args.algo}")

    # Set up watchdog observer
    event_handler = DirectoryMonitorHandler(algo=args.algo)
    observer = Observer()
    observer.schedule(event_handler, path=str(directory), recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)  # Keeps main thread alive sleep cleanly without burning CPU
    except KeyboardInterrupt:
        print("\nStopping monitor...")
        log("Stopping monitor")
        observer.stop()

    observer.join()


if __name__ == "__main__":
    main()
