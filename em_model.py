import math as m
import random as r
import numpy as np
import pandas as pd
import  matplotlib.pyplot as plt

GLOBAL_STAR_POS=0
GLOBAL_STAR_RAD=56
GLOBAL_SQUARE_SIDE=10
GLOBAL_PLANET_RAD=6

def make_square_structure(local_planet_offset):
    bottom_left_x_square=GLOBAL_STAR_POS-GLOBAL_STAR_RAD-GLOBAL_SQUARE_SIDE
    bottom_left_y_square=GLOBAL_STAR_POS-(1/2*GLOBAL_SQUARE_SIDE)
    xvalues=[]
    yvalues=[]
    for x in range(bottom_left_x_square+local_planet_offset,bottom_left_x_square+GLOBAL_SQUARE_SIDE+local_planet_offset):
        for y in range(bottom_left_y_square,bottom_left_y_square+GLOBAL_SQUARE_SIDE):
                xvalues.append(x)
                yvalues.append(y)
    return pd.DataFrame({'x':xvalues,'y':yvalues})


def make_control_object(planet_offset):
    xvalues=[]
    yvalues=[]
    
    center=GLOBAL_STAR_POS-GLOBAL_STAR_RAD-GLOBAL_PLANET_RAD+planet_offset
    
    for startx in range(center-GLOBAL_PLANET_RAD,center+GLOBAL_PLANET_RAD):
        for starty in range(-GLOBAL_PLANET_RAD,+GLOBAL_PLANET_RAD):
            sum_of_sqrs=(startx-center)**2+(starty)**2
            if (sum_of_sqrs**.5)<GLOBAL_PLANET_RAD:
                xvalues.append(startx)
                yvalues.append(starty)
    return pd.DataFrame({'x':xvalues,'y':yvalues})
                
def make_star():
    index=0
    xvalues=[]
    yvalues=[]
    ivalues=[]
    psi=-90 #starting point of arc sweep
    for startx in range(GLOBAL_STAR_POS-GLOBAL_STAR_RAD,GLOBAL_STAR_POS+GLOBAL_STAR_RAD):
        psi= -90+(float(index)/(2*float(GLOBAL_STAR_RAD)))*180 #we sweep from -90 to +90 using 2r increments
        psi=psi*m.pi/180
        
        index+=1
        intensity=.4 +.6*m.cos(psi)       #limb darkening model
        #intensity=1   #uncomment this to switch to uniform luminosity

        for starty in range(-GLOBAL_STAR_RAD,+GLOBAL_STAR_RAD):
            sum_of_sqrs=(startx-GLOBAL_STAR_POS)**2+(starty)**2
            if (sum_of_sqrs**.5)<GLOBAL_STAR_RAD:
                xvalues.append(startx)
                yvalues.append(starty)
                ivalues.append(intensity)
    return pd.DataFrame({'x':xvalues,'y':yvalues, 'z':ivalues})
    
def file_write(file_string,data_to_write):
    #write lightcurve to file
    file=open(file_string,'w')
        
    for file_counter in range(0,len(data_to_write)):
        data=str(data_to_write[file_counter])
        file.write(data[2:6]+','+'\n')
    file.close()

def main():

    START_PLANET_POS=0
    END_PLANET_POS=115
    
    star_df=make_star()       #place star at a fixed point
    star_luminosity=star_df['z'].sum()       #sum all star lum
                                
    lumarray=np.empty([END_PLANET_POS-START_PLANET_POS,1])
    
    for planet_offset in range(START_PLANET_POS,END_PLANET_POS):      #loop moving structure accross the star        
    
        planet_df=make_square_structure(planet_offset)           #comment/uncomment out one of these two lines to place either control object or square structure
        #planet_df=make_control_object(planet_offset)            #comment/uncomment out one of these two lines to place either control object or square structure
        
        intersection_df=pd.merge(planet_df, star_df, on=['x', 'y'], how='inner') #find intersection points
        intersection_lum_array=intersection_df['z']
        visible_luminosity=star_luminosity-sum(intersection_lum_array)  #light shining through is total starlight - occluded light
        lumarray[planet_offset]=visible_luminosity    
        
    file_write('lightcurvedata.csv',lumarray)   
        
if __name__ == "__main__":
    main()
