import pyotp
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.config import EMAIL_SENDER, EMAIL_PASSWORD
import logging

logging.basicConfig(level= logging.INFO)

def generate_otp():
    """Genera un OTP con una duración de 5 minutos."""
    secret = pyotp.random_base32()  # Esto debe ser una cadena en base32
    totp = pyotp.TOTP(secret, interval=300)  # 300 segundos = 5 minutos
    return totp.now(), secret

def send_otp_email(recipient_email, otp):
    """Envía el OTP al correo electrónico del usuario."""
    #Abre el html prediseñado
    try:
        try: 
            with open('../src/msg','email.html', 'r', encoding='utf-8') as ver_email:
                html = ver_email.read()
        except Exception as e:
            logging.info('No se abrió el correo')
            logging.info(e)

        # Reemplaza el marcador de posición en el HTML con el OTP
        print(html)
        html = html.replace('<!--OTP-->', otp)

        # Configura el mensaje
        msg = MIMEMultipart()
        msg['Subject'] = 'Código de Verificación'
        msg['From'] = EMAIL_SENDER
        msg['To'] = recipient_email
        
        msg.attach(MIMEText(html, 'html', 'utf-8'))    
        # Conecta al servidor SMTP y envía el correo
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, recipient_email, msg.as_string())
    except Exception as e:
        logging.info('No se envió el correo')
        logging.info(e)

def verify_otp(otp, user_input):
    """Verifica si el OTP ingresado por el usuario es correcto."""
    totp = pyotp.TOTP(otp, interval=300)  # 300 segundos = 5 minutos
    return totp.verify(user_input)


"""
def generate_otp():
    #Genera un OTP con una duración de 5 minutos.
    secret = pyotp.random_base32()  # Esto debe ser una cadena en base32
    totp = pyotp.TOTP(secret, interval=300)  # 300 segundos = 5 minutos
    return totp.now(), secret

def send_otp_email(recipient_email, otp):
    #Envía el OTP al correo electrónico del usuario.
    # Configura el mensaje
    msg = MIMEText("Tu código de verificación es: " + otp)
    msg['Subject'] = 'Código de Verificación'
    msg['From'] = EMAIL_SENDER
    msg['To'] = recipient_email

    # Conecta al servidor SMTP y envía el correo
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, recipient_email, msg.as_string())

def verify_otp(otp, user_input):
    #Verifica si el OTP ingresado por el usuario es correcto.
    totp = pyotp.TOTP(otp, interval=300)  # 300 segundos = 5 minutos
    return totp.verify(user_input)
"""