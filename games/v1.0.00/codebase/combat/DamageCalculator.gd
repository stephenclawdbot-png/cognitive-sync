## DamageCalculator.gd
## Static utility class for all damage calculations.
class_name DamageCalculator

## Full damage formula:
##   raw = (base + elemental) * dmg_mult * crit_mult
##   mitigated = raw - toughness
##   resisted = mitigated * (1 - effective_res)
##   damage = max(1, resisted)
##
## effective_res = resistance / (resistance + 50)  [diminishing returns]

static func calculate(attacker_stats: Dictionary, defender_stats: Dictionary, element: String = "physical", is_crit: bool = false) -> Dictionary:
	var base_dmg: int = attacker_stats.get("damage", 10)
	var dmg_mult: float = attacker_stats.get("dmg_mult", 1.0)
	var crit_chance: float = attacker_stats.get("crit_chance", 0.05)
	var crit_mult: float = attacker_stats.get("crit_mult", 1.5)

	# Crit roll (if not forced)
	if not is_crit:
		is_crit = randf() < crit_chance

	var crit_multiplier: float = crit_mult if is_crit else 1.0

	# Raw damage
	var raw := (base_dmg) * dmg_mult * crit_multiplier

	# Toughness mitigation (flat reduction)
	var toughness: int = defender_stats.get("toughness", 0)
	var after_toughness := max(1.0, raw - toughness)

	# Elemental resistance (diminishing returns)
	var res_key := element + "_res"
	var resistance: int = defender_stats.get(res_key, 0)
	var effective_res := resistance / float(resistance + 50)
	var final_damage := int(after_toughness * (1.0 - effective_res))
	final_damage = max(1, final_damage)

	return {
		"damage": final_damage,
		"is_crit": is_crit,
		"element": element,
		"raw": int(raw),
		"mitigated": int(raw) - final_damage
	}

static func calculate_player_damage(player_stats: Dictionary, enemy_stats: Dictionary, element: String = "physical") -> int:
	var result := calculate(player_stats, enemy_stats, element, false)
	return result["damage"]

static func calculate_enemy_damage(enemy_stats: Dictionary, player_stats: Dictionary, element: String = "physical") -> int:
	var result := calculate(enemy_stats, player_stats, element, false)
	return result["damage"]