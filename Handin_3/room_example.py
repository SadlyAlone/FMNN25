from classes.room import room
import matplotlib.pyplot as plt

n = 20
r1 = room(1,1,n)
r1.set_top(0,0,15)
r1.set_bottom(0,0,15)
r1.set_left(0,0,40)
r1.fill_v()
r1.add_room_boundary(0,0,"right", "neumann")

#r1.print_v()


r2 = room(1,2,n)
r2.set_top(0,0,40)
r2.set_left(0,0,15)
r2.set_right(0,0,15)
r2.add_room_boundary(0,0, "right", "dirichlet")
r2.set_right(0,1,15)
r2.set_bottom(0,1,5)
r2.set_left(0,1,15)
r2.add_room_boundary(0,1,"left", "dirichlet")
r2.fill_v()

#r2.print_v()


r3 = room(1,1,n)
r3.set_top(0,0,15)
r3.set_right(0,0,40)
r3.set_bottom(0,0,15)
r3.set_left(0,0,15)
r3.add_room_boundary(0,0,"left", "neumann")
r3.fill_v()

#r3.print_v()
w = 0.8
for i in range(10):
    #r2.print_v()
    r1_old = r1.v
    r2_old = r2.v
    r3_old = r3.v

    r2()
    v_matrix = r2.v.reshape(r2.steps_y, r2.steps_x)
    r1_beyond = v_matrix[n+1:-1,1] - v_matrix[n+1:-1,0]
    r3_beyond = v_matrix[1:n-1,-2] - v_matrix[1:n-1,-1]

    r1(r1_beyond)
    r3(r3_beyond)


    b1 = r1.v[r1.boundary[1:-1]]
    b3 = r3.v[r3.boundary[1:-1]]


    r2.v[n*(n+1): n*n*2-n: n] = b1
    r2.v[2*n-1:n*n-1:n] = b3

    r1.v = w*r1.v + (1-w)*r1_old
    r2.v = w*r2.v + (1-w)*r2_old
    r3.v = w*r3.v + (1-w)*r3_old



    print(i)
    print("Room 1")
    r1.print_v()
    print("Room 2")
    r2.print_v()
    print("Room 3")
    r3.print_v()
plt.imshow(r2.v.reshape(r2.steps_y, r2.steps_x), cmap="coolwarm")
plt.show()
