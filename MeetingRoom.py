
#!/usr/bin/python

import datetime
import sys
import re

'''
Solution class for Meeting room reservation system
'''

class Solution:

	def __init__(self):

		#meeting room
		self.number_of_rooms = 2
		self.list_of_rooms = [{} for i in range(self.number_of_rooms)]
		self.booked = [False] * self.number_of_rooms

		#set of constant time variables
		self.scheduler_starttime = datetime.datetime(2000,1,1,9,0,0)
		self.scheduler_endtime = datetime.datetime(2000,1,1,17,0,0)
		self.lunch_starttime = datetime.datetime(2000,1,1,12,0,0)
		self.lunch_endtime = datetime.datetime(2000,1,1,13,0,0)

		#schedule manipulator for each room
		self.scheduler_current_times = [self.scheduler_starttime] * self.number_of_rooms

	'''
	Function to add new events to the schedule for each meeting room.
	'''
	def add_event(self, event_title, event_duration, room):

		#check if tentative schedule time meets the constraint of core work hours
		tentative_time = self.scheduler_current_times[room] + datetime.timedelta(minutes=event_duration)
		if( tentative_time <= self.scheduler_endtime ):

			#check for lunch time constraint
			if(self.scheduler_current_times[room] <= self.lunch_starttime and tentative_time > self.lunch_starttime):
				self.list_of_rooms[room][self.lunch_starttime.time()] = "Lunch"
				self.scheduler_current_times[room] = self.lunch_endtime 

			#add the schedule to dictionary of the meeting room
			self.list_of_rooms[room][self.scheduler_current_times[room].time()] = event_title + " " + str(event_duration) +" "+ "mins"
			self.scheduler_current_times[room] = self.scheduler_current_times[room] + datetime.timedelta(minutes=event_duration)

		#else check if other room has slots to reserve
		else:
			self.booked[room] = True
			if False in self.booked:
				room = 1 - room
				self.add_event(event_title,event_duration,room)
			else:
				#No free slot to allot the new meeting.
				print "Meeting timing out of office hours or All rooms booked."
				self.print_complete_schedule()

	'''
	Print final schedule for each meeting room.
	'''

	def print_complete_schedule(self):

		print "\nMeeting room schedule: "
		for room in xrange(self.number_of_rooms):
			print "Room", room+1 , "schedule:"
			for k in sorted(self.list_of_rooms[room].keys()):
				print k, self.list_of_rooms[room][k]
			print ""
		sys.exit(0)

	'''
	Function to accept input from console and process each meeting one line at a time.
	'''
	def process_input(self):

		room = 0
		print "Enter the meeting details as <title_without_space> <space> <duration_in_minutes> or 'done/exit' to print schedule:"

		#Exit loop based on input from user
		while(True):
			row = raw_input("Enter input:")
			if (row.lower() == 'done'):
				#exit loop
				break
			else:
				#process input line to reserve the meeting room
				try:
					tmp = row.split()
					if(len(tmp) > 1):
						#join words composing the meeting title and stripping aplhabets from the duration (if any)
						self.add_event(" ".join(tmp[:-1]),int(filter(str.isdigit, tmp[-1])),room)
						room = 1 - room
					else:
						raise IndexError
				except ValueError:
					print "Invalid duration. ",
					print "<title> <space> <duration_in_mins> "
				except :
					print "Invalid format. ",
					print "<title> <space> <duration_in_mins> "

 
'''
Main Function
'''
def main():
	scheduler = Solution()
	scheduler.process_input()
	scheduler.print_complete_schedule()


if __name__ == '__main__':
 	main()


