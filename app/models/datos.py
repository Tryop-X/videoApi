########################################################################################################################
########################## CREDENCIALES Y NOMBRE DE LOS SERVICIOS A USAR ###############################################
########################################################################################################################

API_KEY_YOUTUBE = "AIzaSyC_SSAcmJZgl_tBU4QuCnUpLCLikBOXkGI"
API_KEY_OPENAI = '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'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# MONGO_URI = "mongodb+srv://hveras1:GlDC38DAX913ZSIv@videoai.mkgw6wh.mongodb.net/?retryWrites=true&w=majority"
MONGO_URI = "mongodb://127.0.0.1:27017/"
DATABASE_NAME = "video_db"
COLLECTION_NAME = "temario"

# MODELOS


model_temario = "gpt-3.5-turbo"
model_chat = 'gpt-3.5-turbo'
model_resumen = "gpt-3.5-turbo"

########################################################################################################################
########################## CONTENIDO DEL PROMPT PARA CONSULTA A LOS MODELOS DE GPT #####################################
########################################################################################################################

content_temario = """
Responde con un investigador siempre sugiriendo temas de investigación. 
Parte de temas más simples a más complejos.
Responde siempre con el siguiente json (3 temas como máximo, 3 aspectos como máximo)
{
    temaCentral: "", 
    aspectos: [
        {
            aspecto: "",
            temas: ["", "", ""]
        }, ...
    ]
}
"""

content_resumen = """
Vas a generar un resumen (texto ) usando lenguaje de un investigador experto. 
Vas a extraer el contenido y el resumen que generes tendrá la información que la transcripción que se ha proporcionado
"""

content_chat = """
Responderás como un investigador experto respondiendo a la siguiente pregunta con el contenido proporcionado
"""
