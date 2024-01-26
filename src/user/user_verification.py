import os
from dotenv import load_dotenv
import pyotp
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#from config.config import EMAIL_SENDER, EMAIL_PASSWORD
import logging

load_dotenv('../../config/.env')
logging.basicConfig(level= logging.INFO)
email_file_path = os.path.join(os.path.dirname(__file__), '..', 'msg', 'email.html')


def generate_otp():
    """Genera un OTP con una duración de 5 minutos."""
    secret = pyotp.random_base32()  # Esto debe ser una cadena en base32
    totp = pyotp.TOTP(secret, interval=300)  # 300 segundos = 5 minutos
    return totp.now(), secret

def send_otp_email(recipient_email, otp):
    """Envía el OTP al correo electrónico del usuario."""
    try:
        try: 
            #Abre el html prediseñado
            with open(email_file_path, 'r', encoding='utf-8') as ver_email:
                html = ver_email.read()
        except Exception as e:
            logging.info('No se pudo acceder al correo')
            logging.info(e)

        # Reemplaza el marcador de posición en el HTML con el OTP
        html = html.replace('<!--OTP-->', otp)

        # Configura el mensaje
        msg = MIMEMultipart()
        msg['Subject'] = 'Código de Verificación'
        #msg['From'] = EMAIL_SENDER
        msg['From'] = os.getenv('EMAIL_SENDER')
        msg['To'] = recipient_email
        
        msg.attach(MIMEText(html, 'html', 'utf-8'))    
        # Conecta al servidor SMTP y envía el correo
        try: 
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                #server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                server.login(os.getenv('EMAIL_SENDER'), os.getenv('EMAIL_PASSWORD'))
                #server.sendmail(EMAIL_SENDER, recipient_email, msg.as_string())
                server.sendmail(os.getenv('EMAIL_SENDER'), recipient_email, msg.as_string())
        except Exception as e:
            logging.info('No se pudo enviar el correo _N')
            logging.info(e)
    except Exception as e:
        logging.info('No se pudo enviar el correo')
        logging.info(e)

def verify_otp(otp, user_input):
    """Verifica si el OTP ingresado por el usuario es correcto."""
    totp = pyotp.TOTP(otp, interval=300)  # 300 segundos = 5 minutos
    return totp.verify(user_input)
