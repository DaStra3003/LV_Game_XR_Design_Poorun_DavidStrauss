extends Node2D
# Hauptszene: kuemmert sich um Punkte, Tod und das Ziel.

var score = 0
var finished = false
var start_position

@onready var player = $Player
@onready var score_label = $HUD/Score
@onready var message_label = $HUD/Message
@onready var music = $Music


func _ready():
	start_position = player.position
	player.died.connect(_on_player_died)

	# Musik in Endlosschleife: wenn sie fertig ist, einfach nochmal starten
	music.finished.connect(music.play)

	# Alle Haufen und das Ziel mit dieser Szene verbinden
	for poop in get_tree().get_nodes_in_group("poops"):
		poop.jumped_over.connect(_on_jumped_over)
	for goal in get_tree().get_nodes_in_group("goal"):
		goal.reached.connect(_on_goal_reached)

	update_score()
	message_label.text = ""


func _unhandled_input(event):
	# Nach dem Ziel: Enter startet das Level neu
	if finished and event.is_action_pressed("ui_accept"):
		get_tree().reload_current_scene()


func _on_jumped_over():
	score += 1
	update_score()


func update_score():
	score_label.text = "Haufen übersprungen: " + str(score)


func _on_player_died():
	message_label.text = "Igitt! Reingetreten!"
	await get_tree().create_timer(1.5).timeout
	# Alles zuruecksetzen
	score = 0
	update_score()
	for poop in get_tree().get_nodes_in_group("poops"):
		poop.reset()
	player.respawn(start_position)
	message_label.text = ""


func _on_goal_reached():
	finished = true
	message_label.text = "Geschafft!\nEnter = nochmal spielen"
