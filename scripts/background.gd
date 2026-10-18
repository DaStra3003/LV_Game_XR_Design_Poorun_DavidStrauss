extends Node2D
# Der Hintergrund: Himmel, Sonne, Wolken und Huegel.
# Er wird einmal gezeichnet und bewegt sich nicht (liegt in einem CanvasLayer).


func _draw():
	var width = 1280
	var height = 720

	# Himmel mit Farbverlauf (oben dunkler, unten heller)
	draw_polygon(
		PackedVector2Array([Vector2(0, 0), Vector2(width, 0), Vector2(width, height), Vector2(0, height)]),
		PackedColorArray([Color("4aa8f0"), Color("4aa8f0"), Color("dff4ff"), Color("dff4ff")])
	)

	# Sonne
	draw_circle(Vector2(1050, 130), 60, Color("ffe066"))
	draw_circle(Vector2(1050, 130), 46, Color("ffd93b"))

	# Wolken
	draw_cloud(Vector2(180, 120))
	draw_cloud(Vector2(560, 70))
	draw_cloud(Vector2(880, 170))

	# Huegel hinten (heller) und vorne
	draw_hills(height * 0.66, Color("9ad8b4"), 0.0)
	draw_hills(height * 0.78, Color("62bd7c"), 2.0)


func draw_cloud(pos):
	draw_circle(pos + Vector2(-30, 0), 22, Color.WHITE)
	draw_circle(pos + Vector2(0, -10), 30, Color.WHITE)
	draw_circle(pos + Vector2(32, 0), 24, Color.WHITE)
	draw_rect(Rect2(pos.x - 40, pos.y, 90, 14), Color.WHITE)


func draw_hills(base_y, color, offset):
	# Eine Wellenlinie aus Punkten, unten geschlossen
	var points = PackedVector2Array()
	for x in range(0, 1281, 20):
		var y = base_y + sin(x * 0.006 + offset) * 40
		points.append(Vector2(x, y))
	points.append(Vector2(1280, 720))
	points.append(Vector2(0, 720))
	draw_colored_polygon(points, color)
