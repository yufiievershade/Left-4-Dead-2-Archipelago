#include <sourcemod>
#include <sdktools>
#include <sdkhooks>

#define PLUGIN_VERSION "1.0"

public Plugin myinfo = {
    name = "Archipelago Item Restorer",
    author = "Yufii",
    description = "Restores unlocked Archipelago items to vanilla locations",
    version = PLUGIN_VERSION,
    url = ""
};

bool IsArchipelagoMutationActive() {
    ConVar mutationCvar = FindConVar("mp_gamemode");
    if (mutationCvar == null) return false;

    char gamemode[64];
    mutationCvar.GetString(gamemode, sizeof(gamemode));

    // Check if gamemode is directly set to archipelago
    return StrEqual(gamemode, "archipelago", false);
}

void ParseArchipelagoStatus(const char[] jsonPath, ArrayList unlockedItems) {
    File file = OpenFile(jsonPath, "r");
    if (file == null) return;

    char line[256];
    bool inUnlockedArray = false;
    char currentArrayName[64];

    while (!file.EndOfFile() && file.ReadLine(line, sizeof(line))) {
        TrimString(line);

        // Check for array definitions - both unlocked and locked arrays
        if (StrContains(line, "\"") != -1 && StrContains(line, "[") != -1) {
            // Extract array name (e.g., "unlocked_healing", "locked_healing")
            int startQuote = StrContains(line, "\"");
            int endQuote = StrContains(line[startQuote+1], "\"");
            if (endQuote != -1) {
                strcopy(currentArrayName, sizeof(currentArrayName), line[startQuote+1]);
                currentArrayName[endQuote] = '\0';

                // Only collect from unlocked arrays
                if (StrContains(currentArrayName, "unlocked_") == 0) {
                    inUnlockedArray = true;
                } else {
                    inUnlockedArray = false;
                }
            }
            continue;
        }

        // Check for end of current array
        if (StrContains(line, "]") != -1) {
            inUnlockedArray = false;
            currentArrayName[0] = '\0';
            continue;
        }

        // Collect items only from unlocked arrays
        if (inUnlockedArray && StrContains(line, "\"") != -1) {
            char itemName[64];
            if (GetItemNameFromJSONLine(line, itemName, sizeof(itemName))) {
                unlockedItems.PushString(itemName);
            }
        }
    }

    file.Close();
}

bool GetItemNameFromJSONLine(const char[] line, char[] itemName, int maxlen) {
    char trimmed[256];
    strcopy(trimmed, sizeof(trimmed), line);
    TrimString(trimmed);

    // Remove quotes and comma
    ReplaceString(trimmed, sizeof(trimmed), "\"", "");
    ReplaceString(trimmed, sizeof(trimmed), ",", "");

    TrimString(trimmed);
    strcopy(itemName, maxlen, trimmed);
    return strlen(itemName) > 0;
}

bool IsItemUnlocked(const char[] itemName, ArrayList unlockedItems) {
    char checkName[64];
    for (int i = 0; i < unlockedItems.Length; i++) {
        unlockedItems.GetString(i, checkName, sizeof(checkName));
        if (StrEqual(checkName, itemName, false)) {
            return true;
        }
    }
    return false;
}

void ReadSpawnData(const char[] spawnPath, ArrayList spawnData) {
    File file = OpenFile(spawnPath, "r");
    if (file == null) return;

    char line[256];
    while (!file.EndOfFile() && file.ReadLine(line, sizeof(line))) {
        TrimString(line);
        if (strlen(line) > 0) {
            spawnData.PushString(line);
        }
    }

    file.Close();
}

bool ShouldRestoreSpawn(const char[] classname) {
    // Never restore gas cans - they have special gameplay importance
    if (StrEqual(classname, "weapon_gascan") ||
        StrEqual(classname, "weapon_gascan_spawn") ||
        StrEqual(classname, "weapon_propanetank") ||
        StrEqual(classname, "weapon_propanetank_spawn") ||
        StrEqual(classname, "weapon_oxygentank") ||
        StrEqual(classname, "weapon_oxygentank_spawn") ||
        StrEqual(classname, "prop_fuel_barrel") ||
        StrEqual(classname, "prop_propane_tank") ||
        StrEqual(classname, "prop_oxygen_tank")) {
        return false;
    }
    return true;
}


