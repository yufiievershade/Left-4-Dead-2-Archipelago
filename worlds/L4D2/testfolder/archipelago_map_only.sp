#include <sourcemod>
#include <sdktools>

#pragma semicolon 1
#pragma newdecls required

#define PLUGIN_VERSION "1.0"

public Plugin myinfo = {
    name = "Archipelago Map Item Remover",
    author = "Yufii",
    description = "Removes all default map items",
    version = PLUGIN_VERSION,
    url = ""
};

public void OnPluginStart() {
    HookEvent("round_start", Event_RoundStart);
    PrintToServer("[Archipelago Map Remover] Plugin loaded");
}

public Action Event_RoundStart(Event event, const char[] name, bool dontBroadcast) {
    CreateTimer(3.0, Timer_ReplaceMapItems);
    // Remove second pass - items should spawn immediately on round start
    return Plugin_Continue;
}

public Action Timer_ReplaceMapItems(Handle timer) {
    // Check if Archipelago mutation is active before removing items
    if (!IsArchipelagoMutationActive()) {
        PrintToServer("[Map Remover] Archipelago mutation not active, skipping item removal");
        return Plugin_Stop;
    }
    
    PrintToServer("[Map Remover] Scanning for items to remove");
    
    // Open file to save spawn positions
    char spawnFilePath[PLATFORM_MAX_PATH];
    BuildPath(Path_SM, spawnFilePath, sizeof(spawnFilePath), "data/archipelago_spawns_temp.txt");
    File spawnFile = OpenFile(spawnFilePath, "w");
    if (spawnFile == null) {
        PrintToServer("[Map Remover] Failed to create spawn positions file");
    }
    
    int removed = 0;
    int maxEntities = GetMaxEntities();
    char classname[64];
    
    for (int entity = 1; entity < maxEntities; entity++) {
        if (!IsValidEntity(entity)) continue;
        
        GetEntityClassname(entity, classname, sizeof(classname));
        
        // Check for explosive props by model name if it's a prop_physics
        if (StrEqual(classname, "prop_physics")) {
            char modelname[128];
            GetEntPropString(entity, Prop_Data, "m_ModelName", modelname, sizeof(modelname));
            if (StrContains(modelname, "gascan", false) != -1 ||
                StrContains(modelname, "propane", false) != -1 ||
                StrContains(modelname, "oxygen", false) != -1) {
                // Don't remove gas cans on scavenge finale maps
                char mapName[64];
                GetCurrentMap(mapName, sizeof(mapName));
                if (StrContains(modelname, "gascan", false) != -1 && 
                    (StrEqual(mapName, "c1m4_atrium") || StrEqual(mapName, "c6m3_port") || StrEqual(mapName, "c7m3_port"))) {
                    continue; // Skip removal on scavenge finales
                }
                float origin[3];
                GetEntPropVector(entity, Prop_Send, "m_vecOrigin", origin);
                AcceptEntityInput(entity, "Kill");
                PrintToServer("[Map Remover] Removed explosive prop %s (model: %s) at %.0f %.0f %.0f", classname, modelname, origin[0], origin[1], origin[2]);
                removed++;
                continue;
            }
        }
        
        // Remove ALL weapon, item, and prop spawns
        if (StrEqual(classname, "weapon_first_aid_kit_spawn") ||
            StrEqual(classname, "weapon_defibrillator_spawn") ||
            StrEqual(classname, "weapon_adrenaline_spawn") ||
            StrEqual(classname, "weapon_pain_pills_spawn") ||
            StrEqual(classname, "weapon_shotgun_chrome_spawn") ||
            StrEqual(classname, "weapon_pumpshotgun_spawn") ||
            StrEqual(classname, "weapon_autoshotgun_spawn") ||
            StrEqual(classname, "weapon_shotgun_spas_spawn") ||
            StrEqual(classname, "weapon_smg_spawn") ||
            StrEqual(classname, "weapon_smg_silenced_spawn") ||
            StrEqual(classname, "weapon_smg_mp5_spawn") ||
            StrEqual(classname, "weapon_rifle_spawn") ||
            StrEqual(classname, "weapon_rifle_ak47_spawn") ||
            StrEqual(classname, "weapon_rifle_desert_spawn") ||
            StrEqual(classname, "weapon_rifle_sg552_spawn") ||
            StrEqual(classname, "weapon_hunting_rifle_spawn") ||
            StrEqual(classname, "weapon_sniper_military_spawn") ||
            StrEqual(classname, "weapon_sniper_scout_spawn") ||
            StrEqual(classname, "weapon_sniper_awp_spawn") ||
            StrEqual(classname, "weapon_pipe_bomb_spawn") ||
            StrEqual(classname, "weapon_molotov_spawn") ||
            StrEqual(classname, "weapon_vomitjar_spawn") ||
            StrEqual(classname, "weapon_pistol_spawn") ||
            StrEqual(classname, "weapon_pistol_magnum_spawn") ||
            StrEqual(classname, "weapon_melee_spawn") ||
            StrEqual(classname, "weapon_chainsaw_spawn") ||
            StrEqual(classname, "weapon_grenade_launcher_spawn") ||
            StrEqual(classname, "weapon_rifle_m60_spawn") ||
            StrEqual(classname, "weapon_spawn") ||
            // Weapon upgrades
            StrEqual(classname, "upgrade_laser_sight") ||
            StrEqual(classname, "upgrade_incendiary_ammo") ||
            StrEqual(classname, "upgrade_explosive_ammo") ||
            StrEqual(classname, "weapon_upgradepack_incendiary") ||
            StrEqual(classname, "weapon_upgradepack_explosive") ||
            // Explosive props - all variations (except gas cans on scavenge finales)
            (StrEqual(classname, "weapon_gascan") && !IsScavengeFinale()) ||
            StrEqual(classname, "weapon_propanetank") ||
            StrEqual(classname, "weapon_oxygentank") ||
            StrEqual(classname, "prop_fuel_barrel") ||
            StrEqual(classname, "prop_propane_tank") ||
            StrEqual(classname, "prop_oxygen_tank") ||
            (StrEqual(classname, "weapon_gascan_spawn") && !IsScavengeFinale()) ||
            StrEqual(classname, "weapon_propanetank_spawn") ||
            StrEqual(classname, "weapon_oxygentank_spawn") ||
            // Special items
            StrEqual(classname, "weapon_gnome") ||
            StrEqual(classname, "prop_gnome") ||
            StrEqual(classname, "weapon_fireworkcrate") ||
            StrEqual(classname, "prop_fireworks_crate")) {
            
            float origin[3];
            GetEntPropVector(entity, Prop_Send, "m_vecOrigin", origin);
            
            // Save spawn position to file before removing
            if (spawnFile != null) {
                spawnFile.WriteLine("%s|%.0f|%.0f|%.0f", classname, origin[0], origin[1], origin[2]);
            }
            
            AcceptEntityInput(entity, "Kill");
            PrintToServer("[Map Remover] Removed %s at %.0f %.0f %.0f", classname, origin[0], origin[1], origin[2]);
            removed++;
        }
    }
    
    // Close spawn file
    if (spawnFile != null) {
        spawnFile.Close();
        PrintToServer("[Map Remover] Saved spawn positions to file");
    }
    
    PrintToServer("[Map Remover] Removed %d items this pass", removed);
    return Plugin_Stop;
}

bool IsScavengeFinale() {
    char mapName[64];
    GetCurrentMap(mapName, sizeof(mapName));
    return (StrEqual(mapName, "c1m4_atrium") || StrEqual(mapName, "c6m3_port") || StrEqual(mapName, "c7m3_port"));
}

bool IsArchipelagoMutationActive() {
    ConVar mutationCvar = FindConVar("mp_gamemode");
    if (mutationCvar == null) return false;
    
    char gamemode[64];
    mutationCvar.GetString(gamemode, sizeof(gamemode));
    
    // Check if gamemode is directly set to archipelago
    return StrEqual(gamemode, "archipelago", false);
}