from classes.room import room
mesh_n = 4

r1 = room(1,1,mesh_n)
r1.set_top(0,0,15)
r1.set_bottom(0,0,15)
r1.set_left(0,0,40)

r1.fill_v()
r1.add_room_boundry(0,0,"right")

r1.print_v()



r2 = room(1,2,mesh_n)
r2.set_top(0,0,40)
r2.set_left(0,0,15)
r2.add_room_boundry(0,0,"right")

r2.set_right(0,1,15)
r2.set_bottom(0,1,5)
r2.add_room_boundry(0,1,"left")
r2.fill_v()


r2.print_v()




r3 = room(1,1,mesh_n)
r3.set_top(0,0,15)
r3.set_right(0,0,40)
r3.set_bottom(0,0,15)
r3.add_room_boundry(0,0,"left")
r3.fill_v()

r3.print_v()
