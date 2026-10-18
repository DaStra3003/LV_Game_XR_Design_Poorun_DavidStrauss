extends Area2D
# Ein Hundehaufen. Wer reintritt, verliert.
# Das Spritesheet (assets/poop.png) hat 4 Bilder, die wackeln und Fliegen zeigen.
# "size" im Inspector: 1 = klein, 2 = mittel, 3 = gross

signal jumped_over  # wird ausgeloest, wenn die Spielerin drueber ist

@export_range(1, 3) var size = 2

var anim_time = 0.0
var counted = false  # damit jeder Haufen nur einmal Punkte gibt

@onready var sprite = $Sprite2D


func _ready():
	# Groesse einstellen: das Sprite und die Kollisionsbox skalieren
	scale = Vector2(size, size)
	# Zeitversatz, damit nicht alle Haufen gleichzeitig wackeln
	anim_time = position.x * 0.01
	body_entered.connect(_on_body_entered)


func _process(delta):
	# Animation: alle 0.15 Sekunden das naechste Bild
	anim_time += delta
	sprite.frame = int(anim_time / 0.15) % 4

	# Punkt zaehlen, wenn die Spielerin am Haufen vorbei ist
	if counted:
		return
	var player = get_tree().get_first_node_in_group("player")
	if player != null and player.alive and player.position.x > position.x + 30 * size:
		counted = true
		jumped_over.emit()


func _on_body_entered(body):
	if body.is_in_group("player"):
		body.die()


func reset():
	counted = false
