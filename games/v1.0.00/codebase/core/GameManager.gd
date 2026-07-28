## GameManager.gd
## Top-level game state controller. Manages run state, score, and cross-system coordination.
extends Node

enum GameState { MENU, PLAYING, PAUSED, GAME_OVER, TRANSITION }

var current_state: GameState = GameState.MENU
var current_floor: int = 1
var current_room_id: String = ""
var run_seed: int = 0
var run_time: float = 0.0
var rooms_cleared: int = 0
var total_kills: int = 0
var total_gold: int = 0
var player_node: Node = null

# Run modifiers (for future ascendancy / difficulty system)
var run_modifiers: Dictionary = {}

# Callback registry for state transitions
var _state_handlers: Dictionary = {}

func _ready() -> void:
	EventBus.game_started.connect(_on_game_started)
	EventBus.game_over.connect(_on_game_over)
	EventBus.room_cleared.connect(_on_room_cleared)
	EventBus.enemy_died.connect(_on_enemy_died)
	EventBus.dungeon_floor_complete.connect(_on_floor_complete)
	EventBus.portal_entered.connect(_on_portal_entered)
	EventBus.ui_pause_requested.connect(_pause)
	EventBus.ui_resume_requested.connect(_resume)

func _process(delta: float) -> void:
	if current_state == GameState.PLAYING:
		run_time += delta

# ── State management ────────────────────────────────────────────

func change_state(new_state: GameState) -> void:
	if current_state == new_state:
		return
	var old_state = current_state
	current_state = new_state
	print("[GameManager] State: %s → %s" % [state_name(old_state), state_name(new_state)])
	match new_state:
		GameState.PLAYING:
			get_tree().paused = false
		GameState.PAUSED:
			get_tree().paused = true
		GameState.GAME_OVER:
			get_tree().paused = true
			EventBus.game_saved.emit(0)

func state_name(s: GameState) -> String:
	return GameState.keys()[s]

# ── Run lifecycle ───────────────────────────────────────────────

func start_new_run(seed_value: int = 0) -> void:
	run_seed = seed_value if seed_value != 0 else randi()
	current_floor = 1
	run_time = 0.0
	rooms_cleared = 0
	total_kills = 0
	total_gold = 0
	run_modifiers.clear()
	change_state(GameState.PLAYING)
	EventBus.game_started.emit()
	seed(run_seed)
	SceneManager.load_scene("res://scenes/Hub.tscn")

func end_run() -> void:
	change_state(GameState.GAME_OVER)
	EventBus.game_over.emit()

# ── Signal handlers ─────────────────────────────────────────────

func _on_game_started() -> void:
	print("[GameManager] New run started — seed: %d" % run_seed)

func _on_game_over() -> void:
	print("[GameManager] Game over — floor: %d, kills: %d, time: %.1fs" % [current_floor, total_kills, run_time])

func _on_room_cleared(room_id: String) -> void:
	rooms_cleared += 1
	EventBus.ui_show_notification.emit("Room Cleared!", "Floor %d — %d rooms cleared" % [current_floor, rooms_cleared])

func _on_enemy_died(enemy: Node, xp_reward: int, gold_reward: int) -> void:
	total_kills += 1
	total_gold += gold_reward

func _on_floor_complete(floor_num: int) -> void:
	print("[GameManager] Floor %d complete!" % floor_num)

func _on_portal_entered(floor_num: int) -> void:
	current_floor = floor_num
	EventBus.dungeon_floor_loaded.emit(floor_num)

func _pause() -> void:
	change_state(GameState.PAUSED)
	EventBus.game_paused.emit()

func _resume() -> void:
	change_state(GameState.PLAYING)
	EventBus.game_resumed.emit()