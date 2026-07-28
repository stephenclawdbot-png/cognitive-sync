## MainMenu.gd
## Main menu scene — new game, continue, settings, quit.
extends Control

@onready var new_game_btn: Button = $VBox/NewGame
@onready var continue_btn: Button = $VBox/Continue
@onready var settings_btn: Button = $VBox/Settings
@onready var quit_btn: Button = $VBox/Quit

func _ready() -> void:
	new_game_btn.pressed.connect(_on_new_game)
	continue_btn.pressed.connect(_on_continue)
	settings_btn.pressed.connect(_on_settings)
	quit_btn.pressed.connect(_on_quit)
	# Enable continue only if save exists
	continue_btn.disabled = not SaveSystem.has_save(0)
	EventBus.music_play_requested.emit("main_menu")

func _on_new_game() -> void:
	EventBus.sfx_play_requested.emit("ui_click")
	# Class selection would happen here — for now, default
	GameManager.start_new_run()

func _on_continue() -> void:
	EventBus.sfx_play_requested.emit("ui_click")
	var save_data := SaveSystem.load_slot(0)
	if save_data.is_empty():
		return
	var player_data: Dictionary = save_data.get("player", {})
	var game_data: Dictionary = save_data.get("game", {})
	# Restore game state
	GameManager.current_floor = game_data.get("current_floor", 1)
	GameManager.run_seed = game_data.get("run_seed", 0)
	GameManager.run_time = game_data.get("run_time", 0.0)
	GameManager.rooms_cleared = game_data.get("rooms_cleared", 0)
	GameManager.total_kills = game_data.get("total_kills", 0)
	GameManager.total_gold = game_data.get("total_gold", 0)
	# Load into dungeon
	GameManager.change_state(GameManager.GameState.PLAYING)
	SceneManager.load_scene("res://scenes/Dungeon.tscn")

func _on_settings() -> void:
	EventBus.sfx_play_requested.emit("ui_click")
	# Settings panel would open here
	pass

func _on_quit() -> void:
	EventBus.sfx_play_requested.emit("ui_click")
	get_tree().quit()