#include <sourcemod>
#include <sdktools>

#define PLUGIN_VERSION "1.0"

public Plugin myinfo = {
    name = "L4D2 Archipelago Location Tracker",
    author = "Yufii", 
    description = "Tracks location completions for Archipelago randomizer",
    version = PLUGIN_VERSION,
    url = ""
};

char g_sModDataPath[PLATFORM_MAX_PATH];
bool g_bLocationSent[MAXPLAYERS + 1][256]; // Track sent locations per player
bool g_bGlobalLocationSent[256]; // Global tracking to prevent duplicates across all players
char g_sPreviousMap[MAXPLAYERS + 1][64]; // Track previous map for each player

public void OnPluginStart() {
    // Build mod data path - adjust this path as needed
    BuildPath(Path_SM, g_sModDataPath, sizeof(g_sModDataPath), "data/archipelago/mod_data");
    
    // Create directory if it doesn't exist
    if (!DirExists(g_sModDataPath)) {
        CreateDirectory(g_sModDataPath, 511);
    }
    
    // Hook events for location tracking
    HookEvent("player_transitioned", Event_PlayerTransitioned);
    HookEvent("player_spawn", Event_PlayerSpawn);
    HookEvent("finale_win", Event_FinaleWin);
    HookEvent("player_use", Event_PlayerUse);
    
    PrintToServer("[Archipelago Locations] Plugin loaded");
}

public void OnMapStart() {
    char currentMap[64];
    GetCurrentMap(currentMap, sizeof(currentMap));

    // Check if this is a campaign switch by looking at map prefixes
    char currentCampaign[8];
    if (strlen(currentMap) >= 3) {
        strcopy(currentCampaign, sizeof(currentCampaign), currentMap);
        currentCampaign[3] = '\0'; // Get just "c1m", "c2m", etc.
    }

    // Reset tracking only if switching campaigns
    for (int i = 1; i <= MaxClients; i++) {
        if (!StrEqual(g_sPreviousMap[i], "")) {
            char previousCampaign[8];
            if (strlen(g_sPreviousMap[i]) >= 3) {
                strcopy(previousCampaign, sizeof(previousCampaign), g_sPreviousMap[i]);
                previousCampaign[3] = '\0';

                // If campaign changed, reset tracking
                if (!StrEqual(currentCampaign, previousCampaign)) {
                    strcopy(g_sPreviousMap[i], sizeof(g_sPreviousMap[]), "");
                    for (int j = 0; j < 256; j++) {
                        g_bLocationSent[i][j] = false;
                        g_bGlobalLocationSent[j] = false; // Reset global tracking too
                    }
                }
            }
        }
    }
}

