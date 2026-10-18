@tool  # damit man die Fahne auch im Editor sieht
extends Area2D
# Die Zielfahne am Ende des Levels.

signal reached

var done = false


func _ready():
	if not Engine.is_editor_hint():
		body_entered.connect(_on_body_entered)


func _on_body_entered(body):
	if body.is_in_group("player") and not done:
		done = true
		queue_redraw()  # Fahne wird gruen
		reached.emit()


func _draw():
	# Stange
	draw_rect(Rect2(-3, -160, 6, 160), Color("dddddd"))
	# Kugel oben
	draw_rect(Rect2(-6, -168, 12, 10), Color("ffd54a"))
	# Fahne
	var color = Color("ff5c8a")
	if done:
		color = Color("7ed957")
	draw_colored_polygon(PackedVector2Array([
		Vector2(3, -156), Vector2(60, -136), Vector2(3, -116)
	]), color)
