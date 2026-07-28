## HUD.gd
## In-game HUD overlay — health bar, mana bar, XP bar, minimap, skill icons.
extends CanvasLayer

@onready var health_bar: ProgressBar = $HUDContainer/HealthBar
@onready var mana_bar: ProgressBar = $HUDContainer/ManaBar
@onready var xp_bar: ProgressBar = $HUDContainer/XPBar
@onready var gold_label: Label = $HUDContainer/GoldLabel
@onready var floor_label: Label = $HUDContainer/FloorLabel
@onready var skill_icons: HBoxContainer = $HUDContainer/SkillIcons

func _ready() -> void:
	EventBus.player_health_changed.connect(_on_health_changed)
	EventBus.player_mana_changed.connect(_on_mana_changed)
	EventBus.player_xp_changed.connect(_on_xp_changed)
	EventBus.player_gold_changed.connect(_on_gold_changed)
	EventBus.gold_changed.connect(_on_gold_changed)
	EventBus.dungeon_floor_loaded.connect(_on_floor_loaded)
	EventBus.skill_cooldown_started.connect(_on_skill_cd_started)
	EventBus.skill_cooldown_finished.connect(_on_skill_cd_finished)
	EventBus.ui_show_notification.connect(_on_notification)

func _on_health_changed(current: int, maximum: int) -> void:
	health_bar.value = float(current) / float(maximum) * 100
	health_bar.get_node("Label").text = "%d / %d" % [current, maximum]

func _on_mana_changed(current: int, maximum: int) -> void:
	mana_bar.value = float(current) / float(maximum) * 100
	mana_bar.get_node("Label").text = "%d / %d" % [current, maximum]

func _on_xp_changed(current: int, needed: int) -> void:
	xp_bar.value = float(current) / float(needed) * 100

func _on_gold_changed(total: int) -> void:
	gold_label.text = "Gold: %d" % total

func _on_floor_loaded(floor_num: int) -> void:
	floor_label.text = "Floor %d" % floor_num

func _on_skill_cd_started(_skill_id: String, _duration: float) -> void:
	# Show cooldown overlay on skill icon
	pass

func _on_skill_cd_finished(_skill_id: String) -> void:
	# Remove cooldown overlay
	pass

func _on_notification(title: String, body: String) -> void:
	# Show temporary notification banner
	print("[HUD] %s: %s" % [title, body])