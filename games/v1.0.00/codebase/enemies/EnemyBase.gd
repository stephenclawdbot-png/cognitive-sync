## EnemyBase.gd
## Base class for all enemies. Extend for specific enemy types or configure via data.
extends CharacterBody2D

@export var enemy_id: String = "slime"
@export var enemy_level: int = 1

var stats: Dictionary = {
	"max_health": 20, "current_health": 20,
	"damage": 5, "toughness": 2,
	"speed": 60.0, "xp_reward": 8, "gold_reward": 3,
	"fire_res": 0, "ice_res": 0, "lightning_res": 0, "poison_res": 0
}
var ai_state: String = "idle"
var target: Node = null
var attack_cooldown: float = 1.0
var attack_timer: float = 0.0
var detection_range: float = 200.0
var attack_range: float = 40.0
var is_boss: bool = false
var status_effects: Dictionary = {}  # effect_id → { stacks, duration }
var spawn_position: Vector2 = Vector2.ZERO
var wander_target: Vector2 = Vector2.ZERO
var wander_timer: float = 0.0

@onready var sprite: Sprite2D = $Sprite2D
@onready var health_bar: ProgressBar = $HealthBar

func _ready() -> void:
	add_to_group("enemy")
	_load_data()
	_apply_scaling()
	health_bar.visible = false
	spawn_position = global_position
	EventBus.enemy_spawned.emit(self)

func _load_data() -> void:
	var data := DataManager.get_enemy(enemy_id)
	if data.is_empty():
		return
	stats.merge(data.get("base_stats", {}), true)
	detection_range = data.get("detection_range", 200.0)
	attack_range = data.get("attack_range", 40.0)
	attack_cooldown = data.get("attack_cooldown", 1.0)
	is_boss = data.get("is_boss", false)

func _apply_scaling() -> void:
	var base := stats.duplicate()
	var scaled := DataManager.scale_enemy(base, enemy_level)
	stats.merge(scaled, true)
	stats["current_health"] = stats["max_health"]

func _physics_process(delta: float) -> void:
	_update_status_effects(delta)
	match ai_state:
		"idle": _ai_idle(delta)
		"chase": _ai_chase(delta)
		"attack": _ai_attack(delta)
		"wander": _ai_wander(delta)

func _ai_idle(delta: float) -> void:
	var dist := global_position.distance_to(GameManager.player_node.global_position if GameManager.player_node else Vector2.ZERO)
	if dist < detection_range:
		ai_state = "chase"
		health_bar.visible = true
		return
	# Occasionally wander
	wander_timer -= delta
	if wander_timer <= 0:
		wander_timer = randf_range(2.0, 5.0)
		wander_target = spawn_position + Vector2(randf_range(-80, 80), randf_range(-80, 80))
		ai_state = "wander"

func _ai_wander(delta: float) -> void:
	var dir := (wander_target - global_position).normalized()
	velocity = dir * stats["speed"] * 0.3
	move_and_slide()
	if global_position.distance_to(wander_target) < 10 or wander_timer <= 0:
		velocity = Vector2.ZERO
		ai_state = "idle"
	var dist := global_position.distance_to(GameManager.player_node.global_position if GameManager.player_node else Vector2.ZERO)
	if dist < detection_range:
		ai_state = "chase"
		health_bar.visible = true

func _ai_chase(delta: float) -> void:
	if GameManager.player_node == null:
		ai_state = "idle"
		return
	var player_pos := GameManager.player_node.global_position
	var dist := global_position.distance_to(player_pos)
	if dist > detection_range * 1.5:
		ai_state = "idle"
		health_bar.visible = false
		return
	if dist < attack_range:
		ai_state = "attack"
		return
	var dir := (player_pos - global_position).normalized()
	velocity = dir * stats["speed"]
	move_and_slide()

func _ai_attack(delta: float) -> void:
	velocity = Vector2.ZERO
	if GameManager.player_node == null:
		ai_state = "idle"
		return
	var dist := global_position.distance_to(GameManager.player_node.global_position)
	if dist > attack_range:
		ai_state = "chase"
		return
	attack_timer -= delta
	if attack_timer <= 0:
		attack_timer = attack_cooldown
		_perform_attack()

func _perform_attack() -> void:
	# Base: melee attack. Override for ranged enemies.
	var player = GameManager.player_node
	if player and is_instance_valid(player):
		var element := "physical"
		var dmg := DamageCalculator.calculate_enemy_damage(stats, player.stats, element)
		player.take_damage(dmg, element)
	# Attack animation trigger would go here
	EventBus.sfx_play_requested.emit("enemy_attack")

func take_damage(amount: int, element: String = "physical", is_crit: bool = false) -> void:
	stats["current_health"] = max(0, stats["current_health"] - amount)
	health_bar.value = float(stats["current_health"]) / float(stats["max_health"]) * 100
	# Hit flash
	sprite.modulate = Color(1, 0.3, 0.3, 1)
	var t := get_tree().create_timer(0.1)
	t.timeout.connect(func(): sprite.modulate = Color.WHITE)
	if stats["current_health"] <= 0:
		die()

func die() -> void:
	EventBus.enemy_died.emit(self, stats["xp_reward"], stats["gold_reward"])
	# Drop loot
	_drop_loot()
	# Death VFX
	var vfx := ObjectPool.spawn("VFX")
	if vfx and vfx.has_method("play_death"):
		vfx.global_position = global_position
		vfx.play_death()
	EventBus.sfx_play_requested.emit("enemy_death")
	queue_free()

func _drop_loot() -> void:
	var drop_table := DataManager.get_loot_table(enemy_id)
	if drop_table.is_empty():
		drop_table = DataManager.get_loot_table("default_enemy")
	if drop_table.is_empty():
		return
	var roll := randf()
	var cumulative := 0.0
	for entry in drop_table.get("drops", []):
		cumulative += entry.get("chance", 0.0)
		if roll < cumulative:
			var item_id := entry.get("item_id", "")
			var qty := entry.get("quantity", 1)
			var pickup := ObjectPool.spawn("ItemPickup")
			if pickup:
				pickup.global_position = global_position + Vector2(randf_range(-10, 10), randf_range(-10, 10))
				pickup.setup(item_id, qty)
			break

func apply_status(effect_id: String, duration: float, stacks: int = 1) -> void:
	status_effects[effect_id] = { "duration": duration, "stacks": stacks }

func _update_status_effects(delta: float) -> void:
	var expired := []
	for effect_id in status_effects:
		status_effects[effect_id]["duration"] -= delta
		_apply_status_tick(effect_id, delta)
		if status_effects[effect_id]["duration"] <= 0:
			expired.append(effect_id)
	for e in expired:
		status_effects.erase(e)

func _apply_status_tick(effect_id: String, _delta: float) -> void:
	match effect_id:
		"poison":
			take_damage(1, "poison", false)
		"fire":
			take_damage(2, "fire", false)
		"slow":
			stats["speed"] = stats.get("base_speed", 60.0) * 0.5
		"stun":
			velocity = Vector2.ZERO