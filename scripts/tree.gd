@tool  # damit man den Baum auch im Editor sieht
extends Node2D
# Ein einfacher Baum als Deko. Ursprung = unten am Stamm.


func _draw():
	# Stamm
	draw_rect(Rect2(-6, -70, 12, 70), Color("7a5230"))
	# Blaetter (drei Kreise)
	draw_circle(Vector2(-18, -66), 22, Color("3f9d57"))
	draw_circle(Vector2(18, -66), 22, Color("3f9d57"))
	draw_circle(Vector2(0, -86), 26, Color("3f9d57"))
	draw_circle(Vector2(-6, -94), 10, Color("5cc274"))
