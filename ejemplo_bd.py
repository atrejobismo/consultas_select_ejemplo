from sqlalchemy import text
from Conexion_BD import Conexion_BD
from datetime import date
from SES_Correo import SES_Correo
from Log_BD import Log_BD
import time
import traceback

#####
## Autor: J.Zamarripa
## Revision: J.Zavala
## Fecha de creacion: 19/Junio/2020
#####

### Proceso principal: Llama a las funciones para ejecutar el proceso  
def proceso(engineapplication, event):
    try:
        query_extra = """ AND alias IS NOT NULL"""

        # poisbles tipos de respuesta execute select
        # fetchall(): lista de tupla o lista de diccionarios
        # fetchone(): diccionario objeto 
        # scalar(): NULL o  dato consultado 


        # SELECT segura para evitar inyecciones
        # query = text("""SELECT * FROM empresa WHERE id_empresa = :id """ + query_extra)
        # resultados = engineapplication.execute(query, 
        #                                         id = event['parametros']['id_empresa'],
        #                                         nombre = event['parametros']['nombre'],
        #                                         fecha = event['parametros']['fecha'],
        #                                         ).fetchone()
        # SELECT segura para evitar inyecciones
        id_empresa = event['parametros']['id_empresa']
        if not id_empresa: 
            response = {
                    "result": {
                        "process": False,
                        "data":{}
                        },
                    "errors": "Excepcion: No se envio id_empresa"
                }
        else:
            query = text("""SELECT * FROM empresa WHERE id_empresa = """ + str(id_empresa)  + query_extra)
            resultadosQuery = engineapplication.execute(query).fetchone()
            response = {
                    "result": {
                        "process": False,
                        "data":{}
                        },
                    "errors": "Excepcion: No se envio un id_empresa valido"
                }
            resultados = resultadosQuery if resultadosQuery else response


        #################################################

        # SELECT fetchone
        id_empresa = event['parametros']['id_empresa']
        if not id_empresa: 
            response = {
                    "result": {
                        "process": False,
                        "data":{}
                        },
                    "errors": "Excepcion: No se envio id_empresa"
                }
        else:
            empresa = engineapplication.execute("""SELECT * FROM empresa WHERE id_empresa = """ + str(id_empresa)  + query_extra).fetchone()
            razon_social = engineapplication.execute("""SELECT razon_social FROM empresa WHERE id_empresa = """ + str(id_empresa)  + query_extra).scalar()

            if empresa and razon_social:
                ### acceder fetchone
                print("FETCHONE")
                print("El nombre de la empresa es "+str( empresa['razon_social'] ))

            ## EJEMPLO SCALAR
            
            ### acceder SCaALR
                print("SCALAR")
                print("El nombre de la empresa es "+str( razon_social ))
            else:
                response = {
                    "result": {
                        "process": False,
                        "data":{}
                        },
                    "errors": "Excepcion: No se envio un id_empresa valido"
                }


        # EJEMPLO FETCHALL
        print("FETCHALL")
        id_empresa = event['parametros']['id_empresa']
        if not id_empresa: 
            response = {
                    "result": {
                        "process": False,
                        "data":{}
                        },
                    "errors": "Excepcion: No se envio id_empresa"
                }
        else:
            resultados = engineapplication.execute("""SELECT * FROM empresa WHERE id_empresa = """ + str(id_empresa)  + query_extra).fetchall()
            if resultados:
                print("resultado query: ")
                print(resultados)
                ### acceder fetchall
                resultado_en_json = []
                for r in resultados:
                    print("El nombre de la empresa es "+str( r['razon_social'] ))
                    print("Registarda es "+str( r['createdDate'] ))
                    resultado_en_json.append({
                            "id_empresa": r['id_empresa'],
                            "alias": r['alias'],
                            "createdDate": str(r['createdDate']),
                            "razon_social": r['razon_social'],
                            "rfc": r['rfc'],
                        })

                response = {
                            "result": {
                                "process": True,
                                "data": resultado_en_json
                                },
                            "errors": ""
                        }
            else:
                response = {
                "result": {
                    "process": False,
                    "data":{}
                    },
                "errors": "Excepcion: No se envio un id_empresa valido"
                }
        return response
    except Exception as e:
        response = {
                    "result": {
                        "process": False,
                        "data":{}
                        },
                    "errors": "Excepcion: "+str(e)+". Mas informacion: "+ str(traceback.format_exc())
                }

        return response


### Metodo principal: Hace la conexion a la base de datos, ejecuta el proceso y regresa un resultado
def main(event, context):

    ### Guarda la fecha y hora de ejecucion
    fecha_hora_ejecucion = time.strftime('%Y-%m-%d %H:%M:%S')

    ### Conexion a la base de datos
    conexion_bd = Conexion_BD
    (resultado_conexion, engineapplication, nombre_bd) = conexion_bd.conexion(event)

    ### Si la conexion fue exitosa ejecuta el proceso
    if resultado_conexion == True:
        resultado_proceso = proceso(engineapplication, event)

    ### Si la conexion fallo envia un mensaje de error
    else:
        resultado_proceso = {
                    "result": {
                        "process": False,
                        "data": []
                        },
                    "errors": "Error conexion bd" + str(resultado_conexion)
                 }

    ### ¡COMENTAR ANTES DE SUBIR! Imprime en la consola el resultado del proceso al simular el proceso.
    print(resultado_proceso)

     ### Guarda el resultado en el log de la aplicacion
    log_bd = Log_BD
    log_bd.guardar_resultado("ejemplo_db", fecha_hora_ejecucion, event['conexion']['fk_user'], engineapplication, resultado_proceso, nombre_bd)


    ### Regresa el resultado del proceso
    return resultado_proceso
    
### Simula el envio del JSON
### ¡COMENTAR ANTES DE SUBIR! Simula el envio del JSON.
# contenido_json = {
#         "conexion": {
#                     "usuario": "ad8pEkV6o4ZNC/jEf1zSpE/BoEFPhaP4JoFGVq8jdAE=",
#                     "contrasena": "K1ajXa6QcbicYS+ow4kygXm0ht/tXPVd4z4fnWooOfs=",
#                     "instancia": "ad8pEkV6o4ZNC/jEf1zSpGznpMglUkY55zGgHwd8tU3FYv/GpDheQGS6aicPjJWu0RjvIWtm2aJ2wbP12FZd4g==",
#                     "puerto": "ad8pEkV6o4ZNC/jEf1zSpKLuEFHZPo90oozQ4jNB3Bc=",
#                     "bd": "ad8pEkV6o4ZNC/jEf1zSpE/BoEFPhaP4JoFGVq8jdAE=",
#                     "nombre_app": "ad8pEkV6o4ZNC/jEf1zSpGnfKRJFeqOGTQv4xH9c0qQ=",
#                     "fk_user": "SCHEDULER"
#                 },
#         "parametros": {
#             "id_empresa": "1",
#             "nombre": "",
#             "fecha": "1",
#         }

#       }

# context = ""

# main(contenido_json, context)