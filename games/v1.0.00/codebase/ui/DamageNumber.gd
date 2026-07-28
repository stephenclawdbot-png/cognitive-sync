## DamageNumber.gd
## Floating damage number — pooled, rises and fades.
extends Label

var velocity: Vector2 = Vector2.ZERO
var lifetime: float = 0.8
var timer: float = 0.0
var is_crit: bool = false

func _ready() -> void:
	visible = false

func setup(amount: int, crit: bool) -> void:
	text = str(amount) if not crit else str(amount) + "!"
	is_crit = crit
	modulate = Color.RED if crit else Color.WHITE
	scale = Vector2(1.5, 1.5) if crit else Vector2(1, 1)
	timer = 0.0
	velocity = Vector2(randf_range(-20, 20), -40)
	visible = true

func _process(delta: float) -> void:
	if not visible:
		return
	timer += delta
	position += velocity * delta
	velocity.y += 60 * delta  # slight gravity
	modulate.a = 1.0 - (timer / lifetime)
	if timer >= lifetime:
		visible = false
		ObjectPool.despawn("DamageNumber", self)