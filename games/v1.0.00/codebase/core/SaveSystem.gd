## SaveSystem.gd
## JSON-based save system. Auto-saves on room clear, boss kill, level up, and 60s timer.
extends Node

const SAVE_DIR := "user://saves/"
const SAVE_FILE := "slot_%d.json"
const AUTOSAVE_INTERVAL := 60.0

var _autosave_timer: float = 0.0

func _ready() -> void:
	DirAccess.make_dir_recursive_absolute(SAVE_DIR)
	EventBus.room_cleared.connect(_on_room_cleared)
	EventBus.boss_defeated.connect(_on_boss_defeated)
	EventBus.player_level_up.connect(_on_level_up)
	EventBus.game_saved.connect(_on_save_requested)

func _process(delta: float) -> void:
	_autosave_timer += delta
	if _autosave_timer >= AUTOSAVE_INTERVAL:
		_autosave_timer = 0.0
		_save_slot(0)  # autosave to slot 0

func _on_room_cleared(_room_id: String) -> void:
	_save_slot(0)

func _on_boss_defeated(_boss_id: String) -> void:
	_save_slot(0)

func _on_level_up(_new_level: int) -> void:
	_save_slot(0)

func _on_save_requested(slot: int) -> void:
	_save_slot(slot)

func _save_slot(slot: int) -> void:
	var player = GameManager.player_node
	if player == null:
		return
	var save_data := {
		"version": "1.0.00",
		"timestamp": Time.get_unix_time_from_system(),
		"player": {
			"class_id": player.class_id,
			"level": player.level,
			"current_xp": player.current_xp,
			"gold": player.gold,
			"stats": player.stats,
			"mana_current": player.mana_current,
			"skill_points": player.skill_points,
			"unlocked_skills": player.unlocked_skills,
			"facing_direction": [player.facing_direction.x, player.facing_direction.y]
		},
		"game": {
			"current_floor": GameManager.current_floor,
			"rooms_cleared": GameManager.rooms_cleared,
			"total_kills": GameManager.total_kills,
			"total_gold": GameManager.total_gold,
			"run_time": GameManager.run_time,
			"run_seed": GameManager.run_seed
		}
	}
	var path := SAVE_DIR + (SAVE_FILE % slot)
	var file := FileAccess.open(path, FileAccess.WRITE)
	if file == null:
		push_error("[SaveSystem] Failed to write save file: %s" % path)
		return
	file.store_string(JSON.stringify(save_data, "\t"))
	file.close()
	print("[SaveSystem] Saved to slot %d" % slot)

func load_slot(slot: int) -> Dictionary:
	var path := SAVE_DIR + (SAVE_FILE % slot)
	if not FileAccess.file_exists(path):
		return {}
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return {}
	var data = JSON.parse_string(file.get_as_text())
	file.close()
	return data if data is Dictionary else {}

func has_save(slot: int) -> bool:
	return FileAccess.file_exists(SAVE_DIR + (SAVE_FILE % slot))

func delete_slot(slot: int) -> void:
	var path := SAVE_DIR + (SAVE_FILE % slot)
	if FileAccess.file_exists(path):
		DirAccess.remove_absolute(path)