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

#r1.print_v()

r1.update_inner()
r1.print_v()