bool IsSpawnForUnlockedItem(const char[] classname, ArrayList unlockedItems) {
    // Check specific spawn classes against unlocked items
    if (StrEqual(classname, "weapon_first_aid_kit_spawn")) {
        return IsItemUnlocked("First Aid Kit", unlockedItems);
    }
    if (StrEqual(classname, "weapon_defibrillator_spawn")) {
        return IsItemUnlocked("Defib", unlockedItems);
    }
    if (StrEqual(classname, "weapon_adrenaline_spawn")) {
        return IsItemUnlocked("Adrenaline", unlockedItems);
    }
    if (StrEqual(classname, "weapon_pain_pills_spawn")) {
        return IsItemUnlocked("Pills", unlockedItems);
    }
    if (StrEqual(classname, "weapon_pistol_spawn")) {
        return IsItemUnlocked("Glock", unlockedItems) || IsItemUnlocked("P220 Pistol", unlockedItems);
    }
    if (StrEqual(classname, "weapon_pistol_magnum_spawn")) {
        return IsItemUnlocked("Magnum", unlockedItems);
    }

    // Specific weapon spawns - each spawn class creates a specific weapon type
    if (StrEqual(classname, "weapon_pumpshotgun_spawn")) {
        return IsItemUnlocked("Pump Shotgun", unlockedItems);
    }
    if (StrEqual(classname, "weapon_shotgun_chrome_spawn")) {
        return IsItemUnlocked("Chrome Shotgun", unlockedItems);
    }
    if (StrEqual(classname, "weapon_autoshotgun_spawn")) {
        return IsItemUnlocked("Tactical Shotgun", unlockedItems);
    }
    if (StrEqual(classname, "weapon_shotgun_spas_spawn")) {
        return IsItemUnlocked("Combat Shotgun", unlockedItems);
    }
    if (StrEqual(classname, "weapon_smg_spawn")) {
        return IsItemUnlocked("Submachine Gun", unlockedItems);
    }
    if (StrEqual(classname, "weapon_smg_silenced_spawn")) {
        return IsItemUnlocked("Silenced Submachine Gun", unlockedItems);
    }
    if (StrEqual(classname, "weapon_smg_mp5_spawn")) {
        return IsItemUnlocked("MP5", unlockedItems);
    }
    if (StrEqual(classname, "weapon_rifle_spawn")) {
        return IsItemUnlocked("M-16", unlockedItems);
    }
    if (StrEqual(classname, "weapon_rifle_ak47_spawn")) {
        return IsItemUnlocked("AK-47", unlockedItems);
    }
    if (StrEqual(classname, "weapon_rifle_desert_spawn")) {
        return IsItemUnlocked("Scar-H", unlockedItems);
    }
    if (StrEqual(classname, "weapon_rifle_sg552_spawn")) {
        return IsItemUnlocked("SG 552", unlockedItems);
    }
    if (StrEqual(classname, "weapon_hunting_rifle_spawn")) {
        return IsItemUnlocked("Hunting Rifle", unlockedItems);
    }
    if (StrEqual(classname, "weapon_sniper_military_spawn")) {
        return IsItemUnlocked("Sniper Rifle", unlockedItems);
    }
    if (StrEqual(classname, "weapon_sniper_scout_spawn")) {
        return IsItemUnlocked("Scout", unlockedItems);
    }
    if (StrEqual(classname, "weapon_sniper_awp_spawn")) {
        return IsItemUnlocked("AWP", unlockedItems);
    }

    // Heavy weapons
    if (StrEqual(classname, "weapon_grenade_launcher_spawn")) {
        return IsItemUnlocked("Grenade Launcher", unlockedItems);
    }
    if (StrEqual(classname, "weapon_rifle_m60_spawn")) {
        return IsItemUnlocked("M60", unlockedItems);
    }

    // Grenades
    if (StrEqual(classname, "weapon_pipe_bomb_spawn")) {
        return IsItemUnlocked("Pipe Bomb", unlockedItems);
    }
    if (StrEqual(classname, "weapon_molotov_spawn")) {
        return IsItemUnlocked("Molotov", unlockedItems);
    }
    if (StrEqual(classname, "weapon_vomitjar_spawn")) {
        return IsItemUnlocked("Bile Bomb", unlockedItems);
    }

    // weapon_spawn is a generic spawner that picks from available weapons
    if (StrEqual(classname, "weapon_spawn")) {
        return unlockedItems.Length > 0; // Any unlocked items means weapon_spawn can work
    }

    // weapon_chainsaw_spawn
    if (StrEqual(classname, "weapon_chainsaw_spawn")) {
        return IsItemUnlocked("Chainsaw", unlockedItems);
    }

    // Melee weapons - weapon_melee_spawn creates random melee
    if (StrEqual(classname, "weapon_melee_spawn")) {
        return IsItemUnlocked("Machete", unlockedItems) ||
               IsItemUnlocked("Katana", unlockedItems) ||
               IsItemUnlocked("Fireaxe", unlockedItems) ||
               IsItemUnlocked("Baseball Bat", unlockedItems) ||
               IsItemUnlocked("Cricket Bat", unlockedItems) ||
               IsItemUnlocked("Crowbar", unlockedItems) ||
               IsItemUnlocked("Frying Pan", unlockedItems) ||
               IsItemUnlocked("Golf Club", unlockedItems) ||
               IsItemUnlocked("Guitar", unlockedItems) ||
               IsItemUnlocked("Nightstick", unlockedItems) ||
               IsItemUnlocked("Pitchfork", unlockedItems) ||
               IsItemUnlocked("Shovel", unlockedItems) ||
               IsItemUnlocked("Knife", unlockedItems) ||
               IsItemUnlocked("Chainsaw", unlockedItems) ||
               IsItemUnlocked("Riot Shield", unlockedItems);
    }

    // Weapon upgrades
    if (StrEqual(classname, "upgrade_laser_sight") ||
        StrEqual(classname, "weapon_upgradepack_incendiary") ||
        StrEqual(classname, "weapon_upgradepack_explosive")) {
        return IsItemUnlocked("Laser Sight", unlockedItems) ||
               IsItemUnlocked("Incendiary", unlockedItems) ||
               IsItemUnlocked("Explosive Ammo", unlockedItems);
    }

    // Special items
    if (StrEqual(classname, "weapon_gnome") ||
        StrEqual(classname, "prop_gnome")) {
        return IsItemUnlocked("Gnome Chompski", unlockedItems);
    }
    if (StrEqual(classname, "weapon_fireworkcrate") ||
        StrEqual(classname, "prop_fireworks_crate")) {
        return IsItemUnlocked("Fireworks", unlockedItems);
    }

    return false;
}

