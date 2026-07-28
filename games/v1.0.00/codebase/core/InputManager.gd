## InputManager.gd
## Centralized input handling — processes raw input, fires EventBus signals.
extends Node

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("pause"):
		if GameManager.current_state == GameManager.GameState.PLAYING:
			EventBus.ui_pause_requested.emit()
		elif GameManager.current_state == GameManager.GameState.PAUSED:
			EventBus.ui_resume_requested.emit()

	if event.is_action_pressed("inventory"):
		if GameManager.current_state == GameManager.GameState.PLAYING:
			EventBus.inventory_opened.emit()
		elif GameManager.current_state == GameManager.GameState.PAUSED:
			EventBus.inventory_closed.emit()

	if event.is_action_pressed("skill_tree"):
		EventBus.sfx_play_requested.emit("ui_open")