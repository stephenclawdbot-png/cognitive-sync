## State.gd
## Base class for all character states. Override _enter, _exit, _update, _physics_update.
extends Node

var state_machine: Node = null
var character: CharacterBody2D = null

func _ready() -> void:
	# Wait for parent to be ready, then grab references
	await get_tree().process_frame
	if get_parent() is CharacterBody2D:
		character = get_parent()
	elif get_parent().has_node("../Character"):
		character = get_parent().get_node("../Character")
	if character and character.has_node("StateMachine"):
		state_machine = character.get_node("StateMachine")

# Override these in subclasses
func _enter(_msg: Dictionary = {}) -> void:
	pass

func _exit() -> void:
	pass

func _update(_delta: float) -> void:
	pass

func _physics_update(_delta: float) -> void:
	pass

func _handle_input(_event: InputEvent) -> void:
	pass

# Utility: transition to another state
func transition_to(target_state: String, msg: Dictionary = {}) -> void:
	if state_machine:
		state_machine.transition_to(target_state, msg)