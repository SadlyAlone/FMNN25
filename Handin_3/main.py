from classes.room import room

r = room(1,2,4)
r.set_top(0,0,15)
r.print_v()
r.set_bottom(0,0,15)
r.print_v()
r.set_left(0,0,40)
r.print_v()
r.set_right(0,0,20)
r.print_v()
r.fill_v()
r.print_v()

r.set_room_boundry(0,0,"right")
print(r.boundries)
