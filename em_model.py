import  math as m;
import numpy as np;
import matplotlib.pyplot as plt;


sun_pos=0;sun_rad=50;
square_side=13;

bottom_left_x_square=sun_pos-sun_rad-square_side;
bottom_left_y_square=sun_pos-(1/2*square_side);

triangle_side=5;


def make_square_planet(Planet_set):
    for x in range(bottom_left_x_square+planet_offset,bottom_left_x_square+square_side+planet_offset):
        for y in range(bottom_left_y_square,bottom_left_y_square+square_side):
            elem=str(x) + ',' + str(y)
            Planet_set.add(elem)


def make_circle(local_Set,center,radius):
    elem=[];
    for startx in range(center-radius,center+radius):
        for starty in range(-radius,+radius):
            sum_of_sqrs=(startx-center)**2+(starty)**2;
            if (sum_of_sqrs**.5)<radius:
                elem=str(startx) + ',' + str(starty)
                local_Set.add(elem)
                
def plot_circle(local_set):

    n=0
    s1=np.empty([len(local_set),1])
    s2=np.empty([len(local_set),1])
    
    for item in set(local_set):
        s1[n],s2[n]=item.split(",")
        n=n+1
    plt.scatter(s1,s2)
    plt.show()

#populate sun with points

sun=[]


        
#make sun
Circle_set=set()
make_circle(Circle_set,sun_pos,sun_rad)
plot_circle(Circle_set)    

#big loop moving planet accross the sun        
                        
start_planet_pos=0
end_planet_pos=106
lumarray=np.empty([end_planet_pos-start_planet_pos,1])
for planet_offset in range(start_planet_pos,end_planet_pos):

    Planet_set=set()
    
    #place planet
    #make_square_planet(Planet_set)
    planet_rad=8;
    make_circle(Planet_set,sun_pos-sun_rad-planet_rad+planet_offset,planet_rad)
    
    #luminosity = total sun points - intersection points
    intersection_points=Circle_set.intersection(Planet_set)
    lum=len(Circle_set)-len(intersection_points)
    lumarray[planet_offset]=lum    
    
import timeit
start_time = timeit.default_timer()
# code you want to evaluate    
elapsed = timeit.default_timer() - start_time


file=open('output.csv','w')

for file_counter in range(0,len(lumarray)):
    data=str(lumarray[file_counter])
    file.write(data[2:6]+','+'\n')
file.close()
