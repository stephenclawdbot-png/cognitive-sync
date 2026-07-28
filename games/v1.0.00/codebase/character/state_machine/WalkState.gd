## WalkState.gd
extends State

func _enter(_msg: Dictionary = {}) -> void:
	character.anim_play("walk")

func _physics_update(delta: float) -> void:
	var input_vector := Input.get_vector("move_left", "move_right", "move_up", "move_down")
	if input_vector == Vector2.ZERO:
		transition_to("Idle")
		return

	# 8-directional facing
	character.facing_direction = _get_8dir(input_vector)
	character.velocity = input_vector.normalized() * character.stats.move_speed
	character.move_and_slide()

	if Input.is_action_just_pressed("basic_attack"):
		transition_to("Attack", {"attack_type": "basic"})
	elif Input.is_action_just_pressed("special_attack"):
		transition_to("Attack", {"attack_type": "special"})
	elif Input.is_action_just_pressed("dash"):
		transition_to("Dash")

func _get_8dir(v: Vector2) -> Vector2:
	var angle := v.angle()
	var directions := [
		Vector2(0, 1),    # south
		Vector2(1, 0),    # east
		Vector2(0, -1),   # north
		Vector2(-1, 0),   # west
		Vector2(1, 1).normalized(),   # south-east
		Vector2(-1, 1).normalized(),  # south-west
		Vector2(1, -1).normalized(),  # north-east
		Vector2(-1, -1).normalized()   # north-west
	]
	var best := directions[0]
	var best_dot := -2.0
	for d in directions:
		var dot := v.normalized().dot(d)
		if dot > best_dot:
			best_dot = dot
			best = d
	return best