bool GetEntityNameFromSpawnClass(const char[] spawnClass, char[] entityName, int maxlen) {
    // Direct mapping for most spawns - they use the same name
    if (StrEqual(spawnClass, "weapon_spawn") ||
        StrEqual(spawnClass, "weapon_melee_spawn")) {
        // weapon_spawn creates a random weapon, weapon_melee_spawn creates a random melee
        strcopy(entityName, maxlen, spawnClass);
        return true;
    }

    // Remove "_spawn" suffix to get the actual entity name
    int len = strlen(spawnClass);
    if (len > 6 && StrEqual(spawnClass[len-6], "_spawn")) {
        char baseName[64];
        strcopy(baseName, sizeof(baseName), spawnClass);
        baseName[len-6] = '\0'; // Remove "_spawn"
        strcopy(entityName, maxlen, baseName);
        return true;
    }

    // Special cases
    if (StrEqual(spawnClass, "upgrade_laser_sight")) {
        strcopy(entityName, maxlen, "upgrade_laser_sight");
        return true;
    }
    if (StrEqual(spawnClass, "upgrade_incendiary_ammo")) {
        strcopy(entityName, maxlen, "upgrade_incendiary_ammo");
        return true;
    }
    if (StrEqual(spawnClass, "upgrade_explosive_ammo")) {
        strcopy(entityName, maxlen, "upgrade_explosive_ammo");
        return true;
    }
    if (StrEqual(spawnClass, "weapon_upgradepack_incendiary")) {
        strcopy(entityName, maxlen, "weapon_upgradepack_incendiary");
        return true;
    }
    if (StrEqual(spawnClass, "weapon_upgradepack_explosive")) {
        strcopy(entityName, maxlen, "weapon_upgradepack_explosive");
        return true;
    }
    if (StrEqual(spawnClass, "weapon_gnome")) {
        strcopy(entityName, maxlen, "weapon_gnome");
        return true;
    }
    if (StrEqual(spawnClass, "prop_gnome")) {
        strcopy(entityName, maxlen, "prop_gnome");
        return true;
    }
    if (StrEqual(spawnClass, "weapon_fireworkcrate")) {
        strcopy(entityName, maxlen, "weapon_fireworkcrate");
        return true;
    }
    if (StrEqual(spawnClass, "prop_fireworks_crate")) {
        strcopy(entityName, maxlen, "prop_fireworks_crate");
        return true;
    }

    return false;
}

public void OnPluginStart() {
    HookEvent("round_start", Event_RoundStart);
    PrintToServer("[Archipelago Item Restorer] Plugin loaded");
}

public Action Event_RoundStart(Event event, const char[] name, bool dontBroadcast) {
    CreateTimer(4.0, Timer_RestoreItems);
    return Plugin_Continue;
}

