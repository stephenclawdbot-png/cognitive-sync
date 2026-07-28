## AudioManager.gd
## Loads and plays SFX/music. SFX via AudioStreamPlayer pool; music via single stream with crossfade.
extends Node

var sfx_pool: Array[AudioStreamPlayer] = []
var music_player: AudioStreamPlayer = null
var music_fade_player: AudioStreamPlayer = null
var sfx_library: Dictionary = {}
var music_library: Dictionary = {}
var sfx_volume: float = 0.7
var music_volume: float = 0.5
var sfx_pool_size: int = 8
var next_sfx_index: int = 0

func _ready() -> void:
	_setup_players()
	_load_audio()
	EventBus.sfx_play_requested.connect(play_sfx)
	EventBus.music_play_requested.connect(play_music)
	EventBus.music_stopped.connect(stop_music)

func _setup_players() -> void:
	music_player = AudioStreamPlayer.new()
	music_player.bus = "Music"
	add_child(music_player)
	music_fade_player = AudioStreamPlayer.new()
	music_fade_player.bus = "Music"
	add_child(music_fade_player)
	for i in sfx_pool_size:
		var p := AudioStreamPlayer.new()
		p.bus = "SFX"
		add_child(p)
		sfx_pool.append(p)

func _load_audio() -> void:
	# Load SFX from /audio/sfx/ directory
	var sfx_dir := DirAccess.open("res://audio/sfx/")
	if sfx_dir:
		sfx_dir.list_dir_begin()
		var file := sfx_dir.get_next()
		while not file.is_empty():
			if file.ends_with(".wav") or file.ends_with(".ogg"):
				var id := file.get_basename()
				sfx_library[id] = load("res://audio/sfx/" + file)
			file = sfx_dir.get_next()
	# Load music from /audio/music/
	var music_dir := DirAccess.open("res://audio/music/")
	if music_dir:
		music_dir.list_dir_begin()
		var file := music_dir.get_next()
		while not file.is_empty():
			if file.ends_with(".ogg"):
				var id := file.get_basename()
				music_library[id] = load("res://audio/music/" + file)
			file = music_dir.get_next()

func play_sfx(sfx_id: String) -> void:
	if not sfx_library.has(sfx_id):
		return
	var player := sfx_pool[next_sfx_index]
	next_sfx_index = (next_sfx_index + 1) % sfx_pool_size
	player.stream = sfx_library[sfx_id]
	player.volume_db = linear_to_db(sfx_volume)
	player.play()

func play_music(track_id: String) -> void:
	if not music_library.has(track_id):
		return
	if music_player.stream == music_library[track_id] and music_player.playing:
		return
	music_fade_player.stream = music_player.stream
	music_fade_player.volume_db = music_player.volume_db
	music_fade_player.play()
	music_player.stream = music_library[track_id]
	music_player.volume_db = -60.0
	music_player.play()
	var tween := create_tween()
	tween.tween_property(music_player, "volume_db", linear_to_db(music_volume), 1.0)
	tween.parallel().tween_property(music_fade_player, "volume_db", -60.0, 1.0)
	tween.tween_callback(func(): music_fade_player.stop())

func stop_music() -> void:
	var tween := create_tween()
	tween.tween_property(music_player, "volume_db", -60.0, 0.5)
	tween.tween_callback(func(): music_player.stop())

func set_sfx_volume(vol: float) -> void:
	sfx_volume = clampf(vol, 0.0, 1.0)

func set_music_volume(vol: float) -> void:
	music_volume = clampf(vol, 0.0, 1.0)
	music_player.volume_db = linear_to_db(music_volume)