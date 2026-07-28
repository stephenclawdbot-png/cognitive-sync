## LootTable.gd
## Handles loot rolling with rarity tiers and luck modifiers.
class_name LootTable

# Rarity tiers and their base weights
const RARITY_WEIGHTS := {
	"common": 100.0,
	"uncommon": 35.0,
	"rare": 10.0,
	"epic": 3.0,
	"legendary": 0.5
}

const RARITY_MULTIPLIERS := {
	"common": 1.0,
	"uncommon": 1.3,
	"rare": 1.6,
	"epic": 2.0,
	"legendary": 3.0
}

static func roll_loot(table_id: String, luck: float = 0.0, level: int = 1) -> Dictionary:
	var table := DataManager.get_loot_table(table_id)
	if table.is_empty():
		return {}
	# Apply luck to rarity weights
	var weights := RARITY_WEIGHTS.duplicate()
	for rarity in weights:
		weights[rarity] *= (1.0 + luck * 0.01)
	# Pick rarity
	var total_weight := 0.0
	for w in weights.values():
		total_weight += w
	var roll := randf() * total_weight
	var cumulative := 0.0
	var selected_rarity := "common"
	for rarity in weights:
		cumulative += weights[rarity]
		if roll < cumulative:
			selected_rarity = rarity
			break
	# Filter items by rarity
	var pool: Array = table.get("items", [])
	var candidates := pool.filter(func(item): return item.get("rarity", "common") == selected_rarity)
	if candidates.is_empty():
		candidates = pool.filter(func(item): return item.get("rarity", "common") == "common")
	if candidates.is_empty():
		return {}
	# Pick random item
	var chosen := candidates[randi() % candidates.size()]
	var item_id := chosen.get("item_id", "")
	var quantity := chosen.get("quantity", 1)
	var mult := RARITY_MULTIPLIERS.get(selected_rarity, 1.0)
	return {
		"item_id": item_id,
		"quantity": quantity,
		"rarity": selected_rarity,
		"value_mult": mult,
		"level": level
	}

static func roll_gold(base: int, level: int, luck: float = 0.0) -> int:
	var mult := 1.0 + luck * 0.01
	var variance := randf_range(0.8, 1.2)
	return int(base * pow(1.1, level - 1) * mult * variance)

static func roll_drop(chance: float, luck: float = 0.0) -> bool:
	return randf() < chance * (1.0 + luck * 0.01)