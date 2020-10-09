from classes.room import room
from scipy.sparse.linalg import spsolve
from scipy.sparse import csc_matrix
mesh_n = 4

r1 = room(1,1,mesh_n)
r1.set_top(0,0,15)
r1.set_bottom(0,0,15)
r1.set_left(0,0,40)

r1.fill_v()
r1.add_room_boundry(0,0,"right")
print(r1.boundries)
print("The boundries for r1")
print()
r1.print_v()
print("The initial r1")
print()
r1.update_inner()
r1.print_v()



print("r1 with updated inner points")
print()


r2 = room(1,2,mesh_n)
r2.set_top(0,0,40)
r2.set_left(0,0,15)
r2.add_room_boundry(0,0,"right")

r2.set_right(0,1,15)
r2.set_bottom(0,1,5)
r2.add_room_boundry(0,1,"left")
r2.fill_v()

print(r2.boundries)
print("The boundries for r2")
print()
r2.print_v()
print("The initial r2")
print()
r2.update_inner()
r2.print_v()
print("r2 with updated inner points")
print()


r3 = room(1,1,mesh_n)
r3.set_top(0,0,15)
r3.set_right(0,0,40)
r3.set_bottom(0,0,15)
r3.add_room_boundry(0,0,"left")
r3.fill_v()

print(r3.boundries)
print("The boundries for r3")
print()
r3.print_v()
print("The initial r3")
print()
r3.update_inner()
r3.print_v()
print("r3 with updated inner points")
