#include <sourcemod>
#include <sdktools>

#pragma semicolon 1
#pragma newdecls required

public Plugin myinfo = {
    name = "Archipelago Mutation Check",
    author = "Yufii",
    description = "Ensures Archipelago mutation is active before running Archipelago plugins",
    version = "1.0",
    url = ""
};

public void OnPluginStart() {
    HookEvent("player_spawn", Event_PlayerSpawn);
    HookEvent("round_start", Event_RoundStart);
}

public Action Event_RoundStart(Event event, const char[] name, bool dontBroadcast) {
    CreateTimer(2.0, Timer_CheckMutation);
    return Plugin_Continue;
}

public Action Event_PlayerSpawn(Event event, const char[] name, bool dontBroadcast) {
    int client = GetClientOfUserId(GetEventInt(event, "userid"));
    if (!IsValidClient(client)) return Plugin_Continue;
    
    if (!IsArchipelagoMutationActive()) {
        PrintToChat(client, "[Archipelago] To play Archipelago, use the 'Archipelago' mutation mode!");
    }
    
    return Plugin_Continue;
}

public Action Timer_CheckMutation(Handle timer) {
    if (!IsArchipelagoMutationActive()) {
        // Disable other Archipelago plugins
        ServerCommand("sm plugins unload archipelago_campaign_check_final");
        ServerCommand("sm plugins unload l4d2_archipelago_locations");
        ServerCommand("sm plugins unload l4d2_item_spawner");
        ServerCommand("sm plugins unload l4d2_item_remover");
        ServerCommand("sm plugins unload archipelago_map_only");
    } else {
        // Enable other Archipelago plugins
        ServerCommand("sm plugins load archipelago_campaign_check_final");
        ServerCommand("sm plugins load l4d2_archipelago_locations");
        ServerCommand("sm plugins load l4d2_item_spawner");
        ServerCommand("sm plugins load l4d2_item_remover");
        ServerCommand("sm plugins load archipelago_map_only");
    }
    
    return Plugin_Stop;
}



bool IsArchipelagoMutationActive() {
    ConVar mutationCvar = FindConVar("mp_gamemode");
    if (mutationCvar == null) return false;
    
    char gamemode[64];
    mutationCvar.GetString(gamemode, sizeof(gamemode));
    
    // Check if gamemode is directly set to archipelago
    return StrEqual(gamemode, "archipelago", false);
}

bool IsValidClient(int client) {
    return (client > 0 && client <= MaxClients && IsClientInGame(client) && !IsFakeClient(client));
}