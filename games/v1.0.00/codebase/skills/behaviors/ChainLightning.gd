## ChainLightning.gd
extends SkillBehavior

func _execute_impl(player: Node) -> void:
	var dmg_mult: float = skill_data.get("damage_mult", 1.8)
	var chain_count: int = skill_data.get("chain_count", 3)
	var dmg := int(player.stats["damage"] * dmg_mult)
	# Find nearest enemy, then chain to next nearest
	var hit: Array[Node] = []
	var current_pos: Vector2 = player.global_position
	for i in chain_count:
		var nearest := _find_nearest_enemy(current_pos, hit)
		if nearest == null:
			break
		nearest.take_damage(dmg * pow(0.7, i), "lightning", false)
		nearest.apply_status("stun", 0.3, 1)
		EventBus.enemy_damaged.emit(nearest, int(dmg * pow(0.7, i)), false)
		EventBus.ui_show_floating_text.emit(nearest.global_position, "⚡", Color.YELLOW)
		hit.append(nearest)
		current_pos = nearest.global_position
	EventBus.sfx_play_requested.emit("chain_lightning")

func _find_nearest_enemy(from: Vector2, exclude: Array[Node]) -> Node:
	var enemies := get_tree().get_nodes_in_group("enemy")
	var nearest: Node = null
	var min_dist := 300.0  # max chain range
	for enemy in enemies:
		if exclude.has(enemy) or not is_instance_valid(enemy):
			continue
		var dist := from.distance_to(enemy.global_position)
		if dist < min_dist:
			min_dist = dist
			nearest = enemy
	return nearest