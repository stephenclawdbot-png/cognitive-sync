## Dungeon.tscn script
## Main dungeon scene — hosts DungeonGenerator, player, enemies, HUD.
extends Node2D

@onready var dungeon_gen: Node = $DungeonGenerator
@onready var player: CharacterBody2D = $Player
@onready var hud: CanvasLayer = $HUD
@onready var tilemap: TileMap = $TileMap

func _ready() -> void:
	EventBus.game_started.connect(_on_game_started)
	# If continuing a run, load current floor
	if GameManager.current_state == GameManager.GameState.PLAYING:
		dungeon_gen.generate_floor(GameManager.current_floor)

func _on_game_started() -> void:
	dungeon_gen.generate_floor(1)

func _exit_tree() -> void:
	# Auto-save when leaving dungeon
	SaveSystem._save_slot(0)