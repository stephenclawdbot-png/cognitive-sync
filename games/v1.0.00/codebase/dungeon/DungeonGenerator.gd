## DungeonGenerator.gd
## Procedural dungeon generator. Creates floor layouts, spawns rooms, enemies, and loot.
extends Node2D

const ROOM_SIZE := 320  # 10 tiles × 32px
const GRID_W := 5
const GRID_H := 5

var floor_grid: Array = []
var room_scenes: Dictionary = {}
var current_floor: int = 1
var rooms_visited: Dictionary = {}
var start_pos: Vector2i = Vector2i.ZERO
var boss_pos: Vector2i = Vector2i.ZERO
var portal_node: Node = null

func _ready() -> void:
	EventBus.dungeon_floor_loaded.connect(_on_floor_loaded)
	EventBus.room_cleared.connect(_on_room_cleared)

func generate_floor(floor_num: int) -> void:
	current_floor = floor_num
	floor_grid.clear()
	rooms_visited.clear()
	# Initialize grid
	for x in GRID_W:
		floor_grid.append([])
		for y in GRID_H:
			floor_grid[x].append(null)
	# 1. Generate layout using random walk + branch algorithm
	_layout_floor()
	# 2. Assign room types (start, combat, treasure, boss)
	_assign_room_types()
	# 3. Instantiate room scenes
	_instantiate_rooms()
	# 4. Place player in start room
	_place_player()
	EventBus.dungeon_floor_loaded.emit(floor_num)
	print("[DungeonGen] Floor %d generated — %d rooms" % [floor_num, _count_rooms()])

func _layout_floor() -> void:
	# Random walk from center
	start_pos = Vector2i(GRID_W / 2, GRID_H / 2)
	floor_grid[start_pos.x][start_pos.y] = { "type": "start", "visited": false }
	var current := start_pos
	var room_count := 4 + current_floor  # more rooms on deeper floors
	var directions := [Vector2i(1, 0), Vector2i(-1, 0), Vector2i(0, 1), Vector2i(0, -1)]
	for i in room_count:
		var dir := directions[randi() % directions.size()]
		var next := current + dir
		if _in_bounds(next) and floor_grid[next.x][next.y] == null:
			floor_grid[next.x][next.y] = { "type": "combat", "visited": false }
			current = next
	# Place boss room farthest from start
	var farthest := start_pos
	var max_dist := 0
	for x in GRID_W:
		for y in GRID_H:
			if floor_grid[x][y] != null and floor_grid[x][y]["type"] == "combat":
				var dist := absi(x - start_pos.x) + absi(y - start_pos.y)
				if dist > max_dist:
					max_dist = dist
					farthest = Vector2i(x, y)
	boss_pos = farthest
	floor_grid[farthest.x][farthest.y]["type"] = "boss"

func _assign_room_types() -> void:
	# Convert some combat rooms to treasure/shop rooms
	for x in GRID_W:
		for y in GRID_H:
			if floor_grid[x][y] != null and floor_grid[x][y]["type"] == "combat":
				if randf() < 0.15:
					floor_grid[x][y]["type"] = "treasure"
				elif randf() < 0.10:
					floor_grid[x][y]["type"] = "shop"

func _in_bounds(pos: Vector2i) -> bool:
	return pos.x >= 0 and pos.x < GRID_W and pos.y >= 0 and pos.y < GRID_H

func _instantiate_rooms() -> void:
	for x in GRID_W:
		for y in GRID_H:
			if floor_grid[x][y] != null:
				var room_type := floor_grid[x][y]["type"]
				var room_id := "room_%d_%d" % [x, y]
				floor_grid[x][y]["room_id"] = room_id
				floor_grid[x][y]["grid_pos"] = Vector2i(x, y)
				# In a full implementation, instantiate room scene at (x * ROOM_SIZE, y * ROOM_SIZE)
				# For scaffolding, we just log it
				print("  [Room] %s type=%s at (%d, %d)" % [room_id, room_type, x, y])

func _place_player() -> void:
	if GameManager.player_node:
		GameManager.player_node.global_position = Vector2(start_pos.x * ROOM_SIZE + 160, start_pos.y * ROOM_SIZE + 160)

func _count_rooms() -> int:
	var count := 0
	for x in GRID_W:
		for y in GRID_H:
			if floor_grid[x][y] != null:
				count += 1
	return count

func _on_floor_loaded(floor_num: int) -> void:
	generate_floor(floor_num)

func _on_room_cleared(room_id: String) -> void:
	rooms_visited[room_id] = true
	# Check if boss room cleared → spawn portal
	var room = _find_room_by_id(room_id)
	if room and room["type"] == "boss":
		_spawn_portal(room["grid_pos"])
		EventBus.boss_defeated.emit("floor_%d_boss" % current_floor)
		EventBus.dungeon_floor_complete.emit(current_floor)

func _find_room_by_id(room_id: String) -> Dictionary:
	for x in GRID_W:
		for y in GRID_H:
			if floor_grid[x][y] != null and floor_grid[x][y].get("room_id") == room_id:
				return floor_grid[x][y]
	return {}

func _spawn_portal(grid_pos: Vector2i) -> void:
	var portal_pos := Vector2(grid_pos.x * ROOM_SIZE + 160, grid_pos.y * ROOM_SIZE + 160)
	EventBus.portal_spawned.emit(portal_pos)
	print("[DungeonGen] Portal spawned at %s" % portal_pos)

func get_adjacent_rooms(grid_pos: Vector2i) -> Array:
	var adj := []
	var dirs := [Vector2i(1, 0), Vector2i(-1, 0), Vector2i(0, 1), Vector2i(0, -1)]
	for d in dirs:
		var n := grid_pos + d
		if _in_bounds(n) and floor_grid[n.x][n.y] != null:
			adj.append(floor_grid[n.x][n.y])
	return adj

func spawn_enemies_in_room(room_id: String, room_level: int) -> void:
	var room = _find_room_by_id(room_id)
	if room.is_empty():
		return
	var pack_size := int(3 + room_level * 0.5)
	var enemy_group_id := "floor_%d" % current_floor
	var group := DataManager.get_enemy_group(enemy_group_id)
	if group.is_empty():
		group = DataManager.get_enemy_group("default")
	var enemy_ids: Array = group.get("enemies", ["slime"])
	for i in pack_size:
		var enemy_id := enemy_ids[randi() % enemy_ids.size()]
		# In full implementation, instantiate enemy scene at random position in room
		print("  [Spawn] %s in %s" % [enemy_id, room_id])