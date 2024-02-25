import requests
import sett  # Asumiendo que `sett` es un módulo existente en tu proyecto
import json


def obtener_mensaje_whatsapp(message):
    try:
        if 'type' not in message:
            return "Mensaje no reconocido"
        typeMessage = message['type']
        if typeMessage == 'text':
            return message['text']['body']
        else:
            return "Tipo de mensaje no reconocido"
    except Exception as e:
        return 'No se pudo obtener el mensaje: ' + str(e)
    
#aquí usamos los tokens que hicimos en sett
def enviar_mensaje_whatsapp(data):
    try:
        whatsapp_token = sett.whatsapp_token
        whatsapp_url = sett.whatsapp_url
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + whatsapp_token
        }
        print(data, "data")
        response = requests.post(
            whatsapp_url,
            headers=headers,
            data=data
        )
        if response.status_code == 200:
            return 'Mensaje enviado', 200
        else:
            return 'Mensaje no enviado', response.status_code

    except Exception as e:
        return 'Error al enviar el mensaje: ' + str(e), 403


def text_message(number, text):
    data = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "text",
        "text": {
            "body": text
        }
    })
    return data

def admin_chatbot(text, number, messageId, name):
    try:
        text = text.lower()  # tomamos el mensaje del usuario
        data = text_message(number, 'Hola, ¿en qué puedo ayudarte?')
        enviar_mensaje_whatsapp(data)  # enviamos el mensaje al usuario pasándolo como parámetro el mensaje

    except Exception as e:
        return 'Error en la función admin_chatbot: ' + str(e), 403