public void Event_PlayerTransitioned(Event event, const char[] name, bool dontBroadcast) {
    int client = GetClientOfUserId(event.GetInt("userid"));
    if (!IsValidClient(client) || !IsPlayerAlive(client)) {
        return;
    }

    char currentMap[64];
    GetCurrentMap(currentMap, sizeof(currentMap));

    // Only send checks if we have a previous map and it's different from current
    if (!StrEqual(g_sPreviousMap[client], "") && !StrEqual(g_sPreviousMap[client], currentMap)) {
        // Determine survivors based on the completed map
        bool isL4D1Map = (StrContains(g_sPreviousMap[client], "c8m", false) == 0 || StrContains(g_sPreviousMap[client], "c9m", false) == 0 || StrContains(g_sPreviousMap[client], "c10m", false) == 0 || StrContains(g_sPreviousMap[client], "c11m", false) == 0 || StrContains(g_sPreviousMap[client], "c12m", false) == 0 || StrContains(g_sPreviousMap[client], "c14m", false) == 0 || StrContains(g_sPreviousMap[client], "c7m", false) == 0);

        char survivors[4][16];
        if (isL4D1Map) {
            strcopy(survivors[0], 16, "francis");
            strcopy(survivors[1], 16, "bill");
            strcopy(survivors[2], 16, "zoey");
            strcopy(survivors[3], 16, "louis");
        } else {
            strcopy(survivors[0], 16, "ellis");
            strcopy(survivors[1], 16, "rochelle");
            strcopy(survivors[2], 16, "coach");
            strcopy(survivors[3], 16, "nick");
        }

        // Send location checks for all 4 survivors with delays
        // Use global tracking to prevent duplicates when multiple players transition
        for (int i = 0; i < 4; i++) {
            int locationId = GetLocationId(g_sPreviousMap[client], survivors[i]);

            if (locationId > 0) {
                int locationIndex = locationId - 69420000;

                // Extra safety check
                if (locationIndex < 0 || locationIndex >= 256) {
                    PrintToServer("[AP ERROR] Location index %d out of bounds for map %s, survivor %s", locationIndex, g_sPreviousMap[client], survivors[i]);
                    continue;
                }

                if (!g_bGlobalLocationSent[locationIndex]) {
                    g_bGlobalLocationSent[locationIndex] = true;
                    g_bLocationSent[client][locationIndex] = true;
                    DataPack pack = new DataPack();
                    pack.WriteCell(locationId);
                    pack.WriteString(survivors[i]);
                    CreateTimer(float(i) * 0.5, Timer_SendDelayedLocationCheck, pack);
                }
            }
        }

        PrintToChat(client, "[AP] Level completed: %s", g_sPreviousMap[client]);
    }

    // Update to current map
    strcopy(g_sPreviousMap[client], sizeof(g_sPreviousMap[]), currentMap);
}

public void Event_PlayerSpawn(Event event, const char[] name, bool dontBroadcast) {
    int client = GetClientOfUserId(event.GetInt("userid"));
    if (!IsValidClient(client)) return;

    // Only set previous map if it's empty (first spawn or after campaign switch)
    if (StrEqual(g_sPreviousMap[client], "")) {
        char currentMap[64];
        GetCurrentMap(currentMap, sizeof(currentMap));
        strcopy(g_sPreviousMap[client], sizeof(g_sPreviousMap[]), currentMap);
    }
}

public void Event_FinaleWin(Event event, const char[] name, bool dontBroadcast) {
    char mapName[64];
    GetCurrentMap(mapName, sizeof(mapName));

    // Only send finale completion if at least one player is alive
    bool anyAlive = false;
    for (int i = 1; i <= MaxClients; i++) {
        if (IsValidClient(i) && IsPlayerAlive(i)) {
            anyAlive = true;
            break;
        }
    }

    if (!anyAlive) {
        return;
    }

    // Determine survivors based on the map
    bool isL4D1Map = (StrContains(mapName, "c8m", false) == 0 || StrContains(mapName, "c9m", false) == 0 || StrContains(mapName, "c10m", false) == 0 || StrContains(mapName, "c11m", false) == 0 || StrContains(mapName, "c12m", false) == 0 || StrContains(mapName, "c14m", false) == 0 || StrContains(mapName, "c7m", false) == 0);

    char survivors[4][16];
    if (isL4D1Map) {
        strcopy(survivors[0], 16, "francis");
        strcopy(survivors[1], 16, "bill");
        strcopy(survivors[2], 16, "zoey");
        strcopy(survivors[3], 16, "louis");
    } else {
        strcopy(survivors[0], 16, "ellis");
        strcopy(survivors[1], 16, "rochelle");
        strcopy(survivors[2], 16, "coach");
        strcopy(survivors[3], 16, "nick");
    }

    // Send finale completion for all 4 survivors with duplicate prevention
    for (int i = 0; i < 4; i++) {
        int locationId = GetLocationId(mapName, survivors[i]);

        if (locationId > 0) {
            int locationIndex = locationId - 69420000;

            // Extra safety check
            if (locationIndex < 0 || locationIndex >= 256) {
                PrintToServer("[AP ERROR] Finale location index %d out of bounds for map %s, survivor %s", locationIndex, mapName, survivors[i]);
                continue;
            }

            if (!g_bGlobalLocationSent[locationIndex]) {
                g_bGlobalLocationSent[locationIndex] = true;

                // Mark as sent for first valid client
                for (int client = 1; client <= MaxClients; client++) {
                    if (IsValidClient(client)) {
                        g_bLocationSent[client][locationIndex] = true;
                        break;
                    }
                }

                DataPack pack = new DataPack();
                pack.WriteCell(locationId);
                pack.WriteString(survivors[i]);
                CreateTimer(float(i) * 0.5, Timer_SendDelayedLocationCheck, pack);
            }
        }
    }

    PrintToChatAll("[AP] Finale completed: %s", mapName);
}

