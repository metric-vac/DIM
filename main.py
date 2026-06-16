try:
    import sys
    import argparse
    import hashlib
    from pathlib import Path
    import time
except ModuleNotFoundError:
    print("Packages are missing, run 'pip install -r requirements.txt'")
    sys.exit()


def sha256_file(filepath):
    sha256 = hashlib.sha256()

    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except (FileNotFoundError, PermissionError):
        return None


def get_file_info(file):
    """Helper to safely get file metadata"""
    try:
        info = file.stat()
        return {
            "size": info.st_size,
            "mtime": info.st_mtime_ns,
            "hash": sha256_file(file)
        }
    except FileNotFoundError:
        return None


def main():
    # Setup argparse with the new flags
    parser = argparse.ArgumentParser(
        description="DIM. A CLI tool to hash and monitor changes in a directory."
    )
    parser.add_argument(
        "-d", "--dir",
        type=str,
        required=True,
        help="The path to the directory you want to monitor"
    )
    parser.add_argument(
        "-i", "--interval",
        type=float,
        default=1.0,
        help="Seconds to wait between scans (default: 1.0)"
    )
    
    args = parser.parse_args()

    hashed = {}

    print("========================================================")
    print("  DIM (Directory Integrity Monitor) v1.0 - Metric_vac")
    print("========================================================\n")

    # Use the arguments passed via flags
    directory = Path(args.dir)
    scan_interval = args.interval

    if not directory.exists():
        print("Error: Path doesn't exist")
        return

    # Initial scan
    print("\n================")
    print("Hashing initial snapshot...")
    print("================")

    for file in directory.rglob("*"):
        if file.is_file():
            info = get_file_info(file)
            if info and info["hash"]:
                hashed[str(file)] = info
                print(f"Hashed {file}")

    print("================")
    print(f"Watching directory every {scan_interval}s...\nCntrl - C to exit")
    print("================\n")

    try:
        while True:
            current_snapshot = {}

            # Build current snapshot 
            for file in directory.rglob("*"):
                if file.is_file():
                    info = get_file_info(file)
                    if info and info["hash"]:
                        current_snapshot[str(file)] = info

                        path = str(file)

                        # NEW FILE
                        if path not in hashed:
                            print("[+] File created:", file)

                        # MODIFIED FILE
                        else:
                            old = hashed[path]

                            if info["hash"] != old["hash"]:
                                print("[!] File modified:", file)

            # DELETED FILES
            for path in list(hashed):
                if path not in current_snapshot:
                    print("[-] File deleted:", path)

            # Update state 
            hashed = current_snapshot

            # Use the dynamic interval instead of hardcoded 1
            time.sleep(scan_interval)

    except KeyboardInterrupt:
        print("\nExiting...")


if __name__ == "__main__":
    main()