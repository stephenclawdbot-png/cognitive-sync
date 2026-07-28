## AttackState.gd
extends State

var attack_type: String = "basic"
var attack_duration: float = 0.25
var attack_timer: float = 0.0

func _enter(msg: Dictionary = {}) -> void:
	attack_type = msg.get("attack_type", "basic")
	attack_timer = attack_duration
	character.velocity = Vector2.ZERO
	if attack_type == "basic":
		character.anim_play("attack_basic")
		_fire_projectile()
	elif attack_type == "special":
		if character.mana_current >= character.special_cost:
			character.mana_current -= character.special_cost
			character.anim_play("attack_special")
			_fire_special()
		else:
			EventBus.ui_show_floating_text.emit(character.global_position, "No Mana!", Color.RED)
			transition_to("Idle")
			return
	EventBus.sfx_play_requested.emit("attack_" + attack_type)

func _physics_update(delta: float) -> void:
	attack_timer -= delta
	if attack_timer <= 0:
		transition_to("Idle")

func _fire_projectile() -> void:
	var proj := ObjectPool.spawn("Projectile")
	if proj == null:
		return
	var dir := character.facing_direction
	proj.global_position = character.global_position + dir * 12
	proj.setup(dir, character.stats.damage, character.get_class_id())
	EventBus.projectile_fired.emit(proj)

func _fire_special() -> void:
	# Special skill logic — overridden by class-specific skill behaviors
	var proj := ObjectPool.spawn("Projectile")
	if proj == null:
		return
	var dir := character.facing_direction
	proj.global_position = character.global_position + dir * 12
	proj.setup(dir, character.stats.damage * 2.5, character.get_class_id(), true)
	EventBus.projectile_fired.emit(proj)