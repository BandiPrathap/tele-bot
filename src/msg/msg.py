msg_bot = {
    'msg_start': "¡Hola soy el bot UG! 🤖 \nPuedo responder a tus preguntas acerca de los pagos y matriculaciones de la carrera de software. Para poder usar este bot debes estar registrado, si aun no lo estás puedes hacero utilizando el comando /registrar 😉",
    'msg_get_correo': "Por favor ingresa tu correo insitucional de la UG 📧",
    'msg_is_regitered': "Ya te encuentras registrado en el bot 😅",
    'msg_wrong_email': "Parece que el correo electrónico ingresado no es válido 🤔\nRecuerda que debe ser tu correo institucional de la UG, aquel que termina en @ug.edu.ec 📧\nSi no cuentas con este correo debes acercarte a las oficinas de la facultad 😉",
    'msg_otp_to_email': "Se ha enviado un código al correo que ingresaste, escribe este código en chat para completar el proceso 😁",
    'msg_exit_is_not_regitered': "No estás registrado en el bot 😅\n Para registrarte puedes usar el comando /registrar 😉",
    'msg_ver_user': "¡Te has registrado con éxito! \nYa puedes interactuar con el bot. 😁",
    'msg_exit_user': "Has sido dado de baja del bot exitosamente... 😢\n",
    'msg_wrong_otp': "El código introducido es incorrecto o ha expirado. 😵",
    'msg_user_is_not_registered': "¡No estás registrado! 🤖\nPuedes utilizar el comando /registrar para empezar a interactuar con el bot 😁",
    'msg_limit': "¡Alcanzaste el límite diario de consultas al bot! 😓\n El día de mañana responderé a tus preguntas con mucho gusto 😁",
    'msg_help_login': "Para registrarte en el asistente virutal debes seguir los siguientes pasos: 🤓👇\n\n1. Debes escribir en el chat el comando /registrar \nTe aparecerá un mensaje solicitando tu correo institucional de la UG, debes tener en cuenta que se trata del correo que finaliza con @ug.edu.ec, en caso de no poder acceder a este correo solicita información en secreataría \n2. Una vez escrito el correo correctamente, te llegará un código de verificación al correo que ingresaste \nDebes escribir en el chat el código que recibiste, el código expira en 6 minutos 🕗 \n\n¡Ahora ya puedes interactuar con el bot! 😄 \n\nEn caso de que el código esté expirado debes repetir el proceso enviando /registrar en el chat. 😉",
    'msg_help_logout':"Para darte de baja del asistente virtual debes seguir los siguiente pasos: 🤓👇\n\n1. Debes escribir en el chat el comando /salir \nTe aparecerá un mensaje solicitando el correo institucional UG con el que te inscribiste \n2. Una vez escrito el correo correctamente, te llegará un código de verificación al correo que ingresaste \nDebes escribir en el chat el código que recibiste, el código expira en 6 minutos 🕗 \n\n¡Ahora ya te abrás dado de baja del asistente virtual! 😯 \n\nEn caso de que el código esté expirado debes repetir el proceso enviando /salir en el chat. 😬",
    'msg_about': "¡Yo soy el asistente virtual UG! 🤖\n\nFui creado para responder dudas sobre matrículas y pagos a los estudiantes de la carrera de Ingeniería de Software de la universidad de Guayaquil. 🧑‍💻\n\nFunciono con Inteligencia Artificial, puedes escribir en el chat cualquier pregunta que tengas sobre pagos/matrículas y te responderé con mucho gusto. 😉",
    'msg_links': "Estos enlaces podrían ser de tu interés: 🤓👇\n\n- Sistema integrado de la universidad de Guayaquil (SIUG): \nhttps://servicioenlinea.ug.edu.ec/\n\n- Campus virtual UG: \nhttps://campusvirtual2.ug.edu.ec/",
    'msg_help_actividad': "Para ver cuántas veces interactuaste hoy con el chat debes uilizar el comando /actividad\n\nRecuerda que solo puedes hacer 25 consultas al día 😁"
}

def get_msg(msg_name):
    # Obtiene el mensaje del diccionario o devuelve un mensaje por defecto si la clave no existe
    return msg_bot.get(msg_name, "Mensaje no reconocido")