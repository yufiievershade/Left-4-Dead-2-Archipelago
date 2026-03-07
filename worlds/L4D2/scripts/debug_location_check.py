import os
import time

# Check the same paths the companion script checks
L4D2_PATHS = [
    r"C:\Program Files (x86)\Steam\steamapps\common\Left 4 Dead 2",
    r"C:\Program Files\Steam\steamapps\common\Left 4 Dead 2",
    r"D:\Steam\steamapps\common\Left 4 Dead 2",
    r"E:\Steam\steamapps\common\Left 4 Dead 2",
    r"F:\SteamLibrary\steamapps\common\Left 4 Dead 2",
    r"D:\SteamLibrary\steamapps\common\Left 4 Dead 2",
    r"E:\SteamLibrary\steamapps\common\Left 4 Dead 2",
    r"G:\SteamLibrary\steamapps\common\Left 4 Dead 2",
    r"H:\SteamLibrary\steamapps\common\Left 4 Dead 2",
]

print("Checking for location_check.txt files...")

# Dead Center finale location IDs for testing
test_location_ids = [
    69420012,  # Dead Center - Atrium Finale(Ellis)
    69420013,  # Dead Center - Atrium Finale(Rochelle)
    69420014,  # Dead Center - Atrium Finale(Coach)
    69420015,  # Dead Center - Atrium Finale(Nick)
]


def write_test_location(location_id):
    """Write a test location check file"""
    with open("location_check.txt", "w") as f:
        f.write(str(location_id))
    print(f"Wrote test location check: {location_id}")


print("Available test commands:")
print("1-4: Send Dead Center finale location checks")
print("q: Quit")

while True:
    found_files = []
    for l4d2_path in L4D2_PATHS:
        if os.path.exists(l4d2_path):
            location_file = os.path.join(
                l4d2_path,
                "left4dead2",
                "addons",
                "sourcemod",
                "data",
                "archipelago",
                "mod_data",
                "location_check.txt",
            )
            if os.path.exists(location_file):
                try:
                    with open(location_file, "r") as f:
                        content = f.read().strip()
                    found_files.append(f"{location_file}: {content}")
                except Exception as e:
                    found_files.append(f"{location_file}: ERROR - {e}")

    if found_files:
        print("Found location_check.txt files:")
        for file_info in found_files:
            print(f"  {file_info}")
    else:
        print("No location_check.txt files found")

    # Check for user input
    try:
        user_input = (
            input("Enter command (1-4 for test locations, q to quit): ").strip().lower()
        )
        if user_input == "q":
            break
        elif user_input in ["1", "2", "3", "4"]:
            index = int(user_input) - 1
            if index < len(test_location_ids):
                write_test_location(test_location_ids[index])
                print(
                    f"Sent test location check for Dead Center finale (survivor {user_input})"
                )
            else:
                print("Invalid location index")
        else:
            print("Invalid command")
    except KeyboardInterrupt:
        break
    except:
        pass

    time.sleep(1)
