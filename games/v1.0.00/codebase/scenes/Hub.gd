## Hub.gd
## Hub area scene — safe zone with NPCs, shop, skill tree, portal to dungeon.
extends Node2D

@onready var player: CharacterBody2D = $Player
@onready var hud: CanvasLayer = $HUD

func _ready() -> void:
	EventBus.music_play_requested.emit("hub")
	# Spawn NPCs based on data
	_spawn_npcs()
	# Place player at entrance
	if GameManager.player_node:
		GameManager.player_node.global_position = Vector2(320, 180)

func _spawn_npcs() -> void:
	var npc_data := DataManager.npcs
	for npc_id in npc_data:
		var data: Dictionary = npc_data[npc_id]
		var npc_scene := load("res://npc/NPCBase.tscn")
		if npc_scene:
			var npc := npc_scene.instantiate()
			npc.npc_id = npc_id
			npc.npc_name = data.get("name", npc_id)
			npc.global_position = Vector2(
				data.get("x", 320),
				data.get("y", 180)
			)
			add_child(npc)