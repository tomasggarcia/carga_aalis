import random
import mysql.connector
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="paraguay"
)

mycursor = mydb.cursor()

# mycursor.execute("SELECT distrito_id FROM distritos where distrito_nombre='Asunción' ")
# myresult = mycursor.fetchall()
# for x in myresult:
#   print(x)


# Add aali
def add_aali(table,aali_value,row_name):
    sql = f"""UPDATE {table}s SET aali = {aali_value} WHERE  {table}_nombre="{row_name}" """
    mycursor.execute(sql)
    mydb.commit()
    print(mycursor.rowcount, "record(s) affected")

def find_aali_id(table,value):
    mycursor.execute(f"SELECT {table}_id FROM {table}s where {table}_nombre='{value}' ")
    myresult = mycursor.fetchall()
    return myresult[0][0]


def random_inside_coord(coord_list):
    x_min = coord_list[0][0]
    x_max = coord_list[0][0]
    y_min = coord_list[0][1]
    y_max = coord_list[0][1]
    for coor in coord_list:
        if coor[0] < x_min: x_min = coor[0] 
        if coor[0] > x_max: x_max = coor[0] 
        if coor[1] < y_min: y_min = coor[1] 
        if coor[1] > y_max: y_max = coor[1] 
    random_point = (random.uniform(x_min,x_max)),(random.uniform(y_min,y_max))
    # print('aca',random_point)
    point = Point(random_point)
    polygon = Polygon(coord_list)
    if polygon.contains(point) == True:
        return random_point
    return random_inside_coord(coord_list)

def select_inside_coord(distrito_name):
    mycursor.execute(f"""SELECT ST_AsText(geom) FROM distritos where distrito_nombre="{distrito_name}" """)
    myresult = mycursor.fetchall()
    coordinates_array= myresult[0][0][9:-2].split(',')
    tuple_list = []
    for coordinate in coordinates_array:
        tuple_list.append(tuple([float(coordinate.split(' ')[0]),float(coordinate.split(' ')[1])]))
    coor = random_inside_coord(tuple_list)
    return coor

def select_all_coordinates(distrito_name):
    mycursor.execute(f"SELECT ST_AsText(geom) FROM departamentos where departamento_nombre='{distrito_name}' ")
    myresult = mycursor.fetchall()
    coordinates_array= myresult[0][0][9:-2].split(',')
    tuple_list = []
    for coordinate in coordinates_array:
        tuple_list.append(tuple([float(coordinate.split(' ')[0]),float(coordinate.split(' ')[1])]))
    return tuple_list


def is_in_aali(int_coor, ext_list_coordinates):
    for coor in int_coor:
        if coor not in ext_list_coordinates:
            point = Point(int_coor)
            polygon = Polygon(ext_list_coordinates)
            if polygon.contains(point) == False:
                return False
    return True


def select_all_aali(aali):
    all_departamentos = []
    mycursor.execute(f"SELECT {aali}_nombre FROM {aali}s")
    myresult = mycursor.fetchall()
    for departamento in myresult:
      all_departamentos.append(departamento[0])
    return all_departamentos


departamentos = select_all_aali('departamento')
distritos = select_all_aali('distrito')

for depto in departamentos:
    for dist in distritos:
        distrito_coordinates = select_inside_coord(dist)      
        departamentos_coordinates = select_all_coordinates(depto)
        if is_in_aali(distrito_coordinates,departamentos_coordinates) == True:
            # agregar al distrito  
            
            print(depto, dist)
            add_aali('distrito',find_aali_id('departamento',depto),dist)
