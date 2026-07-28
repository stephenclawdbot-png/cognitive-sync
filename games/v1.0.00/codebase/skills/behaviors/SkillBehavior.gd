## SkillBehavior.gd
## Base class for skill behaviors. Override execute() in subclasses.
class_name SkillBehavior
extends RefCounted

var skill_data: Dictionary = {}

func execute(player: Node, data: Dictionary) -> void:
	skill_data = data
	_execute_impl(player)

func _execute_impl(_player: Node) -> void:
	pass