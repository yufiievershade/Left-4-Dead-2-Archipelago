#include <sourcemod>
#include <sdktools>

public Plugin myinfo = {
    name = "L4D2 Archipelago Starting Items",
    author = "Yufii",
    description = "Gives starting loadout to players",
    version = "1.0",
    url = ""
};

char g_sModDataPath[PLATFORM_MAX_PATH];
bool g_bGivenStartingItems[MAXPLAYERS + 1]; // Track if starting items were given

public void OnPluginStart() {
    BuildPath(Path_SM, g_sModDataPath, sizeof(g_sModDataPath), "data/archipelago");
    if (!DirExists(g_sModDataPath)) {
        CreateDirectory(g_sModDataPath, 511);
    }
    
    char modDataPath[PLATFORM_MAX_PATH];
    Format(modDataPath, sizeof(modDataPath), "%s\\mod_data", g_sModDataPath);
    if (!DirExists(modDataPath)) {
        CreateDirectory(modDataPath, 511);
    }
    
    HookEvent("player_spawn", Event_PlayerSpawn);
    
    PrintToServer("[Archipelago Starting Items] Plugin loaded");
}



public void OnMapStart() {
    // Don't reset starting items tracking - only give once per campaign
}

public void Event_PlayerSpawn(Event event, const char[] name, bool dontBroadcast) {
    int client = GetClientOfUserId(GetEventInt(event, "userid"));
    if (IsValidClient(client) && GetClientTeam(client) == 2 && !g_bGivenStartingItems[client]) {
        CreateTimer(2.0, Timer_GiveStartingItems, client, TIMER_FLAG_NO_MAPCHANGE);
    }
}

public Action Timer_GiveStartingItems(Handle timer, int client) {
    if (IsValidClient(client) && IsPlayerAlive(client) && !g_bGivenStartingItems[client]) {
        GiveStartingLoadout(client);
        g_bGivenStartingItems[client] = true;
    }
    return Plugin_Stop;
}



void GiveStartingLoadout(int client) {
    char startingFile[PLATFORM_MAX_PATH];
    Format(startingFile, sizeof(startingFile), "%s\\mod_data\\starting_items.txt", g_sModDataPath);
    
    if (!FileExists(startingFile)) {
        PrintToServer("[Starting Items] No starting_items.txt found, giving default pistol");
        CheatCommand(client, "give", "weapon_pistol");
        return;
    }
    
    File file = OpenFile(startingFile, "r");
    if (file == null) {
        PrintToServer("[Starting Items] Failed to open starting_items.txt");
        return;
    }
    
    char line[64];
    while (file.ReadLine(line, sizeof(line))) {
        TrimString(line);
        if (strlen(line) > 0) {
            // Special handling for scavenge gas cans
            if (StrEqual(line, "Gas Can")) {
                char mapName[64];
                GetCurrentMap(mapName, sizeof(mapName));
                if (StrEqual(mapName, "c1m4_atrium") || StrEqual(mapName, "c6m3_port") || StrEqual(mapName, "c7m3_port")) {
                    SpawnScavengeGasCan(client);
                    PrintToServer("[Starting Items] Spawned scavenge gas can for %N", client);
                    continue;
                }
            }
            
            char entityName[64];
            GetItemEntityName(line, entityName, sizeof(entityName));
            if (!StrEqual(entityName, "")) {
                CheatCommand(client, "give", entityName);
                PrintToServer("[Starting Items] Gave starting item: %s (%s) to %N", line, entityName, client);
            }
        }
    }
    
    file.Close();
}

stock void CheatCommand(int client, const char[] command, const char[] argument1 = "", const char[] argument2 = "") {
    int userFlags = GetUserFlagBits(client);
    SetUserFlagBits(client, ADMFLAG_ROOT);
    int flags = GetCommandFlags(command);
    SetCommandFlags(command, flags & ~FCVAR_CHEAT);
    FakeClientCommand(client, "%s %s %s", command, argument1, argument2);
    SetCommandFlags(command, flags);
    SetUserFlagBits(client, userFlags);
}

