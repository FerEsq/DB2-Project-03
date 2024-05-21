'''
 * Nombre: HBase.py
 * Autores:
    - Fernanda Esquivel, 21542
    - Adrian Fulladolsa, 21592
    - Elías Alvarado, 21808
 * Descripción: Programa principal que simula el funcionamiento de una base de datos NoSQL tipo HBase.
 * Lenguaje: Python
 * Recursos: VSCode, JSON
 * Historial: 
    - Creado el 20.05.2024
    - Modificado el 20.05.2024
'''

import json
import os
from datetime import datetime
import pyfiglet
from rich.console import Console
from rich.style import Style
from prettytable import PrettyTable

#Definir consola y estilos de rich
console = Console()
blueBold = Style(color="blue", bold=True)
redBold = Style(color="red", bold=True)
blueLight = Style(color="blue", bold=False)
redLight = Style(color="red", bold=False)

class HBase:
    """
    Constructor de la clase HBase
    """
    def __init__(self, directory='tables'):
        self.directory = directory
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    """
    Función para crear una tabla en HBase
    * fileName: Nombre del archivo JSON donde se guardará la tabla
    * tableName: Nombre de la tabla
    * columnFamilies: Lista de column families de la tabla
    """
    def create(self, fileName, tableName, columnFamilies):
        #Definir la estructura de la tabla
        tableStructure = {
            "metadata": {
                "table_name": tableName,
                "column_families": columnFamilies,
                "disabled": False,
                "created": datetime.now().isoformat(),
                "modified": datetime.now().isoformat(),
                "rows_counter": 0
            },
            "rows_data": {}
        }
        
        #Crear el archivo JSON con la estructura de la tabla
        filePath = os.path.join(self.directory, fileName)
        
        if os.path.exists(filePath):
            console.print(f"SISTEMA: El archivo {fileName} ya existe. ¿Desea sobrescribirlo? (s/n): ", style="blue bold")
            overwrite = input().strip().lower()
            if overwrite != 's':
                console.print("SISTEMA: Operación cancelada. La tabla no fue creada.", style=blueBold)
                return
        
        with open(filePath, 'w') as f:
            json.dump(tableStructure, f, indent=4)
        
        console.print(f'SISTEMA: Tabla {tableName} creada en {filePath}.', style=blueBold)
    
    """
    Función para listar las tablas en HBase
    """
    def list(self):
        listTable = PrettyTable()
        listTable.field_names = ["Tabla", "Column Families"]
        
        for file in os.listdir(self.directory):
            if file.endswith('.json'):
                tableName = file.replace('.json', '')
                filePath = os.path.join(self.directory, file)
                with open(filePath, 'r') as f:
                    data = json.load(f)
                    column_families = ", ".join(data["metadata"]["column_families"])
                listTable.add_row([tableName, column_families])
        
        print(listTable)
        print("\n")
    
    def disable(self, tableName):
        found = False
        for file in os.listdir(self.directory):
            if file.endswith('.json'):
                file_path = os.path.join(self.directory, file)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    if data["metadata"]["table_name"] == tableName:
                        data["metadata"]["disabled"] = True
                        data["metadata"]["modified"] = datetime.now().isoformat()
                        found = True
                        with open(file_path, 'w') as f_write:
                            json.dump(data, f_write, indent=4)
                        console.print(f'SISTEMA: Tabla {tableName} deshabilitada.', style=blueBold)
                        break
        
        if not found:
            print()
            console.print(f'ERROR: Tabla {tableName} no encontrada.', style=redBold)
    
    def is_enabled(self, table_name):
        #TODO: Implementar lógica para verificar si una tabla está habilitada
        pass
    
    def alter(self, table_name, new_structure):
        #TODO: Implementar lógica para modificar una tabla
        pass
    
    """
    Función para eliminar una tabla en HBase
    * tableName: Nombre de la tabla a eliminar
    """
    def drop(self, tableName):
        path = os.path.join(self.directory, f'{tableName}.json')
        if os.path.exists(path):
            os.remove(path)
            print(f'Table {tableName} dropped.')
        else:
            print(f'Table {tableName} does not exist.')
    
    """
    Función para describir una tabla en HBase
    * tableName: Nombre de la tabla a describir
    """
    def describe(self, tableName):
        path = os.path.join(self.directory, f'{tableName}.json')
        if os.path.exists(path):
            with open(path, 'r') as f:
                data = json.load(f)
                return data
        else:
            print(f'Table {tableName} does not exist.')

"""
Función para solicitar los datos necesarios para crear una tabla en HBase
* hbase: Instancia de la clase HBase
"""
def requestCreateData(hbase):
    try:
        fileName = input("Ingrese el nombre del archivo JSON: ").strip() + ".json"
        tableName = input("Ingrese el nombre de la tabla: ").strip()
        columnFamilies = input("Ingrese las column families separadas por comas: ").strip().split(',')
        columnFamilies = [cf.strip() for cf in columnFamilies]
        
        hbase.create(fileName, tableName, columnFamilies)
    
    except Exception as e:
        print()
        console.print(f"ERROR: No fue posibe crear la tabla: {e}", style=redBold)

"""
Función para solicitar los datos necesarios para deshabilitar una tabla en HBase
* hbase: Instancia de la clase HBase
"""
def requestDisableData(hbase):
    try:
        tableName = input("Ingrese el nombre de la tabla: ").strip()
        
        hbase.disable(tableName)
    
    except Exception as e:
        print()
        console.print(f"ERROR: No fue posibe deshabilitar la tabla: {e}", style=redBold)

"""
Función para imprime los comandos disponibles
"""
def printComands():
    table = PrettyTable()
    table.field_names = ["Comando", "Funcionalidad"]
    table.add_row(["create", "Crear nueva tabla"])
    table.add_row(["list", "Listar tablas de la base de datos"])
    table.add_row(["disable", "Deshabilitar una tabla"])
    table.add_row(["help", "Imprimir los comandos disponibles"])
    table.add_row(["exit", "Salir del programa"])

    print(table)

#Ejecución del programa
if __name__ == '__main__':
    hbase = HBase()

    #Imprimir bienvenida
    asciiHBase = pyfiglet.figlet_format("HBase Simulator")
    print(asciiHBase)

    console.print("A continuación escriba el comando que desea ejecutar:", style=blueBold)
    printComands()
    print("\n")
    
    while True:
        command = input('> ').strip().lower()
        
        if command == 'create':
            requestCreateData(hbase)
        
        elif command == 'list':
            tablesList = hbase.list()

        elif command == 'disable':
            requestDisableData(hbase)
        
        elif command == 'drop':
            table_name = input("Ingrese el nombre de la tabla a eliminar: ").strip()
            hbase.drop(table_name)
        
        elif command == 'describe':
            table_name = input("Ingrese el nombre de la tabla a describir: ").strip()
            description = hbase.describe(table_name)
            if description:
                print(json.dumps(description, indent=4))

        elif command == 'help':
            printComands()
        
        elif command == 'exit':
            console.print("\n¡Gracias por utilizar el programa!", style=blueBold)
            break
        
        else:
            console.print("ERROR: Comando desconocido.", style=redBold)
