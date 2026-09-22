#include <sourcemod>
#include <sdktools>

#pragma semicolon 1
#pragma newdecls required

public Plugin myinfo = {
    name = "Archipelago Campaign Lock Check",
    author = "Yufii", 
    description = "Checks if current campaign is locked in Archipelago seed",
    version = "1.0",
    url = ""
};

int g_lastFileTime = 0;
ArrayList g_unlockedCampaigns = null;

public void OnPluginStart() {
    HookEvent("player_spawn", Event_PlayerSpawn);
    g_unlockedCampaigns = new ArrayList(ByteCountToCells(64));
    CreateTimer(1.0, Timer_CheckStatusFile, _, TIMER_REPEAT);
}

public void OnPluginEnd() {
    delete g_unlockedCampaigns;
}

public Action Timer_CheckStatusFile(Handle timer) {
    LoadUnlockedCampaigns();
    return Plugin_Continue;
}

public Action Event_PlayerSpawn(Event event, const char[] name, bool dontBroadcast) {
    int client = GetClientOfUserId(GetEventInt(event, "userid"));
    if (!IsValidClient(client)) return Plugin_Continue;
    
    char mapName[64];
    GetCurrentMap(mapName, sizeof(mapName));
    
    char campaignName[64];
    GetCampaignFromMap(mapName, campaignName, sizeof(campaignName));
    
    PrintToServer("[Campaign Lock] Player spawned on map %s (campaign: %s)", mapName, campaignName);
    
    if (IsCampaignLocked(campaignName)) {
        PrintToChatAll("[Archipelago] Campaign '%s' is locked! Disconnecting...", campaignName);
        CreateTimer(1.0, Timer_KickPlayer, GetClientUserId(client));
    } else {
        PrintToServer("[Campaign Lock] Campaign '%s' is unlocked, allowing play", campaignName);
    }
    
    return Plugin_Continue;
}

public Action Timer_KickPlayer(Handle timer, int userid) {
    int client = GetClientOfUserId(userid);
    if (IsValidClient(client)) {
        ClientCommand(client, "disconnect");
    }
    return Plugin_Stop;
}

void GetCampaignFromMap(const char[] mapName, char[] campaign, int maxlen) {
    if (StrContains(mapName, "c1m", false) != -1) {
        strcopy(campaign, maxlen, "Dead Center");
    } else if (StrContains(mapName, "c2m", false) != -1) {
        strcopy(campaign, maxlen, "Dark Carnival");
    } else if (StrContains(mapName, "c3m", false) != -1) {
        strcopy(campaign, maxlen, "Swamp Fever");
    } else if (StrContains(mapName, "c4m", false) != -1) {
        strcopy(campaign, maxlen, "Hard Rain");
    } else if (StrContains(mapName, "c5m", false) != -1) {
        strcopy(campaign, maxlen, "The Parish");
    } else if (StrContains(mapName, "c6m", false) != -1) {
        strcopy(campaign, maxlen, "The Passing");
    } else if (StrContains(mapName, "c7m", false) != -1) {
        strcopy(campaign, maxlen, "The Sacrifice");
    } else if (StrContains(mapName, "c8m", false) != -1) {
        strcopy(campaign, maxlen, "No Mercy");
    } else if (StrContains(mapName, "c9m", false) != -1) {
        strcopy(campaign, maxlen, "Crash Course");
    } else if (StrContains(mapName, "c10m", false) != -1) {
        strcopy(campaign, maxlen, "Death Toll");
    } else if (StrContains(mapName, "c11m", false) != -1) {
        strcopy(campaign, maxlen, "Dead Air");
    } else if (StrContains(mapName, "c12m", false) != -1) {
        strcopy(campaign, maxlen, "Blood Harvest");
    } else if (StrContains(mapName, "c13m", false) != -1) {
        strcopy(campaign, maxlen, "Cold Stream");
    } else if (StrContains(mapName, "c14m", false) != -1) {
        strcopy(campaign, maxlen, "The Last Stand");
    } else {
        strcopy(campaign, maxlen, "Unknown");
    }
}

void LoadUnlockedCampaigns() {
    char statusFile[PLATFORM_MAX_PATH];
    BuildPath(Path_SM, statusFile, sizeof(statusFile), "data/archipelago_status.json");
    
    // Check if file was modified
    int fileTime = GetFileTime(statusFile, FileTime_LastChange);
    if (fileTime == g_lastFileTime) {
        return; // No change
    }
    
    File file = OpenFile(statusFile, "r");
    if (file == null) {
        return;
    }
    
    g_lastFileTime = fileTime;
    g_unlockedCampaigns.Clear();
    
    char buffer[4096];
    ReadFileString(file, buffer, sizeof(buffer));
    CloseHandle(file);
    
    // Find unlocked_campaigns array
    int unlockedStart = StrContains(buffer, "\"unlocked_campaigns\":");
    if (unlockedStart != -1) {
        int arrayStart = StrContains(buffer[unlockedStart], "[");
        if (arrayStart != -1) {
            arrayStart += unlockedStart;
            int arrayEnd = StrContains(buffer[arrayStart], "]");
            if (arrayEnd != -1) {
                char arraySection[1024];
                int copyLen = (arrayEnd < sizeof(arraySection) - 1) ? arrayEnd : sizeof(arraySection) - 1;
                for (int i = 0; i < copyLen; i++) {
                    arraySection[i] = buffer[arrayStart + i];
                }
                arraySection[copyLen] = '\0';
                
                // Parse campaign names from array
                char campaigns[][] = {"Dead Center", "The Passing", "Dark Carnival", "Swamp Fever", "Hard Rain", "The Parish", "Cold Stream", "No Mercy", "Crash Course", "Death Toll", "Dead Air", "Blood Harvest", "The Sacrifice", "The Last Stand"};
                
                for (int i = 0; i < sizeof(campaigns); i++) {
                    char searchPattern[128];
                    Format(searchPattern, sizeof(searchPattern), "\"%s\"", campaigns[i]);
                    if (StrContains(arraySection, searchPattern, false) != -1) {
                        g_unlockedCampaigns.PushString(campaigns[i]);
                    }
                }
            }
        }
    }
    
    PrintToServer("[Campaign Lock] Loaded %d unlocked campaigns", g_unlockedCampaigns.Length);
}

bool IsCampaignLocked(const char[] campaignName) {
    if (g_unlockedCampaigns == null) {
        LoadUnlockedCampaigns();
    }
    
    // Check if campaign is in unlocked list
    char campaign[64];
    for (int i = 0; i < g_unlockedCampaigns.Length; i++) {
        g_unlockedCampaigns.GetString(i, campaign, sizeof(campaign));
        if (StrEqual(campaign, campaignName, false)) {
            PrintToServer("[Campaign Lock] Campaign '%s' is UNLOCKED", campaignName);
            return false;
        }
    }
    
    PrintToServer("[Campaign Lock] Campaign '%s' is LOCKED", campaignName);
    return true;
}

bool IsValidClient(int client) {
    return (client > 0 && client <= MaxClients && IsClientInGame(client) && !IsFakeClient(client));
}