bool IsValidClient(int client) {
    return (client > 0 && client <= MaxClients && IsClientConnected(client) && IsClientInGame(client));
}

void SpawnScavengeGasCan(int client) {
    // Try multiple possible entity names for scavenge gas cans
    char entityNames[][] = {
        "weapon_scavenge_item_gascan",
        "prop_physics",
        "weapon_gascan",
        "gascan"
    };
    
    float clientPos[3];
    GetClientAbsOrigin(client, clientPos);
    clientPos[2] += 10.0;
    
    for (int i = 0; i < sizeof(entityNames); i++) {
        int gascan = CreateEntityByName(entityNames[i]);
        if (gascan != -1) {
            if (StrEqual(entityNames[i], "prop_physics")) {
                SetEntityModel(gascan, "models/props_junk/gascan001a.mdl");
            }
            DispatchSpawn(gascan);
            TeleportEntity(gascan, clientPos, NULL_VECTOR, NULL_VECTOR);
            PrintToServer("[Debug] Spawned scavenge gas can using entity: %s", entityNames[i]);
            return;
        }
    }
    PrintToServer("[Debug] Failed to create any scavenge gas can entity");
}

void GetItemEntityName(const char[] itemName, char[] entityName, int maxlen) {
    // Melee weapons
    if (StrEqual(itemName, "Machete")) {
        strcopy(entityName, maxlen, "machete"); 
    }
    else if (StrEqual(itemName, "Cricket Bat")) {
        strcopy(entityName, maxlen, "cricket_bat"); 
    }
    else if (StrEqual(itemName, "Fireaxe")) {
        strcopy(entityName, maxlen, "fireaxe"); 
    }
    else if (StrEqual(itemName, "Baseball Bat")) {
        strcopy(entityName, maxlen, "baseball_bat"); 
    }
    else if (StrEqual(itemName, "Crowbar")) {
        strcopy(entityName, maxlen, "crowbar"); 
    }
    else if (StrEqual(itemName, "Frying Pan")) {
        strcopy(entityName, maxlen, "frying_pan"); 
    }
    else if (StrEqual(itemName, "Golf Club")) {
        strcopy(entityName, maxlen, "golfclub"); 
    }
    else if (StrEqual(itemName, "Guitar")) {
        strcopy(entityName, maxlen, "electric_guitar"); 
    }
    else if (StrEqual(itemName, "Katana")) {
        strcopy(entityName, maxlen, "katana"); 
    }
    else if (StrEqual(itemName, "Nightstick")) {
        strcopy(entityName, maxlen, "tonfa"); 
    }
    else if (StrEqual(itemName, "Pitchfork")) {
        strcopy(entityName, maxlen, "pitchfork"); 
    }
    else if (StrEqual(itemName, "Shovel")) {
        strcopy(entityName, maxlen, "shovel"); 
    }
    else if (StrEqual(itemName, "Knife")) {
        strcopy(entityName, maxlen, "knife"); 
    }
    else if (StrEqual(itemName, "Chainsaw")) {
        strcopy(entityName, maxlen, "chainsaw"); 
    }
    else if (StrEqual(itemName, "Riot Shield")) {
        strcopy(entityName, maxlen, "riotshield"); 
    }
    // Healing items
    else if (StrEqual(itemName, "First Aid Kit")) {
        strcopy(entityName, maxlen, "first_aid_kit");
    }
    else if (StrEqual(itemName, "Pills")) {
        strcopy(entityName, maxlen, "pain_pills");
    }
    else if (StrEqual(itemName, "Adrenaline")) {
        strcopy(entityName, maxlen, "adrenaline");
    }
    else if (StrEqual(itemName, "Defib")) {
        strcopy(entityName, maxlen, "defibrillator");
    }
    // Weapon Upgrades
    else if (StrEqual(itemName, "Laser Sight")) {
        strcopy(entityName, maxlen, "upgrade_laser_sight");
    }
    else if (StrEqual(itemName, "Incendiary")) {
        strcopy(entityName, maxlen, "upgradepack_incendiary");
    }
    else if (StrEqual(itemName, "Explosive Ammo")) {
        strcopy(entityName, maxlen, "upgradepack_explosive");
    }
    // Grenades
    else if (StrEqual(itemName, "Molotov")) {
        strcopy(entityName, maxlen, "molotov");
    }
    else if (StrEqual(itemName, "Pipe Bomb")) {
        strcopy(entityName, maxlen, "pipe_bomb");
    }
    else if (StrEqual(itemName, "Bile Bomb")) {
        strcopy(entityName, maxlen, "vomitjar");
    }
    // T2 Weapons
    else if (StrEqual(itemName, "AK-47")) {
        strcopy(entityName, maxlen, "weapon_rifle_ak47");
    }
    else if (StrEqual(itemName, "M-16")) {
        strcopy(entityName, maxlen, "weapon_rifle");
    }
    else if (StrEqual(itemName, "Scar-H")) {
        strcopy(entityName, maxlen, "weapon_rifle_desert");
    }
    else if (StrEqual(itemName, "SG 552")) {
        strcopy(entityName, maxlen, "weapon_rifle_sg552");
    }
    // T1 Weapons
    else if (StrEqual(itemName, "Submachine Gun")) {
        strcopy(entityName, maxlen, "weapon_smg");
    }
    else if (StrEqual(itemName, "Silenced Submachine Gun")) {
        strcopy(entityName, maxlen, "weapon_smg_silenced");
    }
    else if (StrEqual(itemName, "MP5")) {
        strcopy(entityName, maxlen, "weapon_smg_mp5");
    }
    // Sniper Rifles
    else if (StrEqual(itemName, "Scout")) {
        strcopy(entityName, maxlen, "weapon_sniper_scout");
    }
    else if (StrEqual(itemName, "AWP")) {
        strcopy(entityName, maxlen, "weapon_sniper_awp");
    }
    else if (StrEqual(itemName, "Sniper Rifle")) {
        strcopy(entityName, maxlen, "weapon_sniper_military");
    }
    else if (StrEqual(itemName, "Hunting Rifle")) {
        strcopy(entityName, maxlen, "weapon_hunting_rifle");
    }
    else if (StrEqual(itemName, "Pump Shotgun")) {
        strcopy(entityName, maxlen, "weapon_pumpshotgun");
    }
    else if (StrEqual(itemName, "Chrome Shotgun")) {
        strcopy(entityName, maxlen, "weapon_shotgun_chrome");
    }
    else if (StrEqual(itemName, "Tactical Shotgun")) {
        strcopy(entityName, maxlen, "weapon_autoshotgun");
    }
    else if (StrEqual(itemName, "Combat Shotgun")) {
        strcopy(entityName, maxlen, "weapon_shotgun_spas");
    }
    // Pistols
    else if (StrEqual(itemName, "Glock")) {
        strcopy(entityName, maxlen, "weapon_pistol");
    }
    else if (StrEqual(itemName, "P220 Pistol")) {
        strcopy(entityName, maxlen, "weapon_pistol");
    }
    else if (StrEqual(itemName, "Magnum")) {
        strcopy(entityName, maxlen, "weapon_pistol_magnum");
    }
    // Heavy Weapons
    else if (StrEqual(itemName, "M60")) {
        strcopy(entityName, maxlen, "weapon_rifle_m60");
    }
    else if (StrEqual(itemName, "Grenade Launcher")) {
        strcopy(entityName, maxlen, "weapon_grenade_launcher");
    }
    // Explosives
    else if (StrEqual(itemName, "Propane Tank")) {
        strcopy(entityName, maxlen, "weapon_propanetank");
    }
    else if (StrEqual(itemName, "Oxygen Tank")) {
        strcopy(entityName, maxlen, "weapon_oxygentank");
    }
    else if (StrEqual(itemName, "Gas Can")) {
        strcopy(entityName, maxlen, "weapon_gascan");
    }
    // Misc
    else if (StrEqual(itemName, "Gnome Chompski")) {
        strcopy(entityName, maxlen, "gnome");
    }
    else if (StrEqual(itemName, "Fireworks")) {
        strcopy(entityName, maxlen, "fireworkcrate");
    }
    else {
        strcopy(entityName, maxlen, "");
    }
}