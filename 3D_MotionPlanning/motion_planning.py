import argparse
import time
import msgpack
from enum import Enum, auto

import numpy as np

from planning_utils import a_star, heuristic, create_grid, smooth_path
from udacidrone import Drone
from udacidrone.connection import MavlinkConnection
from udacidrone.messaging import MsgID
from udacidrone.frame_utils import global_to_local


class States(Enum):
	MANUAL = auto()
	ARMING = auto()
	TAKEOFF = auto()
	WAYPOINT = auto()
	LANDING = auto()
	DISARMING = auto()
	PLANNING = auto()


class MotionPlanning(Drone):

	def __init__(self, connection):
		super().__init__(connection)

		self.target_position = np.array([0.0, 0.0, 0.0])
		self.waypoints = []
		self.in_mission = True
		self.check_state = {}

		# initial state
		self.flight_state = States.MANUAL

		# register all your callbacks here
		self.register_callback(MsgID.LOCAL_POSITION, self.local_position_callback)
		self.register_callback(MsgID.LOCAL_VELOCITY, self.velocity_callback)
		self.register_callback(MsgID.STATE, self.state_callback)

	def local_position_callback(self):
		if self.flight_state == States.TAKEOFF:
			if -1.0 * self.local_position[2] > 0.95 * self.target_position[2]:
				self.waypoint_transition()
		elif self.flight_state == States.WAYPOINT:
			if np.linalg.norm(self.target_position[0:2] - self.local_position[0:2]) < 1.0:
				if len(self.waypoints) > 0:
					self.waypoint_transition()
				else:
					if np.linalg.norm(self.local_velocity[0:2]) < 1.0:
						self.landing_transition()

	def velocity_callback(self):
		if self.flight_state == States.LANDING:
			if self.global_position[2] - self.global_home[2] < 0.1:
				if abs(self.local_position[2]) < 0.1:
					self.disarming_transition()

	def state_callback(self):
		if self.in_mission:
			if self.flight_state == States.MANUAL:
				self.arming_transition()
			elif self.flight_state == States.ARMING:
				if self.armed:
					self.plan_path()
			elif self.flight_state == States.PLANNING:
				self.takeoff_transition()
			elif self.flight_state == States.DISARMING:
				if ~self.armed & ~self.guided:
					self.manual_transition()

	def arming_transition(self):
		self.flight_state = States.ARMING
		print("arming transition")
		self.arm()
		self.take_control()

	def takeoff_transition(self):
		self.flight_state = States.TAKEOFF
		print("takeoff transition")
		self.takeoff(self.target_position[2])

	def waypoint_transition(self):
		self.flight_state = States.WAYPOINT
		print("waypoint transition")
		self.target_position = self.waypoints.pop(0)
		print('target position', self.target_position)
		self.cmd_position(self.target_position[0], self.target_position[1], self.target_position[2],
self.target_position[3])

	def landing_transition(self):
		self.flight_state = States.LANDING
		print("landing transition")
		self.land()

	def disarming_transition(self):
		self.flight_state = States.DISARMING
		print("disarm transition")
		self.disarm()
		self.release_control()

	def manual_transition(self):
		self.flight_state = States.MANUAL
		print("manual transition")
		self.stop()
		self.in_mission = False

	def send_waypoints(self):
		print("Sending waypoints to simulator ...")
		data = msgpack.dumps(self.waypoints)
		self.connection._master.write(data)

	def plan_path(self):
		self.flight_state = States.PLANNING
		print("Searching for a path ...")
		TARGET_ALTITUDE = 5
		SAFETY_DISTANCE = 5

		self.target_position[2] = TARGET_ALTITUDE

		#read lat0, lon0 from colliders into floating point values
		start_pos_data = np.genfromtxt('colliders.csv', max_rows=1, delimiter=',', dtype='str')

		start_pos_coord = {}

		for coord in start_pos_data:
			coord_split = coord.split()
			start_pos_coord[coord_split[0]] = float(coord_split[1])

		#set home position to (lon0, lat0, 0)
		self.set_home_position(start_pos_coord["lon0"], start_pos_coord["lat0"], 0)
		
		#retrieve current global position
		curr_global_position = self.global_position
		
		#convert to current local position using global_to_local()
		curr_local_position = global_to_local(self.global_position, self.global_home)
		print('global home {0}, position {1}, local position {2}'.format(self.global_home, self.global_position,
																	 self.local_position))
																	 
		print(curr_local_position)
		# Read in obstacle map
		data = np.loadtxt('colliders.csv', delimiter=',', dtype='Float64', skiprows=2)

		# Define a grid for a particular altitude and safety margin around obstacles
		grid, north_offset, east_offset = create_grid(data, TARGET_ALTITUDE, SAFETY_DISTANCE)
		print("North offset = {0}, east offset = {1}".format(north_offset, east_offset))
		
		# Define starting point on the grid (this is just grid center)
		grid_start = (int(curr_local_position[0]-north_offset), int(curr_local_position[1]-east_offset))
		
		# convert start position to current position rather than map center
		random_number = np.random.uniform(0.8, 1.2, 1)
		while grid[int(-north_offset * random_number)][int(-east_offset*random_number)] == 1:
			random_number = np.random.uniform(0.8, 1.2, 1)
		
		# Set goal as some arbitrary position on the grid
		grid_goal = (int(-north_offset * random_number), int(-east_offset*random_number))#(-north_offset + 10, -east_offset + 10)
		# TODO: adapt to set goal as latitude / longitude position and convert

		# Run A* to find a path from start to goal
		print('Local Start and Goal: ', grid_start, grid_goal)
		path, _ = a_star(grid, heuristic, grid_start, grid_goal)
		
		#prune path to minimize number of waypoints
		smoothed_path = smooth_path(path)
		# Convert path to waypoints
		waypoints = [[p[0] + north_offset, p[1] + east_offset, TARGET_ALTITUDE, 0] for p in smoothed_path]
		# Set self.waypoints
		self.waypoints = waypoints
		# send waypoints to sim (this is just for visualization of waypoints)
		self.send_waypoints()

	def start(self):
		self.start_log("Logs", "NavLog.txt")

		print("starting connection")
		self.connection.start()

		# Only required if they do threaded
		# while self.in_mission:
		#    pass

		self.stop_log()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--port', type=int, default=5760, help='Port number')
	parser.add_argument('--host', type=str, default='127.0.0.1', help="host address, i.e. '127.0.0.1'")
	args = parser.parse_args()

	conn = MavlinkConnection('tcp:{0}:{1}'.format(args.host, args.port), timeout=60)
	drone = MotionPlanning(conn)
	time.sleep(1)

	drone.start()
