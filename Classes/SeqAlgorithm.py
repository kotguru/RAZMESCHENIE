import numpy as np
from Classes.Calculation import Calculation


class SequentialAlgorithm:
    def __init__(self, input_data, crystal):
        self.data = input_data
        self.array_index = list(range(self.data.shape[0]))
        self.crystal = crystal
        self.calculation = Calculation(self.data, self.crystal, self.array_index)
    
    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, input_data):
        assert isinstance(input_data, np.ndarray), "Invalid input data. Must be Numpy array"
        assert input_data.ndim == 2, "Invalid rang of matrix. Must be 2"
        assert input_data.shape[0] == input_data.shape[1], "Matrix must be quadratic"

        self.__data = input_data
    
    @property
    def crystal(self):
        return self.__crystal
    
    @crystal.setter
    def crystal(self, crystal):
        assert isinstance(crystal, np.ndarray), "Invalid type of crystal data. Must be Numpy Array"
        assert crystal.ndim == 2, "Invalid rang of crystal matrix. Must be 2"
        assert crystal.shape[0] * crystal.shape[1] == self.data.shape[0], "Invalid number of vertexes. Must be as initial matrix len"
        
        self.__crystal = crystal
    
    def start_seq(self):
        index = 0
        x,y = (0,0)
        initial_vertex = (index, x, y)

        self.array_index = self.calculation.insert_vertex_in_crystal(*initial_vertex)
        vector_of_places = self.calculation.vector_of_places()
        vector_of_places.pop(0)

        while(self.calculation.len_of_initial_index_array(self.array_index) > 0):
            connectivity_vector = [self.calculation.connectivity_coef(vertex) for vertex in self.array_index]
            print("Вектор коэффициентов связности групп: ")
            print(connectivity_vector)

            list_of_max = self.calculation.get_list_of_min(connectivity_vector)
            print("Вершины, подлежащие размещению на кристалл: ")
            print(list_of_max)

            for vertex in list_of_max:
                self.array_index = self.calculation.insert_vertex_in_crystal(vertex, *vector_of_places[0])
                vector_of_places.pop(0)

            print("Кристал: ")
            print(self.crystal)
            print('\n')

        print("Кристалл заполнен!")
        print("Значение целевой функции: ", self.calculation.Q_function(), "\n")

    def start_iter(self):
        print("ИТЕРАЦИОННЫЙ АЛГОРИТМ \n")
        q = self.calculation.Q_function()
        q_new = 0

        while(True):
            print("Значение целевой функции: ", q)
            print("Кристалл ДО итерации: ")
            print(self.crystal)

            l_vector = np.array([self.calculation.L_function(vertex+1) for vertex in range(self.data.shape[0])])
            vertex = l_vector.argmax()
            print(l_vector[vertex])
            print("Вершина для замены: ", vertex+1)

            centre = self.calculation.centre_of_mass(vertex)
            print("Центр масс: ", centre)

            vertices = self.calculation.get_near_vertexes(*centre)
            print("Группа вершин: ", [vertex+1 for vertex in vertices])

            args = list()
            for vertex2 in vertices:
                self.crystal = self.calculation.swap_vertices(vertex+1, vertex2+1)
                args.append((vertex, vertex2, self.calculation.Q_function()))
                self.crystal = self.calculation.swap_vertices(vertex2+1, vertex+1)
            print("Значение целевой функции при замене вершины из группы вершин: ", args)

            args = min(args,key=lambda x: x[2])
            if(args[2] < q):

                print("Меняем вершины: ")
                print([vertex+1 for vertex in args[:-1]])

                self.crystal = self.calculation.swap_vertices(args[0]+1, args[1]+1)
                q_new = args[2]

            print("Кристалл ПОСЛЕ итерации: ")
            print(self.crystal)

            print("Новое начение целевой функции:", q_new, "\n")

            if(q_new >= q):
                print("Очередная итерация не уменьшила значение целевой функции. Оптимизация закончена")
                break

            q = q_new

    def __str__(self):
        return self.crystal.__str__()
        