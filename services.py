import requests
import sett  # Asumiendo que `sett` es un módulo existente en tu proyecto
import json
import time

def obtener_mensaje_whatsapp(message):
    try:
        if 'type' not in message:
            text = 'mensaje no reconocido'
            return text

        typeMessage = message['type']
        if typeMessage == 'text':
            text = message['text']['body']
        elif typeMessage == 'button':
            text = message['button']['text']
        elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
            text = message['interactive']['list_reply']['title']
        elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
            text = message['interactive']['button_reply']['title']
        else:
            text = 'mensaje no procesado'
        return text
    except Exception as e:
        return 'No se pudo obtener el mensaje: ' + str(e)
    
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

def buttonReply_Message(number, options, body, footer, sedd, messageId):
    buttons = [] 
    for i, option in enumerate(options):
        buttons.append({
            "type": "reply",
            "reply": {
                "id": sedd + "_btn_" + str(i+1),
                "title": option
            }
        })
    data = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        })
    return data

def listReply_Message(number, options, body, footer, sedd, messageId):
    rows = []
    for i, option in enumerate(options):
        rows.append({
            "id": sedd + "_btn_" + str(i+1),
            "title": option,
            "description": "",
        })
    data = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "body": {
                "text": body
            },
            "footer": {
                "text": footer
            },
            "action": {
                "button": "Ver más",
                "sections": [
                    {
                        "title": "<List Category Item>",
                        "rows": rows
                    }
                ]
            }
        }
    })  
    return data

def document_Message(number, url, caption, filname):
    data = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "document",
        "document": {
            "url": url,
            "caption": caption,
            "filename": filname
        }
    })
    return data

def sticker_Message(number, sticker_url):
    data =  json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "sticker",
        "sticker": {
            "id": sticker_url
        }
    })
    return data

def get_media_id(media_name , media_type):
    media_id = ""
    if media_type == "sticker":
        media_id = sett.stickers.get(media_name, None)
    return media_id

def replyText_Message(number, messageId, text):
    data = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "context": {"message_id":messageId},
        "type": "text",
        "text": {
            "body": text
        }
    })
    return data

def markRead_Message(messageId):
    data = json.dumps({
        "messaging_product": "whatsapp",
        "status": "mark_seen",
        "message_id": messageId
    })
    return data

def admin_chatbot(text, number, messageId, name):
    try:
        text = text.lower()  # Tomamos el mensaje del usuario
        print("mensaje del usuario:", text)
        lista = []
        if "hola" in text:
            body = "¡Bienvenidos a nuestro Salón de Belleza! 👋"
            footer = "Salón de Belleza 💅"
            options = ["✅ Servicios", "📅 Agendar Cita", "🏠 Ubicacion", "👤 Contacto", "📰 Catalogo"]
            replyButtonData = buttonReply_Message(number, options, body, footer, "sed1", messageId)
            lista.append(replyButtonData)
        
        elif "Servicios" in text:
            body = "Selecciona el servicio que deseas"
            footer = "Salón de Belleza"
            options = ["Manicure 💅", "Pedicure 🦶", "Masajes 💆", "Dermatología 👧👦"]

            listReplyData = listReply_Message(number, options, body, footer, "sed2", messageId)
            stickers = sticker_Message(number, get_media_id("gato", "sticker"))

            lista.append(listReplyData)
            lista.append(stickers)
        elif "Manicure" in text:
            body = "Selecciona el tipo de manicure que deseas"
            footer = "Salón de Belleza"
            options = ["Limpieza", "Decoración", "Mantenimiento"]
            listReplyData = listReply_Message(number, options, body, footer, "sed3", messageId)
            lista.append(listReplyData)
        elif "Catalogo" in text:
            body = "Descarga nuestro catalogo de servicios"
            footer = "Salón de Belleza"
            options = ["Descargar ⬇️", "⛔ No, Gracias"]
            
            replyButtonData = buttonReply_Message(number, options, body, footer, "sed4", messageId)
            lista.append(replyButtonData)
        elif "descargar" in text:
            textMessage = text_message(number, "Descargando nuestro catalogo de servicios...⏲️")
            enviar_mensaje_whatsapp(textMessage) # Enviamos el mensaje al usuario pasándolo como parámetro el mensaje

            documentData = document_Message(number, sett.document_pdf, body, "Catalogo de Servicios 👍")
            enviar_mensaje_whatsapp(documentData)
            time.sleep(2)
            textMessage = text_message(number, "¡Listo! 🎉")
            enviar_mensaje_whatsapp(textMessage)

            body = "¿Te gustaría programar una reunión con uno de nuestros especialistas para discutir estos servicios más a fondo?"
            footer = "Salón de Belleza"
            options = ["✅ Sí, agenda reunión", "⛔ No, gracias."]

            replyButtonData = buttonReply_Message(number, options, body, footer, "sed5", messageId)
            lista.append(replyButtonData)
        elif "sí, agenda reunión" in text:
            body = "Estupendo. Por favor, selecciona una fecha y hora para la reunión:"
            footer = "Salón de Belleza"
            options = ["📅 10: mañana 10:00 AM", "📅 7 de junio, 2:00 PM", "📅 8 de junio, 4:00 PM"]

            listReply = listReply_Message(number, options, body, footer, "sed6", messageId)
            lista.append(listReply)
        elif "7 de junio, 2:00 pm" in text:
            body = "Excelente, has seleccionado la reunión para el 7 de junio a las 2:00 PM. Te enviaré un recordatorio un día antes. ¿Necesitas ayuda con algo más hoy?"
            footer = "Salón de Belleza"
            options = ["✅ Sí, por favor", "❌ No, gracias."]

        elif "no, gracias" in text:
            textMessage = text_message(number, "Perfecto! No dudes en contactarnos si tienes más preguntas. Recuerda que también ofrecemos material gratuito para la comunidad. ¡Hasta luego! 😊")
            lista.append(textMessage)
        else:
            data = text_message(number, "Lo siento, no entendí lo que dijiste. ¿Quieres que te ayude con alguna de estas opciones?")
            lista.append(data)

        for item in lista:
            enviar_mensaje_whatsapp(item)
    except Exception as e:
        return 'Error en la función admin_chatbot: ' + str(e), 403
