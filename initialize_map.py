import os # pause
import numpy # math
import random # random numbers
import time #sleep

class Tile:
        
  def __init__(self, name, front, passable):
    self.name = name
    self.front = front
    self.passable = passable
    
class Player:
        
  def __init__(self, name, front, x, y):
    self.name = name
    self.front = front
    self.x = x
    self.y = y
    
class Building:
        
  def __init__(self, name, front, size_x, size_y):
    self.name = name
    self.front = front
    self.size_x = size_x
    self.size_y = size_y
    self.tiles = self.randomize_building(size_x, size_y)
  
  def randomize_building(cls, building_size_x, building_size_y):
    empty_floor = Tile("floor", ".", True)
    door = Tile("door", "D", True)
    wall_horizontal = Tile("wall", "═", False)
    wall_vertical = Tile("wall", "║", False)
    corner_left_top = Tile("wall", "╔", False)
    corner_left_bottom = Tile("wall", "╚", False)
    corner_right_top = Tile("wall", "╗", False)
    corner_right_bottom = Tile("wall", "╝", False)

    building_array = [[empty_floor for col in range(building_size_x)] for row in range(building_size_y)]

    building_array[0] = [wall_horizontal] * building_size_x
    building_array[building_size_y - 1] = [wall_horizontal] * building_size_x
    
    for y in range(building_size_y - 2 ):
      building_array[y + 1][0] = wall_vertical
      building_array[y + 1][building_size_x - 1] = wall_vertical
      
    building_array[0][0] = corner_left_top
    building_array[0][building_size_x - 1] = corner_right_top
    building_array[building_size_y - 1][0] = corner_left_bottom
    building_array[building_size_y - 1][building_size_x - 1] = corner_right_bottom

    doorable_walls = [[random.randint(1, building_size_x - 2),0],[random.randint(1, building_size_x - 2),building_size_y - 1],[0, random.randint(1, building_size_y - 2)],[building_size_x - 1, random.randint(1, building_size_y - 2)]]
    number_of_doors = random.randint(1,3)
    
    for d in range(number_of_doors):
      wall_with_door = random.choice(doorable_walls)
      building_array[wall_with_door[1]][wall_with_door[0]] = door
    
    return building_array     
    
def initialize_map(screen_size_x,screen_size_y):  
  print("....Creating map.....")
  time.sleep(0.5)
  
  empty_tile = Tile("grass", " ", True)

  map_array = [[empty_tile for col in range(screen_size_x)] for row in range(screen_size_y)]
  
  return map_array
  
def add_map_boundaries(map_array, screen_size_x, screen_size_y):
  print("....Adding walls.....")
  time.sleep(0.1)
  
  wall_horizontal = Tile("wall", "═", False)
  wall_vertical = Tile("wall", "║", False)
  corner_left_top = Tile("wall", "╔", False)
  corner_left_bottom = Tile("wall", "╚", False)
  corner_right_top = Tile("wall", "╗", False)
  corner_right_bottom = Tile("wall", "╝", False)
  
  map_array[0] = [wall_horizontal] * screen_size_x
  map_array[screen_size_y - 1] = [wall_horizontal] * screen_size_x
  
  for y in range(screen_size_y - 2 ):
    map_array[y + 1][0] = wall_vertical
    map_array[y + 1][screen_size_x - 1] = wall_vertical
    
  map_array[0][0] = corner_left_top
  map_array[0][screen_size_x - 1] = corner_right_top
  map_array[screen_size_y - 1][0] = corner_left_bottom
  map_array[screen_size_y - 1][screen_size_x - 1] = corner_right_bottom

  return map_array
  
def spill_lakes(map_array, screen_size_x, screen_size_y, number_of_lakes, lake_size, lake_density):
  print("....Spilling lakes...")
  time.sleep(0.1)    
  
  lake_tile = Tile("water", "≈", False)
 
  for lake in range(number_of_lakes):
    lake_x = random.randint(2, (screen_size_x - lake_size) - 2)
    lake_y = random.randint(2, (screen_size_y - lake_size) - 2)
    
    for tile in range(lake_density):
       x = int(random.gauss(lake_size, lake_density/100)) + lake_x - int(lake_size/2)
       y = int(random.gauss(lake_size, lake_density/100)) + lake_y - int(lake_size/2)
       map_array[y][x] = lake_tile

  return map_array
 
def seed_bushes(map_array, screen_size_x, screen_size_y, number_of_bushes, bush_length):
  print("....Seeding bushes...")
  time.sleep(0.1)    
  
  bush_tile = Tile("bush", "#", False)
  bush_spread = [-1,0,0,0,0,1]
 
  for bush_source in range(number_of_bushes):
    bush_x = random.randint(2, (screen_size_x - 3))
    bush_y = random.randint(2, (screen_size_y - 3))
    
    horizontal = bool(random.getrandbits(1))
    
    if (horizontal == True):
      for bush in range(bush_length):
        x = int(random.gauss(bush_length, 1) + bush_x - bush_length)
        y = bush_y + random.choice(bush_spread)
        
        if map_array[y][x].passable == True:
          map_array[y][x] = bush_tile 
    else:
      for bush in range(bush_length):
        y = int(random.gauss(bush_length, 1) + bush_y - bush_length)
        x = bush_x + random.choice(bush_spread)
        
        if map_array[y][x].passable == True:
          map_array[y][x] = bush_tile 
            
  return map_array  
  
