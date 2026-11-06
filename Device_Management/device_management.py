
import os
import shutil
import subprocess


def show_devices():
    print("\nAVAILABLE STORAGE DEVICES")
    print("=========================")

    try:
        result = subprocess.run(
            ["lsblk", "-o", "NAME,SIZE,TYPE,MOUNTPOINTS"],
            capture_output=True,
            text=True,
            check=True
        )

        print(result.stdout)

    except FileNotFoundError:
        print("Error: lsblk command was not found.")

    except subprocess.CalledProcessError:
        print("Error: Could not retrieve storage devices.")


def check_storage():
    while True:
        path = input("\nEnter a mounted storage path (or q to quit): ")

        if path.lower() == "q":
            print("Program ended.")
            break

        if not os.path.isdir(path):
            print("Error: Path does not exist or is not a directory.")
            print("Recovery: Enter a valid mounted storage path.")
            continue

        try:
            usage = shutil.disk_usage(path)

            total = usage.total / (1024 ** 3)
            used = usage.used / (1024 ** 3)
            free = usage.free / (1024 ** 3)

            print("\nSTORAGE INFORMATION")
            print("===================")
            print(f"Total space: {total:.2f} GB")
            print(f"Used space:  {used:.2f} GB")
            print(f"Free space:  {free:.2f} GB")

        except PermissionError:
            print("Error: Permission denied.")
            print("Recovery: Try a storage path you can access.")

        except OSError as error:
            print(f"Storage error: {error}")
            print("Recovery: Check the device connection and try again.")


def main():
    print("DEVICE MANAGEMENT SIMULATOR")
    print("===========================")

    show_devices()
    check_storage()


main()
