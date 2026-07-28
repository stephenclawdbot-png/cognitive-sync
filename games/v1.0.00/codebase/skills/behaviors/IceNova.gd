## IceNova.gd
extends SkillBehavior

func _execute_impl(player: Node) -> void:
	var dmg_mult: float = skill_data.get("damage_mult", 1.5)
	var radius: float = skill_data.get("radius", 120.0)
	var dmg := int(player.stats["damage"] * dmg_mult)
	# AoE damage to all enemies in radius
	var space := player.get_world_2d().direct_space_state
	var shape := CircleShape2D.new()
	shape.radius = radius
	var query := PhysicsShapeQueryParameters2D.new()
	query.shape = shape
	query.transform = Transform2D(0, player.global_position)
	var results := space.intersect_shape(query)
	for result in results:
		var collider = result.get("collider")
		if collider and collider.is_in_group("enemy"):
			collider.take_damage(dmg, "ice", false)
			collider.apply_status("slow", 2.0, 1)
			EventBus.enemy_damaged.emit(collider, dmg, false)
	# VFX
	var vfx := ObjectPool.spawn("VFX")
	if vfx and vfx.has_method("play_aoe"):
		vfx.global_position = player.global_position
		vfx.play_aoe(radius, Color.CYAN)
	EventBus.sfx_play_requested.emit("ice_nova")