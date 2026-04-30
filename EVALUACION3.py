
import pymongo
from pymongo.errors import ConnectionFailure

def conectar_db():
    try:
        cliente = pymongo.MongoClient("mongodb://localhost:27017/")
        # Conexión dinámica que busca qué base de datos tiene la colección 'Personas'
        for db_name in cliente.list_database_names():
            db = cliente[db_name]
            if "Personas" in db.list_collection_names():
                return db["Personas"]
                
        # Base de datos y colección por defecto
        return cliente["EVALUACION3"]["Personas"]
    except ConnectionFailure:
        print("Error: No se pudo conectar a MongoDB. Asegúrate de que el servicio esté activo.")
        return None

# 1. FUNCION: BÚSQUEDA 
def buscar_persona(coleccion):
    rut_buscado = input("\nIngrese el RUT a buscar: ").strip()
    
    documento = None
    for doc in coleccion.find():
        if str(doc.get("RUT", "")).strip().lower() == rut_buscado.lower():
            documento = doc
            break
            
    if documento:
        print("\n--- Registro Encontrado ---")
        print(f"RUT: {documento['RUT']} | EDAD: {documento['EDAD']} | SEXO: {documento['SEXO']}")
    else:
        print("El documento a buscar no existe")

# 2. FUNCION: GUARDAR 
def guardar_persona(coleccion):
    rut = input("\nIngrese el nuevo RUT: ").strip()
    
    existe = False
    for doc in coleccion.find():
        if str(doc.get("RUT", "")).strip().lower() == rut.lower():
            existe = True
            break
            
    if existe:
        print("El documento a ingresar ya existe")
    else:
        try:
            edad = int(input("Ingrese la EDAD: "))
            sexo = input("Ingrese el SEXO: ").strip()
            coleccion.insert_one({"RUT": rut, "EDAD": edad, "SEXO": sexo})
            print("El documento fue guardado de manera correcta")
        except ValueError:
            print("Error: La edad debe ser un número.")

# 3. FUNCION: ACTUALIZAR 
def actualizar_persona(coleccion):
    rut = input("\nIngrese el RUT del registro a actualizar: ").strip()
    
    registro = None
    for doc in coleccion.find():
        if str(doc.get("RUT", "")).strip().lower() == rut.lower():
            registro = doc
            break
            
    if not registro:
        print("El documento a actualizar no Existe")
    else:
        try:
            nueva_edad = int(input("Ingrese la nueva EDAD: "))
            nuevo_sexo = input("Ingrese el nuevo SEXO: ").strip()
            coleccion.update_one({"_id": registro["_id"]}, {"$set": {"EDAD": nueva_edad, "SEXO": nuevo_sexo}})
            print("El documento fue actualizado correctamente")
        except ValueError:
            print("Error: La edad debe ser un número.")

# 4. FUNCION: ELIMINAR 
def eliminar_persona(coleccion):
    rut = input("\nIngrese el RUT del registro a eliminar: ").strip()
    
    registro = None
    for doc in coleccion.find():
        if str(doc.get("RUT", "")).strip().lower() == rut.lower():
            registro = doc
            break
            
    if not registro:
        print("El documento a eliminar no Existe")
    else:
        coleccion.delete_one({"_id": registro["_id"]})
        print("El documento fue eliminado correctamente")

### MENU DE COMANDOS###
def menu_principal():
    coleccion = conectar_db()
    if coleccion is None: return

    while True:
        print("\n========================================")
        print("      SISTEMA DE GESTIÓN (EVALUACIÓN 3)  ")
        print("========================================")
        print("1. Buscar Persona")
        print("2. Guardar Nueva Persona")
        print("3. Actualizar Persona")
        print("4. Eliminar Persona")
        print("5. Salir")
        
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1": buscar_persona(coleccion)
        elif opcion == "2": guardar_persona(coleccion)
        elif opcion == "3": actualizar_persona(coleccion)
        elif opcion == "4": eliminar_persona(coleccion)
        elif opcion == "5":
            print("Cerrando sistema...")
            break
        else:
            print("Opción no válida, intente de nuevo.")

if __name__ == "__main__":
    menu_principal()