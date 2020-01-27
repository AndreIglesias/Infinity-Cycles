import json
import os

class DataHandling:

    def __init__(self, filename):
        self.filename = filename

    def save_data(self, key, *data):
        #Si no existe el archivo data.json lo crea. Se usa "a"(appending) porque si el archivo ya existe no da error...
        #La otra forma es usando "x" pero este da error si ya existe el archivo.

        file = open(self.filename,"a")
        file.close()

        # Almacenar los datos a guardar en diccionarios
        temp_dicc = {}
        for i in data:
            temp_dicc[i[0]] = i[1]
        try:
            with open(self.filename) as json_file:
                temp_data = json.load(json_file)
        except Exception:
            temp_data = {}
        # Guardar los datos del diccionario en la posicion key
        temp_data[key] = temp_dicc
        with open(self.filename, "w") as outfile:
            json.dump(temp_data, outfile, indent=4)

    def load_data(self):
        file = open(self.filename,"a")
        file.close()
        try:
            with open(self.filename) as json_file:
                return json.load(json_file)
        except Exception as e:
            return []
