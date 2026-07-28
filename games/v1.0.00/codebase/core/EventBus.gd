## EventBus.gd
## Central signal bus — all cross-system communication goes through here.
## No system directly references another; everything emits or listens on EventBus.
extends Node

# ── Player signals ──────────────────────────────────────────────
signal player_health_changed(current: int, maximum: int)
signal player_mana_changed(current: int, maximum: int)
signal player_died
signal player_level_up(new_level: int)
signal player_xp_changed(current: int, needed: int)
signal player_gold_changed(total: int)
signal player_dash_state(active: bool)
signal player_stunned(duration: float)
signal player_status_applied(status_id: String, stacks: int)
signal player_status_removed(status_id: String)

# ── Combat signals ─────────────────────────────────────────────
signal enemy_spawned(enemy: Node)
signal enemy_died(enemy: Node, xp_reward: int, gold_reward: int)
signal enemy_damaged(enemy: Node, amount: int, is_crit: bool)
signal projectile_fired(projectile: Node)
signal damage_dealt(target: Node, amount: int, type: String, is_crit: bool)
signal boss_phase_changed(phase: int)

# ── Item / Inventory signals ────────────────────────────────────
signal item_picked_up(item_id: String, quantity: int)
signal item_dropped(item_id: String, quantity: int, position: Vector2)
signal equipment_changed(slot: String, item_id: String)
signal inventory_opened
signal inventory_closed
signal inventory_modified
signal gold_changed(total: int)

# ── Skill signals ──────────────────────────────────────────────
signal skill_unlocked(skill_id: String)
signal skill_activated(skill_id: String)
signal skill_cooldown_started(skill_id: String, duration: float)
signal skill_cooldown_finished(skill_id: String)
signal skill_point_awarded(total_points: int)
signal skill_point_spent(skill_id: String)

# ── Dungeon signals ─────────────────────────────────────────────
signal dungeon_floor_loaded(floor_num: int)
signal room_cleared(room_id: String)
signal room_entered(room_id: String, room_type: String)
signal dungeon_floor_complete(floor_num: int)
signal boss_defeated(boss_id: String)
signal portal_spawned(position: Vector2)
signal portal_entered(floor_num: int)

# ── UI signals ──────────────────────────────────────────────────
signal ui_show_damage_number(position: Vector2, amount: int, is_crit: bool)
signal ui_show_floating_text(position: Vector2, text: String, color: Color)
signal ui_show_notification(title: String, body: String)
signal ui_pause_requested
signal ui_resume_requested
signal ui_transition_started
signal ui_transition_complete

# ── Game state signals ──────────────────────────────────────────
signal game_started
signal game_paused
signal game_resumed
signal game_saved(slot: int)
signal game_loaded(slot: int)
signal game_over
signal scene_change_requested(scene_path: String, params: Dictionary)

# ── Audio signals ───────────────────────────────────────────────
signal sfx_play_requested(sfx_id: String)
signal music_play_requested(track_id: String)
signal music_stopped