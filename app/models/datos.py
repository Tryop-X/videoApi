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
model_resumen = "gpt-4-1106-preview"
model_pdf = "gpt-4-1106-preview"

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


def get_contenido(tema: str, sub_temas: str):
    content_resumen = f"""
    Genera un texto académico con un estilo similar al de papers o tesis, utilizando SOLO la transcripción proporcionada como referencia. 
    El texto va a girar en torno a este tema:{tema} y este subtema:"{sub_temas}". 
    Organiza el texto en 2 o 3 párrafos ,utiliza un lenguaje formal y términos técnicos relacionados con el tema seleccionado. 
    El texto generado tendrá que estar basado en la transcripción que te proporcione:
    RESPONDE SIEMPRE EN ESPAÑOL
    """
    return content_resumen


def get_pdf_text(tema: str, sub_temas: str):
    content_resumen = f"""
    Genera un texto académico con un estilo similar al de papers o tesis, utilizando para esto el contenido que te proporcione. 
    Selecciona este tema:{tema} y estos subtemas:"{sub_temas}" para estructurar el texto. 
    Organiza el texto en introducción, desarrollo (acá abordarás cada uno de estos subtemas, solo vas a mencionar los subtemas que aparezcan en el contenido) y conclusión ,
    utiliza un lenguaje formal y términos técnicos relacionados con el tema antes mencionado. 
    El texto generado tendrá que estar basado en el contenido que te proporcione y CORRECTAMENTE CITADO.
    TEN EN CUENTA QUE AL GENERAR EL TEXTO, VAS A DETALLAR CADA COSA MENCIONADA EN EL CONTENIDO PROPORCIONADO (IMPORTANTE)
    Finalmente vas a generar las referencias bibliográficas diciendo que estas son un resumen generado a partir de 
    los datos que verás en el contenido que tendrá esta forma (CITA EN FORMATO APA):
    
    Autor: _autor_name | fecha publicación: _date
    Fuente: _url
    Título: _title_contend
    
    RESPONDE SIEMPRE EN ESPAÑOL
    """
    return content_resumen


content_chat = """
Responderás como un investigador experto respondiendo a la siguiente pregunta con el contenido proporcionado
"""

title_tema = """
REVISIÓN SISTEMÁTICA DE 
"""

label_info = """
Contenido autogenerado por nuestra herramienta de revisión de contenido audiovisual. 
Hecho por Hugo Vera S. y su amigo.
"""

footer_info = """
Contenido autogenerado por nuestra herramienta de revisión de contenido audiovisual. 
Hecho por Hugo Vera S. y su amigo.
"""