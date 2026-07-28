## StateMachine.gd
## Manages state transitions for a character. Add State child nodes and set initial_state.
extends Node

@export var initial_state: String = "Idle"

var current_state: State = null
var states: Dictionary = {}
var character: CharacterBody2D = null

func _ready() -> void:
	character = get_parent()
	for child in get_children():
		if child is State:
			states[child.name] = child
			child.state_machine = self
			child.character = character
	if states.has(initial_state):
		current_state = states[initial_state]
		current_state._enter()
	else:
		push_error("[StateMachine] Initial state '%s' not found!" % initial_state)

func _process(delta: float) -> void:
	if current_state:
		current_state._update(delta)

func _physics_process(delta: float) -> void:
	if current_state:
		current_state._physics_update(delta)

func _unhandled_input(event: InputEvent) -> void:
	if current_state:
		current_state._handle_input(event)

func transition_to(target_state: String, msg: Dictionary = {}) -> void:
	if not states.has(target_state):
		push_warning("[StateMachine] State '%s' not found" % target_state)
		return
	if current_state:
		current_state._exit()
	current_state = states[target_state]
	current_state._enter(msg)