## DeathState.gd
extends State

var death_timer: float = 1.5
var timer: float = 0.0

func _enter(_msg: Dictionary = {}) -> void:
	character.velocity = Vector2.ZERO
	character.anim_play("death")
	EventBus.sfx_play_requested.emit("player_death")
	EventBus.player_died.emit()

func _physics_update(delta: float) -> void:
	timer += delta
	if timer >= death_timer:
		GameManager.end_run()