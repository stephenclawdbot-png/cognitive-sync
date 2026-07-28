## MeleeStrike.gd
extends SkillBehavior

func _execute_impl(player: Node) -> void:
	# Fire a projectile in facing direction with skill damage multiplier
	var dmg_mult: float = skill_data.get("damage_mult", 1.5)
	var element: String = skill_data.get("element", "physical")
	var proj := ObjectPool.spawn("Projectile")
	if proj == null:
		return
	var dir: Vector2 = player.facing_direction
	proj.global_position = player.global_position + dir * 12
	proj.setup(dir, int(player.stats["damage"] * dmg_mult), player.get_class_id())
	proj.element = element
	EventBus.projectile_fired.emit(proj)