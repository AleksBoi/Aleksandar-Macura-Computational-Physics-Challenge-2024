import math
import matplotlib.pyplot as plt
import pygame

def pygame_setup(x,y,r,fps):
    pygame.init()
    orange = (249, 106, 0)
    purple = (161, 0, 179)
    screen = pygame.display.set_mode([x+2*r,y+2*r])
    running = True
    pygame.time.Clock().tick(fps)
    frame_counter = 0
    font = pygame.font.Font('freesansbold.ttf', 32)
 
    # create a text surface object,
    # on which text is drawn on it.
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        text = font.render(str((round(x_list[int(frame_counter)],2),round(y_list[int(frame_counter)],2))), True, purple, orange)
        textRect = text.get_rect()
        textRect.center = (9*x/10, y // 10)
        screen.blit(text, textRect)
        pygame.draw.circle(screen, (255, 0, 0), (r + x_list[int(frame_counter)]*int(round(x/end_point_X)), y+r-y_list[int(frame_counter)]*int(round(y/end_point_Y))), r)
        pygame.display.flip()
        frame_counter+=1
    pygame.quit()

"""
PYGAME TIMING SETUP
total time is times_list[-1]
set framerate and the seconds is 1/framerate 

seconds / timestep is the index of the coordinate lists

so every frame, the position of the ball is at that point

0 = usintheta ^2 + 2as s = usintheta^2/2g
"""

drag_coefficient_shapes = {
    "Sphere":0.47,
    "Half_sphere":0.42,
    "Cone":0.50,
    "Cube":1.05,
    "Angled_cube":0.8,
    "Long_cyliner":0.82,
    "Short_cylinder":1.15,
    "Streamlined_body":0.04,
    "Streamlined half-body":0.09
}

def init_graph(title):
    plt.title(title)
    plt.xlabel("x /m")
    plt.ylabel("y /m")
    plt.grid()

def Range_calc(velo, angle, grav, height):
    Range = (velo**2/grav)*(math.sin(angle)*math.cos(angle) + math.cos(angle)*((math.sin(angle)*math.sin(angle)+(2*grav*height/(velo)**2))**0.5))
    return Range

def plot_function(velo, angle, grav, height):
    Range = Range_calc(velo, angle, grav, height)
    
    def calc_y_from_x(x):
        y_displacement = height + x*math.tan(angle) - (grav/(2*velo**2)*(1+math.tan(angle)*math.tan(angle))*x**2)
        return y_displacement

    x_increment = 0
    x_pos = []
    y_pos = []
    while x_increment <= Range:
        x_pos.append(x_increment)
        y_pos.append(calc_y_from_x(x_increment))
        x_increment += 0.01
    plt.plot(x_pos,y_pos)

def draw_bounding_parabola(velo, Range, grav, height):
    def calc_y_from_x(x):
        y_displacement = (velo ** 2 / (2 * grav)) - (grav / (2* velo ** 2) * x ** 2)
        return y_displacement
    
    x_increment = 0
    x_pos = []
    y_pos = []
    while x_increment <= Range:
        x_pos.append(x_increment)
        y_pos.append(calc_y_from_x(x_increment))
        x_increment += 0.01

    plt.plot(x_pos,y_pos)

def distance_travelled_by_projectile(velo, angle, grav, X):
    def plug_in(var):
        return 0.5 * math.log(abs(((1+var**2)**0.5)+var)) + 0.5 * var * (1+var**2)**0.5
    left = velo ** 2 / (grav * (1 + math.tan(angle) ** 2))

    s = left * (plug_in(math.tan(angle)) - plug_in(math.tan(angle) - (grav * X / velo ** 2 ) * (1 + math.tan(angle) ** 2)))
    return s

def plot_using_x_and_y_as_function_of_t(u, g, angle, d):
    def y(t):
        init_velo_y = u*math.sin(angle)
        displacement_y = init_velo_y * t - 0.5 * g * (t**2)
        return displacement_y

    def x(t):
        init_velo_x = u*math.cos(angle)
        displacement_x = init_velo_x * t
        return round(displacement_x,3)
    
    angle = math.radians(angle)
    time = round((u * math.sin(angle) / g) + (u**2 * math.sin(angle)**2 / g ** 2 + 2 * d / g)**0.5,3)
    inc = 0
    x_list = []
    y_list = []
    while inc < time:
        x_list.append(x(inc))
        y_list.append(y(inc))
        inc+=0.001
    plt.plot(x_list,y_list)

def plot_r_against_t(u, g, angle, d):
    def y(t):
        init_velo_y = u*math.sin(angle)
        displacement_y = init_velo_y * t - 0.5 * g * (t**2)
        return round(displacement_y,3)

    def x(t):
        init_velo_x = u*math.cos(angle)
        displacement_x = init_velo_x * t
        return round(displacement_x,3)
    angle = math.radians(angle)
    time = 2.5
    inc = 0
    r_list = []
    t_list = []
    while inc < time:
        r_list.append((x(inc)**2 + y(inc)**2)**0.5)
        t_list.append(inc)
        inc+=0.001
    plt.plot(t_list,r_list)
    

def task_one():
    velo = int(input("enter velo: "))
    grav = float(input("enter grav: "))
    h = int(input("enter height: "))
    angle = math.radians(int(input("enter angle (degrees/90): ")))
    #function of y against time
    def y(t):
        init_velo_y = velo*math.sin(angle)
        current_velo_y = init_velo_y - grav * t
        displacement_y = h + init_velo_y * t - 0.5 * grav * (t**2)
        return round(displacement_y,3)

    def x(t):
        init_velo_x = velo*math.cos(angle)
        displacement_x = init_velo_x * t
        return round(displacement_x,3)

    def calc_landing_time():
        time = (velo*math.sin(angle)/grav) + ((velo*math.sin(angle)/grav)**2 + (2/grav)*h)**0.5
        return time

    t = 0
    x_pos = []
    y_pos = []
    while t <= calc_landing_time():
        x_pos.append(x(t))
        y_pos.append(y(t))
        t += 0.01

    plt.plot(x_pos,y_pos)
    init_graph("Projectile Motion Model: u = " + str(velo) + " g = " + str(grav) + " h = " + str(h) + " angle = " + str(round(math.degrees(angle),2)))
    plt.show()
    
def task_two():
    velo = float(input("enter velo: "))
    grav = float(input("enter grav: "))
    h = int(input("enter height: "))
    angle = math.radians(int(input("enter angle (degrees/90): ")))
    plot_function(velo, angle, grav, h)
    init_graph("Projectile trajectory: u = " + str(velo) + " g = " + str(grav) + " h = " + str(h) + " angle = " + str(round(math.degrees(angle),2)))
    #apogee
    plt.plot(velo**2 /grav * math.sin(angle) * math.cos(angle), h + (velo**2 / (2 * grav)) * math.sin(angle) * math.sin(angle), 'o')
    plt.show()

def task_three():
    def get_info():
        h = 0
        X_target = int(input("Enter x coord of target: "))
        Y_target = int(input("Enter y coord of target: "))
        grav = float(input("enter grav: "))
        minimum_velo = grav**0.5 * (Y_target + (X_target**2 + Y_target ** 2)**0.5)**0.5
        minimum_velo_angle = math.atan((Y_target+(X_target**2+Y_target**2)**0.5)/X_target)
        print ("Heres the minimum velocity to get to that point: " + str(minimum_velo))
        velo = input("enter velocity or nothing if you would like to use the minimum: ")
        if velo == "":
            velo = minimum_velo
        else: velo = float(velo)

        return X_target, Y_target, grav, velo, minimum_velo, minimum_velo_angle
    
    def get_both_angles(X_target, Y_target, grav, velo):
        a = (grav/(2*velo**2))*X_target**2
        b = -1 * X_target
        c = Y_target + (grav*X_target**2/(2*velo**2))
        denom = 2*a
        theta_plus = math.atan((-1*b+(b**2-4*a*c)**0.5)/denom)
        theta_minus = math.atan((-1*b-(b**2-4*a*c)**0.5)/denom)
        return theta_plus, theta_minus
    

    X_target, Y_target, grav, velo, minimum_velo, minimum_velo_angle = get_info()
    theta_plus, theta_minus = get_both_angles(X_target, Y_target, grav, velo)

    plot_function(velo,theta_plus,grav,0)
    plot_function(velo,theta_minus,grav,0)
    plot_function(minimum_velo, minimum_velo_angle, grav, 0)
    init_graph("Projectile to hit (" + str(X_target) + "," + str(Y_target) + ")")
    plt.plot(X_target,Y_target,'o')
    plt.legend(["high ball", "low ball","minimum velocity"])
    plt.show()

def task_four():
    def get_info():
        h = float(input("enter the height the projectile should be launched at: "))
        grav = float(input("enter grav: "))
        velo = float(input("enter velocity: "))
        angle = math.radians(float(input("enter launch angle (degrees): ")))

        max_angle = math.asin (
            1 / (2 + 2 * grav * h / velo ** 2) ** 0.5
        )


        return grav, velo, h, angle, max_angle
    
    grav, velo, height, angle, max_angle = get_info()
    print ('maximum angle is: ' + str(math.degrees(max_angle)))
    plot_function(velo, angle, grav, height)
    plot_function(velo, max_angle, grav, height)
    init_graph("Max Range Graphic: u = " + str(velo) + " g = " + str(grav) + " h = " + str(height) + " angle = " + str(round(math.degrees(angle),2)))
    plt.legend(["Range " + str(round(Range_calc(velo,angle,grav,height),2)), "Max Range " + str(round(Range_calc(velo, max_angle, grav, height),2)) + " at angle " + str(round(math.degrees(max_angle),2))])
    plt.show()

def task_five():
    def get_info():
        
        # basics
        grav = float(input("enter grav: "))
        h = 0

        #task 3 part 1
        X_target = int(input("Enter x coord of target: "))
        Y_target = int(input("Enter y coord of target: "))
        minimum_velo = grav**0.5 * (Y_target + (X_target**2 + Y_target ** 2)**0.5)**0.5
        minimum_velo_angle = math.atan((Y_target+(X_target**2+Y_target**2)**0.5)/X_target)
        print ("Heres the minimum velocity to get to that point: " + str(minimum_velo))
        velo = input("enter velocity or nothing if you would like to use the minimum: ")
        if velo == "":
            velo = minimum_velo
        else: velo = float(velo)

        #task 3 part 2
        a = (grav/(2*velo**2))*X_target**2
        b = -1 * X_target
        c = Y_target + (grav*X_target**2/(2*velo**2))
        denom = 2*a
        theta_plus = math.atan((-1*b+(b**2-4*a*c)**0.5)/denom)
        theta_minus = math.atan((-1*b-(b**2-4*a*c)**0.5)/denom)

        #task 4
        max_angle = math.asin (
            1 / (2 + 2 * grav * h / velo ** 2) ** 0.5
        )

        init_graph("projectile through " + str((X_target,Y_target)) + " u = " + str(velo) + " g = " + str(grav) + " h = 0m")

        return grav, velo, minimum_velo, minimum_velo_angle, max_angle, theta_plus, theta_minus
    grav, velo, minimum_velo, minimum_velo_angle, max_angle, theta_plus, theta_minus = get_info()
    plot_function(velo,theta_plus,grav,0)
    plot_function(velo,theta_minus,grav,0)
    plot_function(minimum_velo, minimum_velo_angle, grav, 0)
    plot_function(velo,max_angle,grav,0)
    draw_bounding_parabola(velo,Range_calc(velo,max_angle,grav,0),grav,0)
    plt.legend(["higher", "lower","minimum velocity","maximum range","bounding parabola"])
    plt.show()

def task_six():
    def get_info():
        h = float(input("enter the height the projectile should be launched at: "))
        grav = float(input("enter grav: "))
        velo = float(input("enter velocity: "))
        angle = math.radians(float(input("enter launch angle (degrees): ")))

        max_angle = math.asin (
            1 / (2 + 2 * grav * h / velo ** 2) ** 0.5
        )
        return grav, velo, h, angle, max_angle    
    grav, velo, height, angle, max_angle = get_info()
    print ('maximum angle is: ' + str(math.degrees(max_angle)))
    plot_function(velo, angle, grav, height)
    plot_function(velo, max_angle, grav, height)
    init_graph("u = " + str(velo) + " g = " + str(grav) + " h = " + str(height) + " s = " + str(round(distance_travelled_by_projectile(velo,angle,grav,Range_calc(velo,angle,grav,height)),2)) + " smax = " + str(round(distance_travelled_by_projectile(velo,max_angle,grav,Range_calc(velo,max_angle,grav,height)),2)))
    plt.legend(["Normal Angle = " + str (round(math.degrees(angle),2)),"Max Angle = " + str(round(math.degrees(max_angle),2))])
    plt.show()

def task_seven():
    # PART ONE
    velo = 10
    grav = 10
    def minus(u,g,angle):
        return (3*u)/(2*g) * (math.sin(angle) - (math.sin(angle)**2 - (8/9))**0.5)
    def plus(u,g,angle):
        return (3*u)/(2*g) * (math.sin(angle) + (math.sin(angle)**2 - (8/9))**0.5)
    def plot_max_and_min():
        angle = math.radians(70.51)
        plt.plot(velo*math.cos(angle) * minus(velo,grav,angle), velo*math.sin(angle) * minus(velo,grav,angle) - 0.5 * grav * (minus(velo,grav,angle)**2),'*')
        plt.plot(velo*math.cos(angle) * plus(velo,grav,angle), velo*math.sin(angle) * plus(velo,grav,angle) - 0.5 * grav * (plus(velo,grav,angle)**2),'*')
        angle = math.radians(78)
        plt.plot(velo*math.cos(angle) * minus(velo,grav,angle), velo*math.sin(angle) * minus(velo,grav,angle) - 0.5 * grav * (minus(velo,grav,angle)**2),'*')
        plt.plot(velo*math.cos(angle) * plus(velo,grav,angle), velo*math.sin(angle) * plus(velo,grav,angle) - 0.5 * grav * (plus(velo,grav,angle)**2),'*')
        angle = math.radians(85)
        plt.plot(velo*math.cos(angle) * minus(velo,grav,angle), velo*math.sin(angle) * minus(velo,grav,angle) - 0.5 * grav * (minus(velo,grav,angle)**2),'*')
        plt.plot(velo*math.cos(angle) * plus(velo,grav,angle), velo*math.sin(angle) * plus(velo,grav,angle) - 0.5 * grav * (plus(velo,grav,angle)**2),'*')
    def find_ts(u,g,angle):
        t_plus = (3*u)/(2*g) * (math.sin(angle) + (math.sin(angle)**2 - (8/9))**0.5)
        t_minus = (3*u)/(2*g) * (math.sin(angle) - (math.sin(angle)**2 - (8/9))**0.5)
        return t_plus, t_minus
    def find_r(u,g,t,angle):
        init_velo_y = u*math.sin(angle)
        displacement_y = init_velo_y * t - 0.5 * g * (t**2)
        init_velo_x = u*math.cos(angle)
        displacement_x = init_velo_x * t

        return (displacement_x**2 + displacement_y**2)**0.5
    
    list_of_angles_deg = [30, 45, 60, 70.5, 78, 85]
    for angle in list_of_angles_deg:
        plot_using_x_and_y_as_function_of_t(velo,grav,angle,5)
    plt.legend([30, 45, 60, 70.5, 78, 85])        
    plot_max_and_min()
    init_graph ("Projectiles v = 10m/s, g = 10m/s^2")
    plt.show()
    #PART TWO 
    plt.clf()
    for angle in list_of_angles_deg:
        plot_r_against_t(velo,grav,angle,5)
    for angle in list_of_angles_deg:
        if angle > 65:
            max_t, min_t = find_ts(velo,grav,math.radians(angle)) 
            plt.plot(max_t, find_r(velo,grav,max_t,math.radians(angle)),'*')
            plt.plot(min_t, find_r(velo,grav,min_t,math.radians(angle)),'*')
    plt.legend([30, 45, 60, 70.5, 78, 85])    
    plt.title("Projectiles v = 10m/s, g = 10m/s^2")
    plt.xlabel("t /s")
    plt.ylabel("r /m")
    plt.grid()
    plt.show()

def task_eight(bounce_total, timestep):
    def get_info():
        u = float(input("enter velo: "))
        g = float(input("enter grav: "))
        h = int(input("enter height: "))
        angle = math.radians(float(input("enter angle (degrees/90): ")))
        e = float(input("enter coefficient of restitution: "))
        return u,g,h,angle,e
    
    def get_vy_at_end_bounce_one():
        init_vy = u * math.sin(angle)
        end_vy = (init_vy**2 + 2 * g * h) ** 0.5
        return end_vy

    def make_displacement_lists(end_vy):
        x_list = []
        y_list = []
        actual_time = 0
        for loop in range (1,bounce_total+1):
            t = 0
            y_displacement = 0
            velo_y = u * math.sin(angle) * e ** (loop - 1)
            while y_displacement >= 0:
                if (loop - 1) == 0:
                    y_displacement = velo_y * t - (g/2) * (t ** 2) + h
                else: 
                    velo_y = end_vy * e ** (loop - 1)
                    y_displacement = (velo_y * t) - ((g/2) * (t ** 2))
                y_list.append(y_displacement)
                x_list.append(u*math.cos(angle)*actual_time)
                t += timestep
                actual_time += timestep
        print(actual_time)
        return x_list, y_list

    u,g,h,angle,e = get_info()
    x_list, y_list = make_displacement_lists(get_vy_at_end_bounce_one())
    end_point_X = x_list[-1]
    end_point_Y = (u * math.sin(angle)) ** 2 / (2*g) + h
    plt.plot(x_list,y_list)
    init_graph("u = " + str(u) + " g = " + str(g) + " h = " + str(h) + " e = " + str(e) + " angle = " + str(round(math.degrees(angle),1)))
    

    return x_list, y_list, end_point_X, end_point_Y

def task_nine(timestepincrement):
    def get_info():
        velo = int(input("enter velo: "))
        grav = float(input("enter grav: "))
        h = int(input("enter height: "))
        angle = math.radians(int(input("enter angle (degrees/90): ")))
        shape = float(input("Which shape would you like the ball to be: "))
        mass = float(input("How heavy should the ball be: "))
        air_density = float(input("How dense should the air be: "))
        cross_sectional_area = float(input("Cross sectional area size? "))
        #drag_coefficient = drag_coefficient_shapes[shape]
        #drag_coefficient = 0.1
        k = 0.5 * shape * air_density * cross_sectional_area / mass
        return velo,grav,h,angle, k
    def define_initial_parameters():
        t = 0
        x = 0
        y = h
        ux = u * math.cos(angle)
        ax = 0
        uy = u * math.sin(angle)
        ay = 0
        return t,ux,uy,ax,ay,x,y
    def change_parameters_accel():
        ax = -1 * ux * k * v
        ay = -1*g - uy * k * v
        return ax,ay
    def change_parameters_velo():
        vx = ux + ax * timestepincrement
        vy = uy + ay * timestepincrement
        return vx,vy
    def change_parameters_displacement():
        sx = x + ux * timestepincrement + 0.5 * ax * timestepincrement ** 2
        sy = y + uy * timestepincrement + 0.5 * ay * timestepincrement ** 2
        return sx,sy
    def calc_x_position(t,isDrag):
        if isDrag:
            x = x + ux * timestepincrement + 0.5 * ax * timestepincrement ** 2
            return x
        else:
            x = u * math.cos(angle) * t
            return x
    def calc_y_position(t,isDrag):
        if isDrag:
            y = y + uy * timestepincrement + 0.5 * ay * timestepincrement ** 2
            return y
        else:
            y = h + u * math.sin(angle) * t - 0.5 * g * t**2
            return y
    u,g,h,angle,k = get_info()
    #u = 20
    #g = 5
    #h = 30
    #angle = math.radians(45)
    #k = 0.5 * 0.1 * 1 * 0.01 / 0.1
    t,ux,uy,ax,ay,x,y = define_initial_parameters()
    #non-drag
    x_list = []
    y_list = []
    while y > 0:
        x_list.append(calc_x_position(t,False))
        y_list.append(calc_y_position(t,False))
        t += timestepincrement
        x = calc_x_position(t,False)
        y = calc_y_position(t,False)
    plt.plot(x_list,y_list)

    #drag 
    t,ux,uy,ax,ay,x,y = define_initial_parameters()
    v = u
    x_list = []
    y_list = []
    while y > 0:
        ax,ay = change_parameters_accel()
        x,y = change_parameters_displacement()
        ux,uy = change_parameters_velo()
        v = (ux**2 + uy**2)**0.5
        x_list.append(x)
        y_list.append(y)
    plt.plot(x_list,y_list)
    init_graph("Projectile motion model: u = " + str(u) + " g = " + str(g) + " h = " + str(h) + " angle = " + str(round(math.degrees(angle),2)))
    plt.legend(["No air resistance","Air resistance"])
    plt.show()

    #(ux**2 + uy**2)*0.5
    




#task_one()
#task_two()
#task_three()
#task_four()
#task_five()
#task_six()
#task_seven()
#x_list, y_list, end_point_X, end_point_Y = task_eight(7, 0.001)
task_nine(0.001)
#pygame_setup(1250,800,30,100)
#plt.show()h