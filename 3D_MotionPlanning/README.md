3D Motion Planning Project

Remarks:
•	Due to some rendering problem, that when starting the simulator the drone start location is inside a building, I was not able to test some other algorithms other than the basic one required for the submission. The only workaround that worked was pressing shift+R couple of times and then all the buildings disappeared and that was the only way to get the drone to move from its initial position without collapsing and flipping down to the ground. In addition I tried to check if this problem was fixed in any other release, but I could not find anything. So please if there is a solution to this problem let me know and I will resubmit the project maybe with some new implementations of some other algorithms that I have learned in this amazing course   Thanks in advance!

The following points are the answers to the Project Rubric points:

•	Explain the starter code.
o	The main difference is that in backyard_flyer, the drone was programmed to fly at a certain altitude and then fly through 4 points that form a square. However in motion_planning.py is kind of the same except that this time a list of obstacles is imported with some safety margin north and east. In addition a path through these obstacles is planned using a_star algorithm and drone is flying along that path in a zigzag motion. The zigzag motion is due to the fact that the path is planned through a grid with no diagonal movement is allowed.

•	Implementation of the Path Planning Algorithm
o	The home position coordination are read from colliders.csv file using genfromtxt() function from numpy and with the help of some string manipulation methods, the values are collected and stored in dictionary with their corresponding names lat0, and lon0
o	The home global coordinates were converted to local position using global_to_local() function and then set as home position of the drone.
o	grid_start is set to be the current location of the drone
o	grid_goal is chosen to be at a random position from the center of the map, north offset and east offset. Each time the motion_planning is started, the algorithm generates a random location within a given range of the center of the map and checks if it does not collide with an obstacle and set it as a grid_goal and with grid_start both will be given to the a_start function to search for the path.
o	The Action enum class was provided with more actions, as in diagonal movement with cost of srqt(2).
o	For smoothing the path, collinearity check was used for removing collinear nodes on the path.




•	Executing the flight.
o	The picture provided is a screenshot of the simulator after the drone successfully executed 2 paths. This picture alse shows the problem mentioned in the remarks at the beginning, the disappearing of the buildings after resetting the scene. 
 
![image](https://user-images.githubusercontent.com/57869923/111068282-72d7c100-84c8-11eb-9e9b-1755f98ede02.png)
