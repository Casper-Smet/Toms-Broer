from AStar import *

startpunt = eval(input("Startpunt =  (y,x)   "))
eindpunt = eval(input("Eindpunt =    (y,x)  "))

path = dmain(startpunt, eindpunt)

print(path)
