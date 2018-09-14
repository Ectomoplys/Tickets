import cPickle as pickle
import atexit
import os.path
 
project_list = []
FILE = 'project.txt'

class Ticket(object):
	def __init__(self, title, description, priority):
		self.title = title
		self.description = description
		self.priority = priority
 
	def close(self):
		self.isOpen = False

	def open(self):
		self.isOpen = True
 
class Project(object): 
	def __init__(self, title):
		self.tickets = []
		self.title = title
		project_list.append(self)
 
	def add_ticket(self, ticket):
		self.tickets.append(ticket)
       
def main():
	atexit.register(exit_handler)

	if (os.path.isfile(FILE)):
		load_projects()
	else:
		f = open(FILE, 'w+')
		f.close()
    
	print('\nYou have {0} projects open'.format(len(project_list)))
	print('You have {0} tickets open'.format(ticket_count()))
	
	while True:
		user_input = input('''\nWhat would you like to do?
	1. Add a project
	2. Remove a project
	3. Edit a project
	4. Add a ticket
	5. Remove a ticket
	6. Edit a ticket
	7. Delete all projects and tickets
	8. View open tickets
	9. View open projects
	0. Quit\n''')

		if user_input == 1:
			add_project()
		elif user_input == 4:
			add_ticket()
		elif user_input == 7:
			confirm = raw_input('Are you sure? (yes/no) ')
			if confirm.lower() == 'yes':
				del project_list[:]
		elif user_input == 8:
			view_tickets()
		elif user_input == 9:
			list_projects()
		elif user_input == 0:
			break

def list_projects():
	global project_list
	count = 0

	for project in project_list:
		print('\t{0} {1}'.format(count, project.title))
		count += 1

def add_project():
	title = raw_input('project name: ')

	project = Project(title)

	print('Number of projects in database: {0}\n'.format(len(project_list)))

def add_ticket():
	list_projects()

	user_input = input('which project is the ticket for? ')
	project = project_list[user_input]

	title = raw_input('title: ')
	description = raw_input('description: ')
	priority = raw_input('priority (high, med, low): ')

	ticket = Ticket(title, description, priority)

	project.add_ticket(ticket)

def ticket_count():
	count = 0
	global project_list

	for project in project_list:
		count += len(project.tickets)

	return count
 
def save_projects():
	with open(FILE, 'wb') as fp:
		pickle.dump(project_list, fp)
               
def load_projects():
	with open(FILE, 'rb') as fp:
		global project_list
		project_list = pickle.load(fp)

def view_tickets():
	for project in project_list:
		print(project.title)

		for ticket in project.tickets:
			print('\t{0}'.format(ticket.title))
 
def exit_handler():
	print('saving projects...')
	save_projects()
	print('projects saved')
	print('exiting...')
 
if __name__ == '__main__':
	main()