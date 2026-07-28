## ItemPickup.gd
## Pickup-able item on the ground. Pooled. Detects player overlap and grants item.
extends Area2D

var item_id: String = ""
var quantity: int = 1
var rarity: String = "common"
var attract_range: float = 60.0
var pickup_range: float = 20.0
var magnet_speed: float = 200.0
var lifetime: float = 120.0  # items disappear after 2 min
var timer: float = 0.0
var attracted: bool = false

@onready var sprite: Sprite2D = $Sprite2D

func _ready() -> void:
	body_entered.connect(_on_body_entered)

func setup(id: String, qty: int, r: String = "common") -> void:
	item_id = id
	quantity = qty
	rarity = r
	timer = 0.0
	attracted = false
	visible = true
	monitoring = true
	# Load sprite based on item data
	var item_data := DataManager.get_item(item_id)
	if not item_data.is_empty():
		var sprite_path := item_data.get("icon", "")
		if not sprite_path.is_empty() and ResourceLoader.exists(sprite_path):
			sprite.texture = load(sprite_path)

func _physics_process(delta: float) -> void:
	timer += delta
	if timer >= lifetime:
		_deactivate()
		return
	var player = GameManager.player_node
	if player == null or not is_instance_valid(player):
		return
	var dist := global_position.distance_to(player.global_position)
	# Magnet effect
	if dist < attract_range:
		attracted = true
	if attracted:
		var dir := (player.global_position - global_position).normalized()
		velocity = dir * magnet_speed
		position += velocity * delta
	# Pickup
	if dist < pickup_range:
		_pickup(player)

func _pickup(player: Node) -> void:
	EventBus.item_picked_up.emit(item_id, quantity)
	EventBus.sfx_play_requested.emit("pickup")
	# Add to inventory (inventory system would be a component on player)
	player.gold += _get_gold_value()
	EventBus.gold_changed.emit(player.gold)
	_deactivate()

func _get_gold_value() -> int:
	var item_data := DataManager.get_item(item_id)
	var base_value: int = item_data.get("value", 5)
	var rarity_mult := LootTable.RARITY_MULTIPLIERS.get(rarity, 1.0)
	return int(base_value * rarity_mult * quantity)

func _on_body_entered(body: Node) -> void:
	if body.is_in_group("player"):
		_pickup(body)

func _deactivate() -> void:
	visible = false
	monitoring = false
	ObjectPool.despawn("ItemPickup", self)