## PlayerCharacter.gd
## Core player node — holds stats, components, and drives the state machine.
## Attach to CharacterBody2D with Sprite2D + AnimationPlayer + StateMachine child.
extends CharacterBody2D

# ── Core stats ──────────────────────────────────────────────────
@export var class_id: String = "dexterity_wizard"
@export var level: int = 1
@export var current_xp: int = 0
@export var gold: int = 0

var stats: Dictionary = {
	"max_health": 100, "current_health": 100,
	"max_mana": 50, "current_mana": 50,
	"damage": 10, "toughness": 5,
	"move_speed": 120.0, "crit_chance": 0.05, "crit_mult": 1.5,
	"dash_cooldown": 1.0, "special_cost": 15,
	"fire_res": 0, "ice_res": 0, "lightning_res": 0, "poison_res": 0
}
var facing_direction: Vector2 = Vector2(0, 1)
var mana_current: int = 50
var special_cost: int = 15
var skill_points: int = 0
var unlocked_skills: Array[String] = []

# ── Components (nodes added in scene tree) ──────────────────────
@onready var state_machine: Node = $StateMachine
@onready var sprite: Sprite2D = $Sprite2D
@onready var anim_player: AnimationPlayer = $AnimationPlayer
@onready var health_bar: ProgressBar = $HealthBar

func _ready() -> void:
	_load_class_data()
	_apply_class_stats()
	GameManager.player_node = self
	EventBus.player_level_up.connect(_on_level_up)
	EventBus.player_status_applied.connect(_on_status_applied)
	health_bar.value = 100

func _load_class_data() -> void:
	var data := DataManager.get_class_data(class_id)
	if data.is_empty():
		push_warning("[Player] Class '%s' not found in data" % class_id)
		return
	stats.merge(data.get("base_stats", {}), true)

func _apply_class_stats() -> void:
	mana_current = stats.get("max_mana", 50)
	stats["current_health"] = stats.get("max_health", 100)
	special_cost = stats.get("special_cost", 15)

func get_class_id() -> String:
	return class_id

func anim_play(anim_name: String) -> void:
	var full_name := "%s_%s" % [_dir_name(), anim_name]
	if anim_player.has_animation(full_name):
		anim_player.play(full_name)
	elif anim_player.has_animation(anim_name):
		anim_player.play(anim_name)

func _dir_name() -> String:
	var dirs := {
		Vector2(0, 1): "s", Vector2(1, 0): "e", Vector2(0, -1): "n", Vector2(-1, 0): "w",
		Vector2(1, 1): "se", Vector2(-1, 1): "sw", Vector2(1, -1): "ne", Vector2(-1, -1): "nw"
	}
	return dirs.get(facing_direction, "s")

# ── Damage intake ───────────────────────────────────────────────

func take_damage(amount: int, element: String = "physical") -> void:
	var res_key := element + "_res"
	var resistance := stats.get(res_key, 0) as int
	var effective_res := resistance / float(resistance + 50)
	var actual := int(amount * (1.0 - effective_res))
	stats["current_health"] = max(0, stats["current_health"] - actual)
	EventBus.player_health_changed.emit(stats["current_health"], stats["max_health"])
	EventBus.ui_show_damage_number.emit(global_position, actual, false)
	if stats["current_health"] <= 0:
		state_machine.transition_to("Death")
	else:
		# brief hit flash
		sprite.modulate = Color(1, 0.3, 0.3, 1)
		var t := get_tree().create_timer(0.1)
		t.timeout.connect(func(): sprite.modulate = Color.WHITE)

# ── Healing / Mana ───────────────────────────────────────────────

func heal(amount: int) -> void:
	stats["current_health"] = min(stats["max_health"], stats["current_health"] + amount)
	EventBus.player_health_changed.emit(stats["current_health"], stats["max_health"])

func spend_mana(amount: int) -> bool:
	if mana_current >= amount:
		mana_current -= amount
		EventBus.player_mana_changed.emit(mana_current, stats["max_mana"])
		return true
	return false

func regenerate_mana(amount: int) -> void:
	mana_current = min(stats["max_mana"], mana_current + amount)
	EventBus.player_mana_changed.emit(mana_current, stats["max_mana"])

# ── XP / Leveling ───────────────────────────────────────────────

func gain_xp(amount: int) -> void:
	current_xp += amount
	var needed := DataManager.xp_for_level(level)
	while current_xp >= needed:
		current_xp -= needed
		level += 1
		skill_points += 1
		EventBus.player_level_up.emit(level)
		EventBus.skill_point_awarded.emit(skill_points)
		needed = DataManager.xp_for_level(level)
	EventBus.player_xp_changed.emit(current_xp, needed)

func _on_level_up(new_level: int) -> void:
	# Increase max stats on level up
	stats["max_health"] += 10
	stats["max_mana"] += 5
	stats["damage"] += 2
	stats["current_health"] = stats["max_health"]
	mana_current = stats["max_mana"]
	EventBus.ui_show_notification.emit("Level Up!", "You are now level %d" % new_level)
	EventBus.sfx_play_requested.emit("level_up")

func _on_status_applied(status_id: String, stacks: int) -> void:
	EventBus.ui_show_floating_text.emit(global_position, status_id + " x" + str(stacks), Color.YELLOW)

# ── Skills ──────────────────────────────────────────────────────

func unlock_skill(skill_id: String) -> bool:
	if skill_points <= 0 or unlocked_skills.has(skill_id):
		return false
	var skill_data := DataManager.get_skill(skill_id)
	if skill_data.is_empty():
		return false
	# Check prerequisites
	var prereq := skill_data.get("prerequisite", "")
	if not prereq.is_empty() and not unlocked_skills.has(prereq):
		return false
	unlocked_skills.append(skill_id)
	skill_points -= 1
	EventBus.skill_unlocked.emit(skill_id)
	EventBus.skill_point_spent.emit(skill_id)
	return true