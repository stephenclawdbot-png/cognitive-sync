## DataManager.gd
## Loads all JSON data files at startup and provides lookup access.
## All game data (items, skills, enemies, curves, rooms, npcs) lives in /data/*.json
extends Node

# ── Data dictionaries ────────────────────────────────────────────
var items: Dictionary = {}
var skills: Dictionary = {}
var enemies: Dictionary = {}
var enemy_groups: Dictionary = {}
var curves: Dictionary = {}
var room_sets: Dictionary = {}
var npcs: Dictionary = {}
var dialogues: Dictionary = {}
var equipment: Dictionary = {}
var loot_tables: Dictionary = {}
var status_effects: Dictionary = {}
var class_data: Dictionary = {}
var dungeon_config: Dictionary = {}

const DATA_DIR := "res://data/"

func _ready() -> void:
	_load_all_data()

func _load_all_data() -> void:
	items          = _load_json("items.json")
	skills         = _load_json("skills.json")
	enemies        = _load_json("enemies.json")
	enemy_groups  = _load_json("enemy_groups.json")
	curves         = _load_json("curves.json")
	room_sets      = _load_json("room_sets.json")
	npcs           = _load_json("npcs.json")
	dialogues      = _load_json("dialogues.json")
	equipment      = _load_json("equipment.json")
	loot_tables    = _load_json("loot_tables.json")
	status_effects = _load_json("status_effects.json")
	class_data     = _load_json("classes.json")
	dungeon_config = _load_json("dungeon_config.json")
	print("[DataManager] All data loaded — %d items, %d skills, %d enemies" % [items.size(), skills.size(), enemies.size()])

func _load_json(filename: String) -> Dictionary:
	var path := DATA_DIR + filename
	if not FileAccess.file_exists(path):
		push_warning("[DataManager] Missing data file: %s" % path)
		return {}
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		push_error("[DataManager] Failed to open: %s" % path)
		return {}
	var parsed = JSON.parse_string(file.get_as_text())
	file.close()
	return parsed if parsed is Dictionary else {}

# ── Public lookup API ───────────────────────────────────────────

func get_item(item_id: String) -> Dictionary:
	return items.get(item_id, {})

func get_skill(skill_id: String) -> Dictionary:
	return skills.get(skill_id, {})

func get_enemy(enemy_id: String) -> Dictionary:
	return enemies.get(enemy_id, {})

func get_curve(curve_id: String) -> Dictionary:
	return curves.get(curve_id, {})

func get_npc(npc_id: String) -> Dictionary:
	return npcs.get(npc_id, {})

func get_equipment(slot: String) -> Dictionary:
	return equipment.get(slot, {})

func get_loot_table(table_id: String) -> Dictionary:
	return loot_tables.get(table_id, {})

func get_status_effect(effect_id: String) -> Dictionary:
	return status_effects.get(effect_id, {})

func get_class_data(class_id: String) -> Dictionary:
	return class_data.get(class_id, {})

func get_dungeon_config() -> Dictionary:
	return dungeon_config

func get_room_set(set_id: String) -> Dictionary:
	return room_sets.get(set_id, {})

func get_enemy_group(group_id: String) -> Dictionary:
	return enemy_groups.get(group_id, {})

# ── XP / Leveling ────────────────────────────────────────────────

func xp_for_level(level: int) -> int:
	## XP needed to go from `level` to `level + 1`
	## Formula: floor(100 * 1.5^(level - 1))
	return int(100 * pow(1.5, level - 1))

func level_from_xp(total_xp: int) -> Dictionary:
	## Given cumulative XP, returns { level, current_xp, needed_xp, progress }
	var level := 1
	var remaining := total_xp
	while remaining >= xp_for_level(level):
		remaining -= xp_for_level(level)
		level += 1
	return {
		"level": level,
		"current_xp": remaining,
		"needed_xp": xp_for_level(level),
		"progress": float(remaining) / float(xp_for_level(level))
	}

# ── Enemy scaling ───────────────────────────────────────────────

func scale_enemy(base_stats: Dictionary, level: int) -> Dictionary:
	## Scales base enemy stats to given level using curves from data
	var scalar_life := 1.15
	var scalar_dmg := 1.10
	var scalar_tgh := 1.08
	if curves.has("enemy_scaling"):
		var sc = curves["enemy_scaling"]
		scalar_life = sc.get("life_scalar", scalar_life)
		scalar_dmg = sc.get("damage_scalar", scalar_dmg)
		scalar_tgh = sc.get("toughness_scalar", scalar_tgh)
	return {
		"max_health": int(base_stats.get("max_health", 10) * pow(scalar_life, level - 1)),
		"damage": int(base_stats.get("damage", 3) * pow(scalar_dmg, level - 1)),
		"toughness": int(base_stats.get("toughness", 0) * pow(scalar_tgh, level - 1)),
		"speed": base_stats.get("speed", 60.0),
		"xp_reward": int(base_stats.get("xp_reward", 5) * pow(1.12, level - 1)),
		"gold_reward": int(base_stats.get("gold_reward", 2) * pow(1.10, level - 1))
	}