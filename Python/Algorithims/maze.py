import curses  
from curses import wrapper 
import queue 
import time 

maze = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]

def print_maze(maze, stdscr, path=[]): 
  BLUE = curses.color_pair(1)
  RED = curses.color_pair(2)


  for i, row in enumerate(maze): #Enumerate gives the index and the value of the rows. 
    for j, value in enumerate(row): #Enumerates over row and grabs the values of the column. 
        if (i, j) in path: 
           stdscr.addstr(i, j*2, "X", RED)
        else: 
          stdscr.addstr(i, j*2, value, BLUE)



def find_start(maze, start): 
   for i, row in enumerate(maze): 
      for j, value in enumerate(row): 
         if value == start: 
            return i, j
         
      return None

def find_path(maze, stdscr): 
   start = "O"
   end = "X"
   start_pos = find_start(maze, start)

   q =  queue.Queue() #First in, first out data structure. An example of this would be phone calls, one would naturally accept the oldest call before the most recent. 
   q.put((start_pos, [start_pos])) #Tuple that contains starting position and a list that contains the starting position as well. This is done to keep track of the current node being processed in the queue as well as the path to get to that node. This allows the path to be easily displayed as well. 

   visited = set() #Contains all the positions that have been visited. 

   while not q.empty():  #When the queue is not empty the most recent element will be grabbed, the one next in queue
      current_pos, path = q.get()
      row, col = current_pos 

      stdscr.clear() #clears entire screen. 
      print_maze(maze, stdscr, path) #Prints the maze and the path every while loop. 
      time.sleep(0.5)
      stdscr.refresh() #Refreshes screen

      if maze[row][col] == end: 
         return path 
      
      adjacents = find_adjacent(maze, row, col) #Checks for obstacles and already processed values. 
      for adjacent in adjacents: 
         if adjacent in visited: #If adjacent is in the set "visited" the algorithm will continue  
            continue 
         
         r, c = adjacent #Both R and C are used to prevent clashes between variable names.
         if maze[r][c] == "#": #If "#" the Obstacle is found, continue the search. 
            continue 
         
         new_path = path + [adjacent] #Adds adjacent node to the current path, not the most efficent way but simple. 
         q.put((adjacent, new_path))
         visited.add(adjacent)
         
         
      
def find_adjacent(maze, row, col): 
   adjacents = []

   if row > 0: #Checks if there is an adjacent value above. 
      adjacents.append((row -1, col))

   if row + 1 < len(maze): #Checks if there is an adjacent below. Len is a simple way to establish bounds without error. 
      adjacents.append((row +1, col))

   if col > 0: #Left 
      adjacents.append((row, col - 1))

   if col + 1 < len(maze[0]): #Right 
      adjacents.append((row, col + 1))

      return adjacents

def main(stdscr): #standard outupt screen 
  curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
  curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

  find_path(maze, stdscr)
  stdscr.getch() #Waits until a user makes an input before exiting the program. 


wrapper(main) #initializes the curses moduel and the calls the function which parses the stdscreen object. This allows us to control the output. 
