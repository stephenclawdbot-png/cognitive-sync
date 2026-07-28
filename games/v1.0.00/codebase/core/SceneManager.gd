## SceneManager.gd
## Handles scene transitions with fade-out/fade-in. Add a CanvasLayer with ColorRect for transitions.
extends Node

var current_scene: Node = null
var transition_layer: CanvasLayer = null
var fade_rect: ColorRect = null
var pending_scene: String = ""
var pending_params: Dictionary = {}

func _ready() -> void:
	_setup_transition_layer()
	EventBus.scene_change_requested.connect(load_scene)
	current_scene = get_tree().current_scene

func _setup_transition_layer() -> void:
	transition_layer = CanvasLayer.new()
	transition_layer.layer = 100
	fade_rect = ColorRect.new()
	fade_rect.color = Color.BLACK
	fade_rect.modulate.a = 0.0
	fade_rect.size = Vector2(640, 360)
	transition_layer.add_child(fade_rect)
	add_child(transition_layer)

func load_scene(scene_path: String, params: Dictionary = {}) -> void:
	pending_scene = scene_path
	pending_params = params
	EventBus.ui_transition_started.emit()
	_fade_out()

func _fade_out() -> void:
	var tween := create_tween()
	tween.tween_property(fade_rect, "modulate:a", 1.0, 0.3)
	tween.tween_callback(_swap_scene)

func _swap_scene() -> void:
	if current_scene:
		current_scene.queue_free()
	var packed := load(pending_scene)
	if packed is PackedScene:
		current_scene = packed.instantiate()
		get_tree().current_scene = current_scene
		get_tree().root.add_child(current_scene)
		_fade_in()
	else:
		push_error("[SceneManager] Failed to load: %s" % pending_scene)
		_fade_in()

func _fade_in() -> void:
	var tween := create_tween()
	tween.tween_property(fade_rect, "modulate:a", 0.0, 0.3)
	tween.tween_callback(func(): EventBus.ui_transition_complete.emit())