## IdleState.gd
extends State

func _enter(_msg: Dictionary = {}) -> void:
	character.anim_play("idle")

func _physics_update(_delta: float) -> void:
	var input_vector := Input.get_vector("move_left", "move_right", "move_up", "move_down")
	if input_vector != Vector2.ZERO:
		transition_to("Walk")
		return

	if Input.is_action_just_pressed("basic_attack"):
		transition_to("Attack", {"attack_type": "basic"})
	elif Input.is_action_just_pressed("special_attack"):
		transition_to("Attack", {"attack_type": "special"})
	elif Input.is_action_just_pressed("dash"):
		transition_to("Dash")
	elif Input.is_action_just_pressed("interact"):
		EventBus.sfx_play_requested.emit("interact")