public void OnClientPutInServer(int client) {
    if (IsValidClient(client)) {
        char currentMap[64];
        GetCurrentMap(currentMap, sizeof(currentMap));

        // Set previous map for new players
        strcopy(g_sPreviousMap[client], sizeof(g_sPreviousMap[]), currentMap);

        // Reset location tracking for new players
        for (int j = 0; j < 256; j++) {
            g_bLocationSent[client][j] = false;
        }
    }
}

public void Event_PlayerUse(Event event, const char[] name, bool dontBroadcast) {
    int client = GetClientOfUserId(event.GetInt("userid"));
    if (!IsValidClient(client)) return;
    
    char targetName[64];
    event.GetString("targetname", targetName, sizeof(targetName));
    
    // Check for special collectibles
    if (StrContains(targetName, "gnome", false) != -1) {
        WriteLocationFile(69420231); // Gnome Chompski
        PrintToChat(client, "[AP] Found Gnome Chompski!");
    }
    else if (StrContains(targetName, "moustachio", false) != -1) {
        char mapName[64];
        GetCurrentMap(mapName, sizeof(mapName));
        
        if (StrContains(mapName, "fairgrounds", false) != -1) {
            WriteLocationFile(69420229); // Moustachio Strength
            PrintToChat(client, "[AP] Completed Moustachio Strength!");
        }
        else if (StrContains(mapName, "coaster", false) != -1) {
            WriteLocationFile(69420230); // Moustachio Whack A Mole
            PrintToChat(client, "[AP] Completed Moustachio Whack A Mole!");
        }
    }
}

void WriteLocationFile(int locationId) {
    char filePath[PLATFORM_MAX_PATH];
    Format(filePath, sizeof(filePath), "%s\\location_check.txt", g_sModDataPath);
    
    // Try to create directory first
    if (!DirExists(g_sModDataPath)) {
        CreateDirectory(g_sModDataPath, 511);
    }
    
    File file = OpenFile(filePath, "w");
    if (file != null) {
        char locationStr[32];
        IntToString(locationId, locationStr, sizeof(locationStr));
        file.WriteString(locationStr, false);
        file.Close();
    } else {
        PrintToServer("[AP ERROR] Could not write location file to %s", filePath);
    }
}

