## SkillManager.gd
## Manages skill tree progression, activation, and cooldowns.
extends Node

var unlocked_skills: Dictionary = {}  # skill_id → { level, cooldown_timer }
var active_skills: Array[String] = []
var skill_points: int = 0

func _ready() -> void:
	EventBus.skill_unlocked.connect(_on_skill_unlocked)
	EventBus.skill_activated.connect(_on_skill_activated)
	EventBus.skill_point_awarded.connect(_on_skill_points_awarded)

func _process(delta: float) -> void:
	# Tick cooldowns
	for skill_id in unlocked_skills:
		var cd: float = unlocked_skills[skill_id].get("cooldown_timer", 0.0)
		if cd > 0:
			unlocked_skills[skill_id]["cooldown_timer"] = max(0, cd - delta)
			if unlocked_skills[skill_id]["cooldown_timer"] == 0:
				EventBus.skill_cooldown_finished.emit(skill_id)

func unlock_skill(skill_id: String) -> bool:
	if skill_points <= 0:
		return false
	var skill_data := DataManager.get_skill(skill_id)
	if skill_data.is_empty():
		return false
	# Check prerequisite
	var prereq := skill_data.get("prerequisite", "")
	if not prereq.is_empty() and not unlocked_skills.has(prereq):
		return false
	# Check if already maxed
	var current_level := unlocked_skills.get(skill_id, {}).get("level", 0)
	var max_level: int = skill_data.get("max_level", 1)
	if current_level >= max_level:
		return false
	# Unlock
	if not unlocked_skills.has(skill_id):
		unlocked_skills[skill_id] = { "level": 0, "cooldown_timer": 0.0 }
	unlocked_skills[skill_id]["level"] += 1
	skill_points -= 1
	EventBus.skill_unlocked.emit(skill_id)
	return true

func activate_skill(skill_id: String) -> bool:
	if not unlocked_skills.has(skill_id):
		return false
	var cd: float = unlocked_skills[skill_id].get("cooldown_timer", 0.0)
	if cd > 0:
		return false
	var skill_data := DataManager.get_skill(skill_id)
	if skill_data.is_empty():
		return false
	# Execute skill behavior
	var behavior_id := skill_data.get("behavior", "melee_strike")
	var behavior := _get_behavior(behavior_id)
	if behavior:
		behavior.execute(GameManager.player_node, skill_data)
	# Start cooldown
	var cooldown: float = skill_data.get("cooldown", 1.0)
	unlocked_skills[skill_id]["cooldown_timer"] = cooldown
	EventBus.skill_cooldown_started.emit(skill_id, cooldown)
	EventBus.skill_activated.emit(skill_id)
	return true

func _get_behavior(behavior_id: String) -> Node:
	var path := "res://skills/behaviors/" + behavior_id + ".gd"
	if ResourceLoader.exists(path):
		return load(path).new()
	return null

func _on_skill_unlocked(skill_id: String) -> void:
	print("[SkillManager] Unlocked: %s" % skill_id)

func _on_skill_activated(skill_id: String) -> void:
	print("[SkillManager] Activated: %s" % skill_id)

func _on_skill_points_awarded(total: int) -> void:
	skill_points = total

func get_skill_info(skill_id: String) -> Dictionary:
	var data := DataManager.get_skill(skill_id)
	var level := unlocked_skills.get(skill_id, {}).get("level", 0)
	var cd := unlocked_skills.get(skill_id, {}).get("cooldown_timer", 0.0)
	return {
		"name": data.get("name", skill_id),
		"description": data.get("description", ""),
		"level": level,
		"max_level": data.get("max_level", 1),
		"cooldown": data.get("cooldown", 1.0),
		"current_cooldown": cd,
		"unlocked": unlocked_skills.has(skill_id),
		"prerequisite": data.get("prerequisite", ""),
		"behavior": data.get("behavior", "melee_strike"),
		"icon": data.get("icon", "")
	}