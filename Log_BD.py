from sqlalchemy import text
from SES_Correo import SES_Correo
import time
import requests

## Descripcion: Se encarga de guarda el resultado de la ejecucion del proceso
class Log_BD:

    ### Nos permite guardar el resultado en la BD (Ejecucion exitosa o erronea)
    def guardar_resultado(log_nombre_proceso, log_fecha_hora_ejecucion, log_usuario, engineapplication, resultado_proceso, log_bd):

        # Verificamos los resultados obtenidos
        if resultado_proceso['result']['process'] == True:
            log_resultado = "True"
            log_descripcion_resultado = str(resultado_proceso['result']['data'])

        elif resultado_proceso['result']['process'] == False:
            log_resultado = "False"
            log_descripcion_resultado = str(resultado_proceso['errors'])

        else:
           log_resultado = "False"
           log_descripcion_resultado = str(resultado_proceso)

        query_insert = text(""" INSERT INTO x_config_log_procesos (
                                `proceso`,
                                `fk_user`,
                                `resultado`,
                                `descripcion_resultado`,
                                `fecha_hora_ejecucion`,
                                `fecha_hora_fin_ejecucion`
                                )
                                VALUES
                                (
                                :proceso,
                                :fk_user,
                                :resultado,
                                :descripcion_resultado,
                                :fecha_hora_ejecucion,
                                :fecha_hora_fin_ejecucion
                                );
                             """)

        # Guardamos la fecha hora fin de ejecucion
        log_fecha_hora_fin_ejecucion = time.strftime('%Y-%m-%d %H:%M:%S')

        # Ejecutamos el query
        engineapplication.execute(query_insert, 
                                  proceso = log_nombre_proceso,
                                  fk_user = log_usuario,
                                  resultado = log_resultado,
                                  descripcion_resultado = log_descripcion_resultado,
                                  fecha_hora_ejecucion = log_fecha_hora_ejecucion,
                                  fecha_hora_fin_ejecucion = log_fecha_hora_fin_ejecucion)

        # Por ultimo enviamos el correo de alerta a usuarios desarrolladores (Solamente si fallo)
        if log_resultado == "False":

          # Se realiza un diccionario de datos para enviarlo a la funcion
          contenido_resultado_error = {
                      "proceso": str(log_nombre_proceso),
                      "fk_user": str(log_usuario),
                      "resultado": str(log_resultado),
                      "descripcion_resultado": str(log_descripcion_resultado),
                      "fecha_hora_ejecucion": str(log_fecha_hora_ejecucion),
                      "fecha_hora_fin_ejecucion": str(log_fecha_hora_fin_ejecucion),
                      "base_datos": str(log_bd)
                    }

          # Ejecutamos la funcion encargada de enviar el correo
          Log_BD.enviar_resultado_erroneo(contenido_resultado_error)

        return ""

    # Nos permite generar el cuerpo del correo
    def generar_cuerpo_correo(contenido_resultado_error):

      cuerpo_correo = """ 
                        <table class="egt">
                          <tr>
                            <th>Proceso</th>
                            <th>Fk_user</th>
                            <th>Resultado</th>
                            <th>descripcion resultado</th>
                            <th>Fecha hora ejecucion</th>
                            <th>Fecha hora fin ejecucion</th>
                            <th>BD</th>
                          </tr>
                          <tr>
                            <td>""" + str(contenido_resultado_error['proceso']) + """</td>
                            <td>""" + str(contenido_resultado_error['fk_user']) + """</td>
                            <td>""" + str(contenido_resultado_error['resultado']) + """</td>
                            <td>""" + str(contenido_resultado_error['descripcion_resultado']) + """</td>
                            <td>""" + str(contenido_resultado_error['fecha_hora_ejecucion']) + """</td>
                            <td>""" + str(contenido_resultado_error['fecha_hora_fin_ejecucion']) + """</td>
                            <td>""" + str(contenido_resultado_error['base_datos']) + """</td>
                          </tr>
                        </table>
                      """

      return cuerpo_correo

    ### Nos permite enviar el resultado por correo (Ejecucion exitosa o erronea)
    def enviar_resultado_erroneo(contenido_resultado_error):
      
      # Obtenemos los correos del API para proceder a enviar los correos
      # Definimos la cabecera y el diccionario con los datos
      url = "https://cgdjsnxsdg.execute-api.us-east-2.amazonaws.com/v1_log_correos"
      headers = {}
      # Hacemos el request 
      solicitud = requests.post(url, json = {}, headers = headers)
  
      # Verificamos si se realizo la conexion exitosamente
      if solicitud.status_code == 200:
        correos_log = solicitud.json()

        # Genemos el titulo del correo
        titulo_correo = "Error en proceso: " + str(contenido_resultado_error['proceso'])
        cuerpo_correo = Log_BD.generar_cuerpo_correo(contenido_resultado_error)

        # Instanciamos la clase
        ses_correo = SES_Correo

        # Recorremos los correos obtenidos del API
        for correo_log in correos_log['result']['data']['correos']:

          # Enviamos el correo a cada uno de los correos descritos en el proceso
          ses_correo.sendemail(correo_log, titulo_correo, cuerpo_correo)


        return ""

