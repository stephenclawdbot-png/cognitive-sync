## DashState.gd
extends State

var dash_speed: float = 480.0
var dash_duration: float = 0.15
var dash_timer: float = 0.0
var dash_direction: Vector2 = Vector2.ZERO
var invulnerable: bool = true

func _enter(_msg: Dictionary = {}) -> void:
	dash_timer = dash_duration
	dash_direction = character.facing_direction
	character.velocity = dash_direction * dash_speed
	EventBus.player_dash_state.emit(true)
	EventBus.sfx_play_requested.emit("dash")
	invulnerable = true
	character.set_collision_mask_value(2, false)  # disable hurtbox

func _physics_update(delta: float) -> void:
	dash_timer -= delta
	character.velocity = dash_direction * dash_speed * (dash_timer / dash_duration)
	character.move_and_slide()
	if dash_timer <= 0:
		transition_to("Idle")

func _exit() -> void:
	EventBus.player_dash_state.emit(false)
	invulnerable = false
	character.set_collision_mask_value(2, true)  # re-enable hurtbox