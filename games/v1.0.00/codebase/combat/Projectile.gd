## Projectile.gd
## Projectile scene script — pooled, fires in a direction, damages enemies on hit.
extends Area2D

var direction: Vector2 = Vector2.ZERO
var speed: float = 300.0
var damage: int = 10
var owner_id: String = ""
var element: String = "physical"
var is_special: bool = false
var lifetime: float = 2.0
var timer: float = 0.0
var pierce: int = 0
var hit_enemies: Array[Node] = []

@onready var sprite: Sprite2D = $Sprite2D
@onready var collision: CollisionShape2D = $CollisionShape2D

func _ready() -> void:
	body_entered.connect(_on_body_entered)
	monitoring = true

func setup(dir: Vector2, dmg: int, owner: String, special: bool = false) -> void:
	direction = dir.normalized()
	damage = dmg
	owner_id = owner
	is_special = special
	timer = 0.0
	lifetime = 2.0 if not special else 3.0
	pierce = 1 if special else 0
	hit_enemies.clear()
	rotation = dir.angle()
	visible = true
	monitoring = true
	collision.disabled = false

func _physics_process(delta: float) -> void:
	position += direction * speed * delta
	timer += delta
	if timer >= lifetime:
		_deactivate()

func _on_body_entered(body: Node) -> void:
	if body.is_in_group("enemy") and not hit_enemies.has(body):
		hit_enemies.append(body)
		var is_crit := randf() < 0.1  # placeholder crit chance
		var result := DamageCalculator.calculate(
			{"damage": damage, "crit_chance": 0.1, "crit_mult": 1.5},
			body.stats,
			element, is_crit
		)
		body.take_damage(result["damage"], element, result["is_crit"])
		EventBus.enemy_damaged.emit(body, result["damage"], result["is_crit"])
		EventBus.ui_show_damage_number.emit(body.global_position, result["damage"], result["is_crit"])
		if pierce > 0:
			pierce -= 1
		else:
			_deactivate()

func _deactivate() -> void:
	visible = false
	monitoring = false
	collision.disabled = true
	ObjectPool.despawn("Projectile", self)