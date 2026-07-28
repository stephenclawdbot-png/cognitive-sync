## ObjectPool.gd
## Generic object pool for projectiles, VFX, and item pickups.
## Pre-instantiates scenes and recycles them instead of freeing/creating.
extends Node

var pools: Dictionary = {}  # pool_name → { scene, active, inactive }

func _ready() -> void:
	_preload_pool("Projectile", preload("res://combat/Projectile.tscn"), 100)
	_preload_pool("VFX", preload("res://combat/VFX.tscn"), 50)
	_preload_pool("ItemPickup", preload("res://items/ItemPickup.tscn"), 30)
	_preload_pool("DamageNumber", preload("res://ui/DamageNumber.tscn"), 20)

func _preload_pool(pool_name: String, scene: PackedScene, count: int) -> void:
	pools[pool_name] = { "scene": scene, "inactive": [] }
	for i in count:
		var instance := scene.instantiate()
		instance.visible = false
		add_child(instance)
		pools[pool_name]["inactive"].append(instance)

func spawn(pool_name: String) -> Node:
	if not pools.has(pool_name):
		push_warning("[ObjectPool] Pool '%s' not found" % pool_name)
		return null
	var pool = pools[pool_name]
	if pool["inactive"].is_empty():
		# Pool exhausted — create one more
		var instance := pool["scene"].instantiate()
		add_child(instance)
		return instance
	var instance = pool["inactive"].pop_back()
	instance.visible = true
	return instance

func despawn(pool_name: String, instance: Node) -> void:
	if not pools.has(pool_name):
		instance.queue_free()
		return
	instance.visible = false
	if instance is CollisionObject2D:
		instance.monitoring = false
	pools[pool_name]["inactive"].append(instance)

func get_pool_size(pool_name: String) -> int:
	if not pools.has(pool_name):
		return 0
	return pools[pool_name]["inactive"].size()