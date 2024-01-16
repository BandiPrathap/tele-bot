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
    'msg_limit': "¡Alcanzaste el límite diario de consultas al bot! 😓\n El día de mañana responderé a tus preguntas con mucho gusto 😁"
}

def get_msg(msg_name):
    # Obtiene el mensaje del diccionario o devuelve un mensaje por defecto si la clave no existe
    return msg_bot.get(msg_name, "Mensaje no reconocido")

# Ejemplo de uso
cadena = 'msg_start'
print(get_msg(cadena))