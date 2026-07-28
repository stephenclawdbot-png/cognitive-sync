## Fireball.gd
extends SkillBehavior

func _execute_impl(player: Node) -> void:
	var dmg_mult: float = skill_data.get("damage_mult", 2.0)
	var proj := ObjectPool.spawn("Projectile")
	if proj == null:
		return
	var dir: Vector2 = player.facing_direction
	proj.global_position = player.global_position + dir * 16
	proj.setup(dir, int(player.stats["damage"] * dmg_mult), player.get_class_id(), true)
	proj.element = "fire"
	proj.speed = 400.0
	EventBus.projectile_fired.emit(proj)
	EventBus.sfx_play_requested.emit("fireball")