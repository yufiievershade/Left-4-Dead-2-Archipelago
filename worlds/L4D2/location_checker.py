#!/usr/bin/env python3
"""
Location checker for L4D2 Archipelago integration
Monitors game state and triggers location checks
"""

import os
import time
from location_mapping import get_location_id

def trigger_location_check(location_id, mod_data_path="mod_data"):
    """Write location check file for the companion script to pick up"""
    if not os.path.exists(mod_data_path):
        os.makedirs(mod_data_path)
    
    location_file = os.path.join(mod_data_path, "location_check.txt")
    
    # Write location ID to file
    with open(location_file, 'w') as f:
        f.write(str(location_id))
    
    print(f"Triggered location check: {location_id}")

def check_safe_room_entry(map_name, character_name):
    """Check if player entered a safe room and trigger location check"""
    location_id = get_location_id(map_name, character_name)
    
    if location_id:
        trigger_location_check(location_id)
        return True
    else:
        print(f"No location ID found for {map_name} + {character_name}")
        return False

# Example usage for testing
if __name__ == "__main__":
    # Test location check
    check_safe_room_entry("c1m1_hotel", "ellis")