import numpy as np
import math

class Calculation:
    def __init__(self, input_data, crystal, array_index):
        self.matrix = input_data
        self.crystal = crystal
        self.array_index = array_index

    def insert_vertex_in_crystal(self, vertex, x, y):
        self.crystal[y][x] = vertex+1
        self.array_index[vertex] = None

        return self.array_index

    def connectivity_coef(self, vertex):
        if(vertex):
            vertexes = [int(item) - 1 for row in self.crystal for item in row if item != 0]
            sum_of_placed = self.matrix[vertex][vertexes].sum()
            result = 2*sum_of_placed - self.matrix[vertex].sum()
        else:
            result = None

        return result

    def get_list_of_min(self, list_):
        result = list()

        max_ = max([i for i in list_ if i != None])
        for i, item in enumerate(list_):
            if item == max_:
                result.append(i)

        return result

    def get_distance(self, vertex1, vertex2):
        return math.sqrt((vertex1[0] - vertex2[0])**2 + (vertex1[1] - vertex2[1])**2)

    def get_distance_between_vertexes(self, vertex1, vertex2):
        coordinates = list()

        for y, row in enumerate(self.crystal):
            for x, item in enumerate(row):
                if ((vertex1 == item or vertex2 == item)):
                    coordinates.append((x, y))

        return self.get_distance(coordinates[0], coordinates[1])

    def vector_of_places(self):
        places = list()

        for y,row in enumerate(self.crystal):
            for x,item in enumerate(row):
                    distance = self.get_distance((0,0),(x,y))
                    places.append((x,y,distance))
        places = sorted(places, key=lambda x: x[2])
        places = [coordinates[:-1] for coordinates in places]

        return places

    def len_of_initial_index_array(self, array):
        result = 0

        for item in array:
            if(item):
                result += 1

        return result

    def Q_function(self):
        result = 0

        for row1 in self.crystal:
            for vertex1 in row1:
                for row2 in self.crystal:
                    for vertex2 in row2:
                        if(vertex1 == vertex2):
                            continue
                        result += self.get_distance_between_vertexes(vertex1, vertex2) * \
                                  self.matrix[int(vertex1) - 1][int(vertex2) - 1]

        return math.ceil(result/2)

    def L_function(self, vertex1):
        result = sum([self.matrix[int(vertex1) - 1][int(vertex2) - 1] * self.get_distance_between_vertexes(vertex1, vertex2) \
                    for row in self.crystal for vertex2 in row if vertex2 != vertex1])

        return result / self.matrix[int(vertex1) - 1].sum()

    def get_x_coord(self, vertex):
        for row in self.crystal:
            for x,item in enumerate(row):
                if item == vertex:
                    return x

    def get_y_coord(self, vertex):
        for y,row in enumerate(self.crystal):
            for item in row:
                if item == vertex:
                    return y

    def centre_of_mass(self, vertex1):
        xc = sum([self.matrix[vertex1][vertex2] * self.get_x_coord(vertex2+1) for vertex2 in range(self.matrix.shape[0])]) \
                  / self.matrix[vertex1].sum()
        yc = sum([self.matrix[vertex1][vertex2] * self.get_y_coord(vertex2+1) for vertex2 in range(self.matrix.shape[0])]) \
                  / self.matrix[vertex1].sum()

        return (xc,yc)

    def get_near_vertexes(self, xc, yc):
        xc1 = int(xc - (xc - int(xc)))
        xc2 = xc1 + 1
        yc1 = int(yc - (yc - int(yc)))
        yc2 = yc1 + 1

        vertices = []
        rang = self.crystal.shape[0]

        if xc1 >= 0 and yc1 >= 0:
            vertices.append(self.crystal[yc1][xc1] - 1)
        if xc1 >= 0 and yc2 <= rang:
            vertices.append(self.crystal[yc1][xc2] - 1)
        if xc2 <= rang and yc1 >= 0:
            vertices.append(self.crystal[yc2][xc1] - 1)
        if xc2 <= rang and yc2 <= rang:
            vertices.append(self.crystal[yc2][xc2] - 1)

        return vertices

    def swap_vertices(self, vertex1, vertex2):
        (x1,y1) = (self.get_x_coord(vertex1), self.get_y_coord(vertex1))
        (x2,y2) = (self.get_x_coord(vertex2), self.get_y_coord(vertex2))

        self.crystal[y1][x1], self.crystal[y2][x2] = self.crystal[y2][x2], self.crystal[y1][x1]

        return self.crystal