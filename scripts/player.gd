extends CharacterBody2D
# Das ist meine Spielfigur. Sie kann nach links und rechts laufen und springen.
# Die Grafik ist ein Spritesheet (assets/girl.png) mit 6 Bildern nebeneinander:
# 0 = stehen, 1-3 = laufen, 4 = springen, 5 = getroffen

signal died  # wird ausgeloest, wenn die Figur stirbt

const SPEED = 300.0          # Laufgeschwindigkeit
const JUMP_FORCE = -760.0    # negativ = nach oben (Sprunghoehe ca. 180 Pixel)
const GRAVITY = 1600.0
const FALL_LIMIT = 900.0     # wer tiefer faellt, ist raus

var alive = true
var run_time = 0.0  # zaehlt fuer die Laufanimation hoch

@onready var sprite = $Sprite2D


func _physics_process(delta):
	# Wenn die Figur tot ist, faellt sie einfach aus dem Bild (wie bei Mario)
	if not alive:
		velocity.y += GRAVITY * delta
		position += velocity * delta
		return

	# Schwerkraft
	if not is_on_floor():
		velocity.y += GRAVITY * delta

	# Springen (nur am Boden)
	if Input.is_action_just_pressed("jump") and is_on_floor():
		velocity.y = JUMP_FORCE

	# Wenn man die Sprungtaste frueh loslaesst, springt man weniger hoch
	if Input.is_action_just_released("jump") and velocity.y < 0:
		velocity.y = velocity.y * 0.5

	# Links / Rechts
	var direction = Input.get_axis("move_left", "move_right")
	velocity.x = direction * SPEED

	move_and_slide()

	# Nicht links aus dem Level laufen
	if position.x < 16:
		position.x = 16

	update_animation(direction, delta)

	# In ein Loch gefallen?
	if position.y > FALL_LIMIT:
		die()


func update_animation(direction, delta):
	# Blickrichtung spiegeln
	if direction < 0:
		sprite.flip_h = true
	elif direction > 0:
		sprite.flip_h = false

	if not is_on_floor():
		sprite.frame = 4
	elif direction != 0:
		# Laufanimation: alle 0.1 Sekunden das naechste Bild (1, 2, 3, 2, 1, ...)
		run_time += delta
		var step = int(run_time / 0.1) % 4
		sprite.frame = [1, 2, 3, 2][step]
	else:
		sprite.frame = 0
		run_time = 0.0


func die():
	if not alive:
		return
	alive = false
	sprite.frame = 5
	velocity = Vector2(0, -500)  # kleiner Huepfer nach oben, dann faellt sie raus
	died.emit()


func respawn(start_position):
	alive = true
	position = start_position
	velocity = Vector2.ZERO
	sprite.frame = 0
	$Camera2D.reset_smoothing()