public Action Timer_RestoreItems(Handle timer) {
    // Check if Archipelago mutation is active before restoring items
    if (!IsArchipelagoMutationActive()) {
        PrintToServer("[Item Restorer] Archipelago mutation not active, skipping item restoration");
        return Plugin_Stop;
    }

    PrintToServer("[Item Restorer] Beginning item restoration process");

    // Read current archipelago status to determine unlocked items
    // Find the most recently updated status file across multiple possible locations
    char candidatePaths[3][PLATFORM_MAX_PATH];
    float lastModifiedTimes[3];
    int validPaths = 0;

    // Check multiple possible locations for the status file
    BuildPath(Path_SM, candidatePaths[validPaths], sizeof(candidatePaths[]), "data/archipelago_status.json");
    if (FileExists(candidatePaths[validPaths])) {
        lastModifiedTimes[validPaths] = float(GetFileTime(candidatePaths[validPaths], FileTime_LastChange));
        validPaths++;
    }

    BuildPath(Path_SM, candidatePaths[validPaths], sizeof(candidatePaths[]), "../../../archipelago_status.json");
    if (FileExists(candidatePaths[validPaths])) {
        lastModifiedTimes[validPaths] = float(GetFileTime(candidatePaths[validPaths], FileTime_LastChange));
        validPaths++;
    }

    BuildPath(Path_SM, candidatePaths[validPaths], sizeof(candidatePaths[]), "../../../../archipelago_status.json");
    if (FileExists(candidatePaths[validPaths])) {
        lastModifiedTimes[validPaths] = float(GetFileTime(candidatePaths[validPaths], FileTime_LastChange));
        validPaths++;
    }

    if (validPaths == 0) {
        PrintToServer("[Item Restorer] Could not find archipelago_status.json in any expected location");
        return Plugin_Stop;
    }

    // Find the most recently modified file
    char statusPath[PLATFORM_MAX_PATH];
    float latestTime = 0.0;

    for (int i = 0; i < validPaths; i++) {
        if (lastModifiedTimes[i] > latestTime) {
            latestTime = lastModifiedTimes[i];
            strcopy(statusPath, sizeof(statusPath), candidatePaths[i]);
        }
    }

    PrintToServer("[Item Restorer] Using status file: %s", statusPath);

    ArrayList unlockedItems = new ArrayList(64);
    ParseArchipelagoStatus(statusPath, unlockedItems);

    PrintToServer("[Item Restorer] Found %d unlocked items", unlockedItems.Length);
    for (int i = 0; i < unlockedItems.Length; i++) {
        char itemName[64];
        unlockedItems.GetString(i, itemName, sizeof(itemName));
        PrintToServer("[Item Restorer] Unlocked item: %s", itemName);
    }

    // Read spawn data
    char spawnPath[PLATFORM_MAX_PATH];
    BuildPath(Path_SM, spawnPath, sizeof(spawnPath), "data/archipelago_spawns_temp.txt");

    if (!FileExists(spawnPath)) {
        PrintToServer("[Item Restorer] Spawn file not found: %s", spawnPath);
        return Plugin_Stop;
    }

    ArrayList spawnData = new ArrayList(256);
    ReadSpawnData(spawnPath, spawnData);

    PrintToServer("[Item Restorer] Read %d spawn entries from file", spawnData.Length);

    // Process each spawn entry
    int restored = 0;
    char spawnLine[256];
    char parts[4][64];
    for (int i = 0; i < spawnData.Length; i++) {
        spawnData.GetString(i, spawnLine, sizeof(spawnLine));

        // Parse classname|x|y|z
        int numParts = ExplodeString(spawnLine, "|", parts, sizeof(parts), sizeof(parts[]));
        if (numParts != 4) continue;

        char classname[64];
        strcopy(classname, sizeof(classname), parts[0]);
        TrimString(classname);

        // Skip gas cans entirely
        if (!ShouldRestoreSpawn(classname)) {
            continue;
        }

        // Check if this spawn corresponds to an unlocked item
        if (!IsSpawnForUnlockedItem(classname, unlockedItems)) {
            continue;
        }

        // Parse coordinates
        float origin[3];
        origin[0] = StringToFloat(parts[1]);
        origin[1] = StringToFloat(parts[2]);
        origin[2] = StringToFloat(parts[3]);

        // Map spawn classname to actual entity name
        char entityName[64];
        if (!GetEntityNameFromSpawnClass(classname, entityName, sizeof(entityName))) {
            PrintToServer("[Item Restorer] Unknown spawn class: %s", classname);
            continue;
        }

        // Spawn the entity
        int entity = CreateEntityByName(entityName);
        if (entity != -1) {
            DispatchSpawn(entity);
            TeleportEntity(entity, origin, NULL_VECTOR, NULL_VECTOR);
            PrintToServer("[Item Restorer] Restored %s (%s) at %.0f %.0f %.0f", entityName, classname, origin[0], origin[1], origin[2]);
            restored++;
        } else {
            PrintToServer("[Item Restorer] Failed to create entity: %s", entityName);
        }
    }

    PrintToServer("[Item Restorer] Restored %d items this round", restored);

    // Clean up
    delete spawnData;
    delete unlockedItems;

    return Plugin_Stop;
}
