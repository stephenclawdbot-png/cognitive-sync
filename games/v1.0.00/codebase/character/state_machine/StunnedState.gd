## StunnedState.gd
extends State

var stun_duration: float = 0.5
var timer: float = 0.0

func _enter(msg: Dictionary = {}) -> void:
	stun_duration = msg.get("duration", 0.5)
	timer = 0.0
	character.velocity = Vector2.ZERO
	character.anim_play("stunned")
	EventBus.sfx_play_requested.emit("stun")

func _physics_update(delta: float) -> void:
	timer += delta
	if timer >= stun_duration:
		transition_to("Idle")