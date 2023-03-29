class SES_Correo:

    def accesos_ses():

        ### Se genera el cliente para SES 
        smtp_server = "email-smtp.us-east-1.amazonaws.com"
        port = 587  
        username = "AKIAZJLACZFP7S4QFI7F"
        password = "BE919f7FirQMRjnHc78Z5XYm7ojoOiqf9MVKB61zCVRX"
        Def_From = """avisos@bismoavisos.com"""

        return smtp_server, port, username, password, Def_From

    def sendemail(Def_To, Def_Header, Def_Body):

        # print("Def_To:" + str(Def_To))
        # print("Def_Header: " + str(Def_Header))
        # print("Def_Body: " + str(Def_Body))
        # if Def_filename is not None: 
        #     print("Def_filename: " + str(Def_filename))

        ### Se importan las librerias nesesarias
        import smtplib, ssl, urllib.request
        from email.mime.application import MIMEApplication
        from email.mime.multipart import MIMEMultipart 
        from email.mime.text import MIMEText 
        from email.mime.base import MIMEBase 
        from email import encoders 

        ### Se obtiene los accesos
        (smtp_server, port, username, password, Def_From) = SES_Correo.accesos_ses()

        ### Generamos el SSL context
        context = ssl.create_default_context()

        ### Se definen el formulario del correo
        #Def_To = """mkllo@yopmail.com"""
        #Def_Header = """Test1"""
        #Def_Body = """Ejemplo de envio de ficheros"""
   
        ### Empieza proceso para general y enviar el correo
        try:
            ### Generamos la instancia MIMEMultipart 
            msg = MIMEMultipart() 
            msg['From'] = Def_From 
            msg['To'] = Def_To 
            msg['Subject'] = Def_Header
  
            ### Agregamos el cuerpo del correo
            msg.attach(MIMEText(Def_Body, 'html'))
  
            ### Abrimos el fichero a enviar
            # Def_filename = "requirements.txt"
            # ### Agregamomos el fichero al mensaje 
            # if Def_filename is not None and Def_filename != "":

                # ### Agregamo el fichero contenido en el bucket de S3
                # URL_fichero = "https://ficherosbismo.s3.us-east-2.amazonaws.com/db_tierra_fund/requirements.txt"

                # part = MIMEApplication(URL_fichero, Def_filename)
                # part.add_header("Content-Disposition", 'attachment', filename=Def_filename)

                # ### Adjunta el fichero al correo
                # msg.attach(part)
 
            ### Generamos la sesion
            server = smtplib.SMTP(smtp_server,port)
  
            ### Se genera la seguridad 
            server.starttls(context=context) 
  
            ### Auntentificamos
            server.login(username, password)
  
            ### Enviamos el email
            server.sendmail(Def_From, Def_To, msg.as_string()) 
            server.quit() 

        except Exception as e:
            # Print any error messages to stdout
            print(e)

        return "enviado"
