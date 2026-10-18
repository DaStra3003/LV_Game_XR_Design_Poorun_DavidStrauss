@tool  # damit man die Plattform auch im Editor sieht
extends StaticBody2D
# Eine Plattform aus Erde mit Gras oben drauf.
# Die Groesse stelle ich im Inspector ueber "size" ein.
# Der Ursprung ist die linke obere Ecke.

@export var size = Vector2(400, 200):
	set(value):
		size = value
		update_collision()
		queue_redraw()

const DIRT = Color("8b5a2b")
const GRASS = Color("4caf50")
const GRASS_LIGHT = Color("7ed957")


func _ready():
	update_collision()


func update_collision():
	if not is_inside_tree():
		return
	var shape = RectangleShape2D.new()
	shape.size = size
	$CollisionShape2D.shape = shape
	$CollisionShape2D.position = size / 2


func _draw():
	# Erde
	draw_rect(Rect2(Vector2.ZERO, size), DIRT)
	# Grasstreifen oben
	draw_rect(Rect2(0, 0, size.x, 12), GRASS)
	draw_rect(Rect2(0, 0, size.x, 4), GRASS_LIGHT)
	# ein paar Grasbueschel ueber der Kante
	for x in range(6, int(size.x) - 6, 24):
		draw_rect(Rect2(x, -6, 3, 6), GRASS)
		draw_rect(Rect2(x + 6, -4, 3, 4), GRASS_LIGHT)