int GetLocationId(const char[] mapName, const char[] characterName) {
    int baseId = 69420000;
    
    // Dead Center
    if (StrEqual(mapName, "c1m1_hotel")) {
        if (StrEqual(characterName, "ellis")) return baseId + 0;
        if (StrEqual(characterName, "rochelle")) return baseId + 1;
        if (StrEqual(characterName, "coach")) return baseId + 2;
        if (StrEqual(characterName, "nick")) return baseId + 3;
    }
    else if (StrEqual(mapName, "c1m2_streets")) {
        if (StrEqual(characterName, "ellis")) return baseId + 4;
        if (StrEqual(characterName, "rochelle")) return baseId + 5;
        if (StrEqual(characterName, "coach")) return baseId + 6;
        if (StrEqual(characterName, "nick")) return baseId + 7;
    }
    else if (StrEqual(mapName, "c1m3_mall")) {
        if (StrEqual(characterName, "ellis")) return baseId + 8;
        if (StrEqual(characterName, "rochelle")) return baseId + 9;
        if (StrEqual(characterName, "coach")) return baseId + 10;
        if (StrEqual(characterName, "nick")) return baseId + 11;
    }
    else if (StrEqual(mapName, "c1m4_atrium")) {
        if (StrEqual(characterName, "ellis")) return baseId + 12;
        if (StrEqual(characterName, "rochelle")) return baseId + 13;
        if (StrEqual(characterName, "coach")) return baseId + 14;
        if (StrEqual(characterName, "nick")) return baseId + 15;
    }
    // The Passing
    else if (StrEqual(mapName, "c6m1_riverbank")) {
        if (StrEqual(characterName, "ellis")) return baseId + 17;
        if (StrEqual(characterName, "rochelle")) return baseId + 18;
        if (StrEqual(characterName, "coach")) return baseId + 19;
        if (StrEqual(characterName, "nick")) return baseId + 20;
    }
    else if (StrEqual(mapName, "c6m2_bedlam")) {
        if (StrEqual(characterName, "ellis")) return baseId + 21;
        if (StrEqual(characterName, "rochelle")) return baseId + 22;
        if (StrEqual(characterName, "coach")) return baseId + 23;
        if (StrEqual(characterName, "nick")) return baseId + 24;
    }
    else if (StrEqual(mapName, "c6m3_port")) {
        if (StrEqual(characterName, "ellis")) return baseId + 25;
        if (StrEqual(characterName, "rochelle")) return baseId + 26;
        if (StrEqual(characterName, "coach")) return baseId + 27;
        if (StrEqual(characterName, "nick")) return baseId + 28;
    }
    // Dark Carnival
    else if (StrEqual(mapName, "c2m1_highway")) {
        if (StrEqual(characterName, "ellis")) return baseId + 29;
        if (StrEqual(characterName, "rochelle")) return baseId + 30;
        if (StrEqual(characterName, "coach")) return baseId + 31;
        if (StrEqual(characterName, "nick")) return baseId + 32;
    }
    else if (StrEqual(mapName, "c2m2_fairgrounds")) {
        if (StrEqual(characterName, "ellis")) return baseId + 33;
        if (StrEqual(characterName, "rochelle")) return baseId + 34;
        if (StrEqual(characterName, "coach")) return baseId + 35;
        if (StrEqual(characterName, "nick")) return baseId + 36;
    }
    else if (StrEqual(mapName, "c2m3_coaster")) {
        if (StrEqual(characterName, "ellis")) return baseId + 37;
        if (StrEqual(characterName, "rochelle")) return baseId + 38;
        if (StrEqual(characterName, "coach")) return baseId + 39;
        if (StrEqual(characterName, "nick")) return baseId + 40;
    }
    else if (StrEqual(mapName, "c2m4_barns")) {
        if (StrEqual(characterName, "ellis")) return baseId + 41;
        if (StrEqual(characterName, "rochelle")) return baseId + 42;
        if (StrEqual(characterName, "coach")) return baseId + 43;
        if (StrEqual(characterName, "nick")) return baseId + 44;
    }
    else if (StrEqual(mapName, "c2m5_concert")) {
        if (StrEqual(characterName, "ellis")) return baseId + 45;
        if (StrEqual(characterName, "rochelle")) return baseId + 46;
        if (StrEqual(characterName, "coach")) return baseId + 47;
        if (StrEqual(characterName, "nick")) return baseId + 48;
    }
    // Swamp Fever
    else if (StrEqual(mapName, "c3m1_plankcountry")) {
        if (StrEqual(characterName, "ellis")) return baseId + 49;
        if (StrEqual(characterName, "rochelle")) return baseId + 50;
        if (StrEqual(characterName, "coach")) return baseId + 51;
        if (StrEqual(characterName, "nick")) return baseId + 52;
    }
    else if (StrEqual(mapName, "c3m2_swamp")) {
        if (StrEqual(characterName, "ellis")) return baseId + 53;
        if (StrEqual(characterName, "rochelle")) return baseId + 54;
        if (StrEqual(characterName, "coach")) return baseId + 55;
        if (StrEqual(characterName, "nick")) return baseId + 56;
    }
    else if (StrEqual(mapName, "c3m3_shantytown")) {
        if (StrEqual(characterName, "ellis")) return baseId + 57;
        if (StrEqual(characterName, "rochelle")) return baseId + 58;
        if (StrEqual(characterName, "coach")) return baseId + 59;
        if (StrEqual(characterName, "nick")) return baseId + 60;
    }
    else if (StrEqual(mapName, "c3m4_plantation")) {
        if (StrEqual(characterName, "ellis")) return baseId + 61;
        if (StrEqual(characterName, "rochelle")) return baseId + 62;
        if (StrEqual(characterName, "coach")) return baseId + 63;
        if (StrEqual(characterName, "nick")) return baseId + 64;
    }
    // Hard Rain
    else if (StrEqual(mapName, "c4m1_milltown_a")) {
        if (StrEqual(characterName, "ellis")) return baseId + 65;
        if (StrEqual(characterName, "rochelle")) return baseId + 66;
        if (StrEqual(characterName, "coach")) return baseId + 67;
        if (StrEqual(characterName, "nick")) return baseId + 68;
    }
    else if (StrEqual(mapName, "c4m2_sugarmill_a")) {
        if (StrEqual(characterName, "ellis")) return baseId + 69;
        if (StrEqual(characterName, "rochelle")) return baseId + 70;
        if (StrEqual(characterName, "coach")) return baseId + 71;
        if (StrEqual(characterName, "nick")) return baseId + 72;
    }
    else if (StrEqual(mapName, "c4m3_sugarmill_b")) {
        if (StrEqual(characterName, "ellis")) return baseId + 73;
        if (StrEqual(characterName, "rochelle")) return baseId + 74;
        if (StrEqual(characterName, "coach")) return baseId + 75;
        if (StrEqual(characterName, "nick")) return baseId + 76;
    }
    else if (StrEqual(mapName, "c4m4_milltown_b")) {
        if (StrEqual(characterName, "ellis")) return baseId + 77;
        if (StrEqual(characterName, "rochelle")) return baseId + 78;
        if (StrEqual(characterName, "coach")) return baseId + 79;
        if (StrEqual(characterName, "nick")) return baseId + 80;
    }
    else if (StrEqual(mapName, "c4m5_milltown_escape")) {
        if (StrEqual(characterName, "ellis")) return baseId + 81;
        if (StrEqual(characterName, "rochelle")) return baseId + 82;
        if (StrEqual(characterName, "coach")) return baseId + 83;
        if (StrEqual(characterName, "nick")) return baseId + 84;
    }
    // The Parish
    else if (StrEqual(mapName, "c5m1_waterfront")) {
        if (StrEqual(characterName, "ellis")) return baseId + 85;
        if (StrEqual(characterName, "rochelle")) return baseId + 86;
        if (StrEqual(characterName, "coach")) return baseId + 87;
        if (StrEqual(characterName, "nick")) return baseId + 88;
    }
    else if (StrEqual(mapName, "c5m2_park")) {
        if (StrEqual(characterName, "ellis")) return baseId + 89;
        if (StrEqual(characterName, "rochelle")) return baseId + 90;
        if (StrEqual(characterName, "coach")) return baseId + 91;
        if (StrEqual(characterName, "nick")) return baseId + 92;
    }
    else if (StrEqual(mapName, "c5m3_cemetery")) {
        if (StrEqual(characterName, "ellis")) return baseId + 93;
        if (StrEqual(characterName, "rochelle")) return baseId + 94;
        if (StrEqual(characterName, "coach")) return baseId + 95;
        if (StrEqual(characterName, "nick")) return baseId + 96;
    }
    else if (StrEqual(mapName, "c5m4_quarter")) {
        if (StrEqual(characterName, "ellis")) return baseId + 97;
        if (StrEqual(characterName, "rochelle")) return baseId + 98;
        if (StrEqual(characterName, "coach")) return baseId + 99;
        if (StrEqual(characterName, "nick")) return baseId + 100;
    }
    else if (StrEqual(mapName, "c5m5_bridge")) {
        if (StrEqual(characterName, "ellis")) return baseId + 101;
        if (StrEqual(characterName, "rochelle")) return baseId + 102;
        if (StrEqual(characterName, "coach")) return baseId + 103;
        if (StrEqual(characterName, "nick")) return baseId + 104;
    }
    // The Sacrifice
    else if (StrEqual(mapName, "c7m1_docks")) {
        if (StrEqual(characterName, "francis")) return baseId + 105;
        if (StrEqual(characterName, "bill")) return baseId + 106;
        if (StrEqual(characterName, "zoey")) return baseId + 107;
        if (StrEqual(characterName, "louis")) return baseId + 108;
    }
    else if (StrEqual(mapName, "c7m2_barge")) {
        if (StrEqual(characterName, "francis")) return baseId + 109;
        if (StrEqual(characterName, "bill")) return baseId + 110;
        if (StrEqual(characterName, "zoey")) return baseId + 111;
        if (StrEqual(characterName, "louis")) return baseId + 112;
    }
    else if (StrEqual(mapName, "c7m3_port")) {
        if (StrEqual(characterName, "francis")) return baseId + 113;
        if (StrEqual(characterName, "bill")) return baseId + 114;
        if (StrEqual(characterName, "zoey")) return baseId + 115;
        if (StrEqual(characterName, "louis")) return baseId + 116;
    }
    // No Mercy
    else if (StrEqual(mapName, "c8m1_apartment")) {
        if (StrEqual(characterName, "francis")) return baseId + 117;
        if (StrEqual(characterName, "bill")) return baseId + 118;
        if (StrEqual(characterName, "zoey")) return baseId + 119;
        if (StrEqual(characterName, "louis")) return baseId + 120;
    }
    else if (StrEqual(mapName, "c8m2_subway")) {
        if (StrEqual(characterName, "francis")) return baseId + 121;
        if (StrEqual(characterName, "bill")) return baseId + 122;
        if (StrEqual(characterName, "zoey")) return baseId + 123;
        if (StrEqual(characterName, "louis")) return baseId + 124;
    }
    else if (StrEqual(mapName, "c8m3_sewers")) {
        if (StrEqual(characterName, "francis")) return baseId + 125;
        if (StrEqual(characterName, "bill")) return baseId + 126;
        if (StrEqual(characterName, "zoey")) return baseId + 127;
        if (StrEqual(characterName, "louis")) return baseId + 128;
    }
    else if (StrEqual(mapName, "c8m4_interior")) {
        if (StrEqual(characterName, "francis")) return baseId + 129;
        if (StrEqual(characterName, "bill")) return baseId + 130;
        if (StrEqual(characterName, "zoey")) return baseId + 131;
        if (StrEqual(characterName, "louis")) return baseId + 132;
    }
    else if (StrEqual(mapName, "c8m5_rooftop")) {
        if (StrEqual(characterName, "francis")) return baseId + 133;
        if (StrEqual(characterName, "bill")) return baseId + 134;
        if (StrEqual(characterName, "zoey")) return baseId + 135;
        if (StrEqual(characterName, "louis")) return baseId + 136;
    }
    // Crash Course
    else if (StrEqual(mapName, "c9m1_alleys")) {
        if (StrEqual(characterName, "francis")) return baseId + 137;
        if (StrEqual(characterName, "bill")) return baseId + 138;
        if (StrEqual(characterName, "zoey")) return baseId + 139;
        if (StrEqual(characterName, "louis")) return baseId + 140;
    }
    else if (StrEqual(mapName, "c9m2_lots")) {
        if (StrEqual(characterName, "francis")) return baseId + 141;
        if (StrEqual(characterName, "bill")) return baseId + 142;
        if (StrEqual(characterName, "zoey")) return baseId + 143;
        if (StrEqual(characterName, "louis")) return baseId + 144;
    }
    // Death Toll
    else if (StrEqual(mapName, "c10m1_caves")) {
        if (StrEqual(characterName, "francis")) return baseId + 145;
        if (StrEqual(characterName, "bill")) return baseId + 146;
        if (StrEqual(characterName, "zoey")) return baseId + 147;
        if (StrEqual(characterName, "louis")) return baseId + 148;
    }
    else if (StrEqual(mapName, "c10m2_drainage")) {
        if (StrEqual(characterName, "francis")) return baseId + 149;
        if (StrEqual(characterName, "bill")) return baseId + 150;
        if (StrEqual(characterName, "zoey")) return baseId + 151;
        if (StrEqual(characterName, "louis")) return baseId + 152;
    }
    else if (StrEqual(mapName, "c10m3_ranchhouse")) {
        if (StrEqual(characterName, "francis")) return baseId + 153;
        if (StrEqual(characterName, "bill")) return baseId + 154;
        if (StrEqual(characterName, "zoey")) return baseId + 155;
        if (StrEqual(characterName, "louis")) return baseId + 156;
    }
    else if (StrEqual(mapName, "c10m4_mainstreet")) {
        if (StrEqual(characterName, "francis")) return baseId + 157;
        if (StrEqual(characterName, "bill")) return baseId + 158;
        if (StrEqual(characterName, "zoey")) return baseId + 159;
        if (StrEqual(characterName, "louis")) return baseId + 160;
    }
    else if (StrEqual(mapName, "c10m5_houseboat")) {
        if (StrEqual(characterName, "francis")) return baseId + 161;
        if (StrEqual(characterName, "bill")) return baseId + 162;
        if (StrEqual(characterName, "zoey")) return baseId + 163;
        if (StrEqual(characterName, "louis")) return baseId + 164;
    }
    // Dead Air
    else if (StrEqual(mapName, "c11m1_greenhouse")) {
        if (StrEqual(characterName, "francis")) return baseId + 165;
        if (StrEqual(characterName, "bill")) return baseId + 166;
        if (StrEqual(characterName, "zoey")) return baseId + 167;
        if (StrEqual(characterName, "louis")) return baseId + 168;
    }
    else if (StrEqual(mapName, "c11m2_offices")) {
        if (StrEqual(characterName, "francis")) return baseId + 169;
        if (StrEqual(characterName, "bill")) return baseId + 170;
        if (StrEqual(characterName, "zoey")) return baseId + 171;
        if (StrEqual(characterName, "louis")) return baseId + 172;
    }
    else if (StrEqual(mapName, "c11m3_garage")) {
        if (StrEqual(characterName, "francis")) return baseId + 173;
        if (StrEqual(characterName, "bill")) return baseId + 174;
        if (StrEqual(characterName, "zoey")) return baseId + 175;
        if (StrEqual(characterName, "louis")) return baseId + 176;
    }
    else if (StrEqual(mapName, "c11m4_terminal")) {
        if (StrEqual(characterName, "francis")) return baseId + 177;
        if (StrEqual(characterName, "bill")) return baseId + 178;
        if (StrEqual(characterName, "zoey")) return baseId + 179;
        if (StrEqual(characterName, "louis")) return baseId + 180;
    }
    else if (StrEqual(mapName, "c11m5_runway")) {
        if (StrEqual(characterName, "francis")) return baseId + 181;
        if (StrEqual(characterName, "bill")) return baseId + 182;
        if (StrEqual(characterName, "zoey")) return baseId + 183;
        if (StrEqual(characterName, "louis")) return baseId + 184;
    }
    // Blood Harvest
    else if (StrEqual(mapName, "c12m1_hilltop")) {
        if (StrEqual(characterName, "francis")) return baseId + 185;
        if (StrEqual(characterName, "bill")) return baseId + 186;
        if (StrEqual(characterName, "zoey")) return baseId + 187;
        if (StrEqual(characterName, "louis")) return baseId + 188;
    }
    else if (StrEqual(mapName, "c12m2_traintunnel")) {
        if (StrEqual(characterName, "francis")) return baseId + 189;
        if (StrEqual(characterName, "bill")) return baseId + 190;
        if (StrEqual(characterName, "zoey")) return baseId + 191;
        if (StrEqual(characterName, "louis")) return baseId + 192;
    }
    else if (StrEqual(mapName, "c12m3_bridge")) {
        if (StrEqual(characterName, "francis")) return baseId + 193;
        if (StrEqual(characterName, "bill")) return baseId + 194;
        if (StrEqual(characterName, "zoey")) return baseId + 195;
        if (StrEqual(characterName, "louis")) return baseId + 196;
    }
    else if (StrEqual(mapName, "c12m4_barn")) {
        if (StrEqual(characterName, "francis")) return baseId + 197;
        if (StrEqual(characterName, "bill")) return baseId + 198;
        if (StrEqual(characterName, "zoey")) return baseId + 199;
        if (StrEqual(characterName, "louis")) return baseId + 200;
    }
    else if (StrEqual(mapName, "c12m5_cornfield")) {
        if (StrEqual(characterName, "francis")) return baseId + 201;
        if (StrEqual(characterName, "bill")) return baseId + 202;
        if (StrEqual(characterName, "zoey")) return baseId + 203;
        if (StrEqual(characterName, "louis")) return baseId + 204;
    }
    // Cold Stream
    else if (StrEqual(mapName, "c13m1_alpinecreek")) {
        if (StrEqual(characterName, "ellis")) return baseId + 205;
        if (StrEqual(characterName, "rochelle")) return baseId + 206;
        if (StrEqual(characterName, "coach")) return baseId + 207;
        if (StrEqual(characterName, "nick")) return baseId + 208;
    }
    else if (StrEqual(mapName, "c13m2_southpinestream")) {
        if (StrEqual(characterName, "ellis")) return baseId + 209;
        if (StrEqual(characterName, "rochelle")) return baseId + 210;
        if (StrEqual(characterName, "coach")) return baseId + 211;
        if (StrEqual(characterName, "nick")) return baseId + 212;
    }
    else if (StrEqual(mapName, "c13m3_memorialbridge")) {
        if (StrEqual(characterName, "ellis")) return baseId + 213;
        if (StrEqual(characterName, "rochelle")) return baseId + 214;
        if (StrEqual(characterName, "coach")) return baseId + 215;
        if (StrEqual(characterName, "nick")) return baseId + 216;
    }
    else if (StrEqual(mapName, "c13m4_cutthroatcreek")) {
        if (StrEqual(characterName, "ellis")) return baseId + 217;
        if (StrEqual(characterName, "rochelle")) return baseId + 218;
        if (StrEqual(characterName, "coach")) return baseId + 219;
        if (StrEqual(characterName, "nick")) return baseId + 220;
    }
    // The Last Stand
    else if (StrEqual(mapName, "c14m1_junkyard")) {
        if (StrEqual(characterName, "francis")) return baseId + 221;
        if (StrEqual(characterName, "bill")) return baseId + 222;
        if (StrEqual(characterName, "zoey")) return baseId + 223;
        if (StrEqual(characterName, "louis")) return baseId + 224;
    }
    else if (StrEqual(mapName, "c14m2_lighthouse")) {
        if (StrEqual(characterName, "francis")) return baseId + 225;
        if (StrEqual(characterName, "bill")) return baseId + 226;
        if (StrEqual(characterName, "zoey")) return baseId + 227;
        if (StrEqual(characterName, "louis")) return baseId + 228;
    }
    
    return 0; // No location found
}

public Action Timer_SendDelayedLocationCheck(Handle timer, DataPack pack) {
    pack.Reset();
    int locationId = pack.ReadCell();
    char survivorName[16];
    pack.ReadString(survivorName, sizeof(survivorName));
    delete pack;
    
    WriteLocationFile(locationId);
    
    return Plugin_Stop;
}


bool IsValidClient(int client) {
    return (client > 0 && client <= MaxClients && IsClientInGame(client) && GetClientTeam(client) == 2);
}
