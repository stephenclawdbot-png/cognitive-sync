## NPCBase.gd
## Base class for hub NPCs. Handles dialog, shop, and quest interactions.
extends CharacterBody2D

@export var npc_id: String = "merchant"
@export var npc_name: String = "Merchant"
@export var interact_range: float = 50.0
@export var dialog_id: String = "merchant_default"
@export var shop_inventory: Array[String] = []

var is_interacting: bool = false
var player_in_range: bool = false

@onready var sprite: Sprite2D = $Sprite2D
@onready var interaction_area: Area2D = $InteractionArea
@onready var dialog_label: Label = $DialogLabel

func _ready() -> void:
	add_to_group("npc")
	interaction_area.body_entered.connect(_on_body_entered)
	interaction_area.body_exited.connect(_on_body_exited)
	dialog_label.visible = false
	_load_npc_data()

func _load_npc_data() -> void:
	var data := DataManager.get_npc(npc_id)
	if data.is_empty():
		return
	npc_name = data.get("name", npc_name)
	dialog_id = data.get("dialog_id", dialog_id)
	shop_inventory = data.get("shop_inventory", [])

func _on_body_entered(body: Node) -> void:
	if body.is_in_group("player"):
		player_in_range = true
		dialog_label.text = "Press F to talk"
		dialog_label.visible = true

func _on_body_exited(body: Node) -> void:
	if body.is_in_group("player"):
		player_in_range = false
		dialog_label.visible = false
		is_interacting = false

func _process(_delta: float) -> void:
	if player_in_range and Input.is_action_just_pressed("interact") and not is_interacting:
		_interact()

func _interact() -> void:
	is_interacting = true
	EventBus.sfx_play_requested.emit("npc_talk")
	match npc_id:
		"merchant":
			_open_shop()
		"blacksmith":
			_open_upgrade()
		"quest_giver":
			_show_dialog()
		_:
			_show_dialog()

func _show_dialog() -> void:
	var dialog_data := DataManager.get_npc(npc_id).get("dialog", {})
	if dialog_data.is_empty():
		dialog_label.text = "..."
		return
	# Simple dialog display — full dialog system would use a DialogManager
	var lines: Array = dialog_data.get("lines", ["Hello, adventurer!"])
	for line in lines:
		dialog_label.text = line
		await get_tree().create_timer(2.0).timeout
	dialog_label.text = "Press F to talk again"
	is_interacting = false

func _open_shop() -> void:
	print("[NPC] Shop opened — %d items" % shop_inventory.size())
	for item_id in shop_inventory:
		var item := DataManager.get_item(item_id)
		print("  - %s: %d gold" % [item.get("name", item_id), item.get("value", 0)])
	# Full implementation would emit a signal to open shop UI
	EventBus.ui_show_notification.emit(npc_name, "Welcome to my shop!")

func _open_upgrade() -> void:
	EventBus.ui_show_notification.emit(npc_name, "Upgrade your equipment here!")