def plant_trees(map_array, screen_size_x, screen_size_y, number_of_trees):
  print("....Planting trees...")
  time.sleep(0.1)
  
  tree_tile = Tile("tree", "♣", False)
 
  for tree in range(number_of_trees):
    x = random.randint(2, screen_size_x - 2)
    y = random.randint(2, screen_size_y - 2)
    
    if map_array[y][x].passable == True:
      map_array[y][x] = tree_tile
  
  return map_array

def construct_buildings(map_array, screen_size_x, screen_size_y, number_of_buildings, min_building_size, max_building_size):

  print("....Making buildings.....")
  time.sleep(0.1)
 
  for construction in range(number_of_buildings):
    building_width = random.randint(min_building_size,max_building_size)
    building_height = random.randint(min_building_size,max_building_size)
    
    building_x = random.randint(2, screen_size_x - building_width - 1)
    building_y = random.randint(2, screen_size_y - building_height - 1)

    building = Building("Home","H",building_width,building_height).tiles
    for y in range(building_height):
      for x in range(building_width):
        map_array[building_y + y][building_x + x] = building[y][x]


  return map_array

def show_generated_map(map_array, screen_size_x, screen_size_y):
  final_map = ""
  
  for y in range(screen_size_y):
    front_tiles = []
    for node in map_array[y]:
      front_tiles.append(node.front)
     
    row = "".join(front_tiles)
    final_map = final_map + row + "\n"
    
  print(final_map)

def show_map_statistics(map_array):
  counted_objects = (count_objects(map_array))
  
  print("Generated objects:")
  
  for object_key, object_value in counted_objects.items():
    print(object_key, " ",object_value)

  programPause = input("Press the any key to start")

def spawn_player(map_array, screen_size_x, screen_size_y):
  while True:
    player_x = random.randint(2, screen_size_x - 2)
    player_y = random.randint(2, screen_size_y - 2)
    if map_array[player_y][player_x].passable == True:
        break
        
  return Player("vinne","V", player_x, player_y)
  
def update_map(temp_map, screen_size_x, screen_size_y, player):
  temp_map[player.y][player.x] = player  
  
  final_map = ""
  
  for y in range(screen_size_y):
    front_tiles = []
    for node in temp_map[y]:
      front_tiles.append(node.front)
     
    row = "".join(front_tiles)
    final_map = final_map + row + "\n"
  
  
  os.system('cls')
  print(final_map)

def count_objects(map_array):
  # objects [grass, tree, bush, water, wall]
  objects = {
    "grass": 0,
    "trees": 0,
    "bushes": 0,
    "water": 0,
    "walls": 0
  }
  
  for row in map_array:
    for cell in row:
      name = cell.name
      if name == "grass":
        objects["grass"] += 1
      elif name == "tree":
        objects["trees"] += 1
      elif name == "bush":
        objects["bushes"] += 1
      elif name == "water":
        objects["water"] += 1
      elif name == "wall":
        objects["walls"] += 1
 
  return objects

def copy_matrix(matrix):
  return [row[:] for row in matrix]

def move_player(map_array, player):
  direction = ""
  direction = input("move 'w' 's' 'a' 'd', get info by adding .info or quit: ")

  if direction == "w":
    if map_array[player.y - 1][player.x].passable == True:
      player.y = player.y - 1
    else:
      player.y = player.y
  elif direction == "s":
    if map_array[player.y + 1][player.x].passable == True:
      player.y = player.y + 1
    else:
      player.y = player.y    
  elif direction == "a":
    if map_array[player.y][player.x - 1].passable == True:
      player.x = player.x - 1
    else:
      player.x = player.x    
  elif direction == "d":
    if map_array[player.y][player.x + 1].passable == True:
      player.x = player.x + 1
    else:
      player.x = player.x
  elif direction == "w.info":
    information = "You are looking at " + str(map_array[player.y - 1][player.x].name)
    input(information)
  elif direction == "s.info":
    information = "You are looking at " + str(map_array[player.y + 1][player.x].name)
    input(information)
  elif direction == "a.info":
    information = "You are looking at " + str(map_array[player.y][player.x - 1].name)
    input(information)
  elif direction == "d.info":
    information = "You are looking at " + str(map_array[player.y][player.x + 1].name)
    input(information)   
  #elif direction == "quit":
    # add global variable and use it in while
    
## ======================= main program start =========================
## ========================== generate map ============================
screen_size_x = 60
screen_size_y = 22

number_of_lakes = 7
lake_size = 10
lake_density = 75
number_of_bushes = 12
bush_length = 15
number_of_trees = 250
number_of_buildings = 2
min_building_size = 4
max_building_size = 8

map_array = initialize_map(screen_size_x, screen_size_y)
map_array = add_map_boundaries(map_array, screen_size_x, screen_size_y)
map_array = spill_lakes(map_array, screen_size_x, screen_size_y, number_of_lakes, lake_size, lake_density)
map_array = seed_bushes(map_array, screen_size_x, screen_size_y, number_of_bushes, bush_length)
map_array = plant_trees(map_array, screen_size_x, screen_size_y, number_of_trees)
map_array = construct_buildings(map_array, screen_size_x, screen_size_y, number_of_buildings, min_building_size, max_building_size)


show_generated_map(map_array, screen_size_x, screen_size_y)
show_map_statistics(map_array)

temp_map = copy_matrix(map_array)

player = spawn_player(temp_map, screen_size_x, screen_size_y)



while True:
  temp_map = copy_matrix(map_array)
  
  update_map(temp_map, screen_size_x, screen_size_y, player)
  move_player(map_array, player)