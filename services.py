import requests
import sett
import json
import time
#obtener mensaje de usuario
def obtener_Mensaje_whatsapp(message):
    if 'type' not in message:
        return 'No es un mensaje'
    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == 'button':
        text = message['button']['action']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_replay']['title']
    else:
        text = "No es un mensaje de texto"


    return text

#enviar mensaje a usuario
def enviar_mensaje_whatsapp(data):
    try:
        whatsapp_token = sett.whatsapp_token
        whatsapp_url = sett.whatsapp_url
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + whatsapp_token}
        response = requests.post(whatsapp_url, 
                                 headers=headers, 
                                 data=data)
        print(data)
        if response.status_code == 200:
            return 'mensaje enviado', 200
        else:
            return 'error al enviar mensaje', response.status_code
    except Exception as e:
        return e,403
       

def text_Message(number, text):
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
#esta funcion envia una lista de opciones 
def send_ReplayMessage(number, options, body, footer, sedd, messageId):
    buttons=[]
    buttons = []
    for i, option in enumerate(options):
        buttons.append(
            {
                "type": "reply",
                "reply": {
                    "id": sedd + "_btn_" + str(i+1),
                    "title": option
                }
            }
        )
    data = json.dumps(
        {
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
}
    )
    return data

#envia una lista de opciones
def send_ListMessage(number, options, body, footer, sedd, messageID):
    #lista de botones
    rows = []
    for i, options in enumerate(options):
        rows.append({
                {
                    "id":sedd + "_row_" + str(i+1),
                    "title": options,
                    "description": "",
                }
        })
    data  =  json.dumps(
        {
            {
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
                    "button": "Ver Opciones",
                    "sections": [
                        {
                            "title": "Secciones",
                            "rows": rows
                        }
                    ]
                }
            }
        }
        }
    )
    return data

#eviar documento PDF
def document_Message(number, url, caption, filename):

    data = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "document",
        "document": {
            "url": url,
            "caption": caption,
            "filename": filename
        }
    })
    return data

#responder al mensaje del usuario
def replyText_Message(number, messageId, text):

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": { "message_id": messageId },
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data

#marcar las notificaciones como leidas
def markRead_Message(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id":  messageId
        }
    )
    return data

#funcion para el chatbot del admin 
def admin_chatbot(text, number ,messageId, name):
    text = text.lower()
    list = []
    #opciones del chatbot 
    if "hola" in text:
        body ="Bienvenidos a Mis Galletas, En que podemos ayudarte?"
        footer="Mis Galletas"
        options = ["Servicios", "Reposteria"]
        replayButtonData = send_ReplayMessage(number, options, body, footer, "sed1", messageId)

        list.append(replayButtonData)
    elif "servicios" in text:
        body = "Estos son los servicios que ofrecemos de reposteria"
        footer = "Mis Galletas"
        options = ["Polvorones", "Cuernitos", "Galletas de Mantequilla"]
        listButtonData = send_ListMessage(number, options, body, footer, "sed2", messageId)
        list.append(listButtonData)
    elif "Polvorones" in text:
        body = "Te podemos enviar un PDF con el catalogo de reposteria"
        footer = "Mis Galletas"
        options = ["Enviar Catalogo", "No Gracias"]
        replayButtonData = send_ReplayMessage(number, options, body, footer, "sed3", messageId)
        list.append(replayButtonData)
    elif "Enviar Catalogo" in text:
        textMessage = text_Message(number, "Aqui tienes el catalogo de reposteria")
        enviar_mensaje_whatsapp(textMessage)
        time.sleep(2)
        document = document_Message(number, sett.document_pdf, "Catalogo de Reposteria", "catalogo.pdf")
        enviar_mensaje_whatsapp(document) #enviar el documento
        time.sleep(3)
        
        #se programa una reunion
        body = "¿Te gustaría programar una reunión con uno de nuestros especialistas para discutir estos servicios más a fondo?"
        footer = "Equipo Bigdateros"
        options = ["✅ Sí, agenda reunión", "No, gracias." ]

        replyButtonData = send_ReplayMessage(number, options, body, footer, "sed4",messageId)
        list.append(replyButtonData)
    elif "Sí, agenda reunión" in text:
        body = "Agenda tu reunion"  
        footer = "Mis Galletas"
        options = ["8 am De la mañana","10 am De la mañana", "2 pm de la tarde", "5 pm de la tarde"]
        listReplay = send_ReplayMessage(number, options, body, footer, "sed4", messageId)
        list.append(listReplay)
    elif "8 am De la mañana" in text:
        body = "Excelente, has seleccionado la reunión para el 7 de junio a las 2:00 PM. Te enviaré un recordatorio un día antes. ¿Necesitas ayuda con algo más hoy?"
        footer = "Equipo Bigdateros"
        options = ["✅ Sí, por favor", "❌ No, gracias."]

    elif "No, gracias." in text:
        textMessage = text_Message(number,"Perfecto! No dudes en contactarnos si tienes más preguntas. Recuerda que también ofrecemos material gratuito para la comunidad. ¡Hasta luego! 😊")
        list.append(textMessage)
        buttonReply = send_ReplayMessage(number, options, body, footer, "sed6",messageId)
        list.append(buttonReply)
    else:
        data = text_Message(number,"Lo siento, no entendí lo que dijiste. ¿Quieres que te ayude con alguna de estas opciones?")
        list.append(data)
    for data in list:
        enviar_mensaje_whatsapp(data)