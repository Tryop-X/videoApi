from flask import Blueprint, jsonify, request
from app.services import videoRepository as videoDb
from openai import OpenAI
import json

bp = Blueprint('routes', __name__)

api_key = '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'
client = OpenAI(api_key=api_key)
vid = videoDb.DataBaseConnection(database_name="videoCollection", collection_name="video")


#
# @bp.route('/get_video', methods=['POST'])
# def get_video():
#     # Recibir datos de JSON en la solicitud POST
#     # data = request.get_json()
#     #
#     # # Asegúrate de que el JSON contenga la clave 'consulta'
#     # if not data or 'consulta' not in data:
#     #     return jsonify({'error': 'No se proporcionó consulta'}), 400
#     #
#     # consulta = data['consulta']
#     # vid = videoDb.DataBaseConnection(database_name="videoCollection", collection_name="video")
#     # video = vid.search_video_embedding(consulta)
#
#     return jsonify(None), 200, {'ContentType': 'application/json'}

@bp.route('/get_video', methods=['GET'])
def get_video():
    consulta = request.args.get('consulta')
    video = vid.search_video(consulta)

    return jsonify(video), 200, {'ContentType': 'application/json'}


@bp.route('/get_cursos', methods=['POST'])
def get_curso():

    data =[
    {
        "tema": "Introducción a SQL",
        "preguntas": [
            {
                "pregunta": "¿Qué es SQL?",
                "respuestas": [
                    {
                        "respuesta": "SQL stands for 'Structured Query Language'.",
                        "correcto": True
                    },
                    {
                        "respuesta": "SQL is an abbreviation for 'Strategic QuestioningLanguage'.",
                        "correcto": False
                    }
                ]
            },
            {
                "pregunta": "¿Por qué es importante conocer SQL?",
                "respuestas": [
                    {
                        "respuesta": "SQL es necesario para manipular datos en bases de datos.",
                        "correcto": True
                    },
                    {
                        "respuesta": "SQL es útil solamente en aplicaciones de nivel alto.",
                        "correcto": False
                    }
                ]
            },
            {
                "pregunta": "¿Cuál es la diferencia entre SQL y otros lenguajes de programación?",
                "respuestas": [
                    {
                        "respuesta": "SQL es predominantemente un lenguaje de consulta, mientras que otros lenguajes son principalmente de desarrollo.",
                        "correcto": True
                    },
                    {
                        "respuesta": "No hay diferencias significativas entre SQL y otros lenguajes de programación.",
                        "correcto": False
                    }
                ]
            }
        ]
    },
    {
        "tema": "Fundamentos de SQL",
        "preguntas": [
                        {
                            "pregunta": "¿Cómo se enlazan consultas SQL a bases de datos?",
                            "respuestas": [
                                {
                                    "respuesta": "Con instrucciones como 'CREATE DATABASE', 'CREATE TABLE', etc.",
                                    "correcto": True
                                },
                                {
                                    "respuesta": "Solo es posible enlazar consultas a bases de datos de forma manual.",
                                    "correcto": False
                                }
                            ]
                        },
                        {
                            "pregunta": "¿Qué es SQL injection?",
                            "respuestas": [
                                {
                                    "respuesta": "Un tipo de ataque informático que consigue acceso no autorizado a bases de datos usando consultas SQL.",
                                    "correcto": True
                                },
                                {
                                    "respuesta": "Un problema que afecta exclusivamente a bases de datos de lenguaje no SQL.",
                                    "correcto": False
                                }
                            ]
                        },
                        {
                            "pregunta": "¿Qué es JOIN en SQL?",
                            "respuestas": [
                                {
                                    "respuesta": "Una manera de combinar consultas mediante el enlazamiento.",
                                    "correcto": True
                                },
                                {
                                    "respuesta": "Sólo es posible en bases de datos relacionales.",
                                    "correcto": False
                                }
                            ]
                        }
                    ]
                },
                {
                    "tema": "ESL (Lenguaje Espacial de Consulta)",
                    "preguntas": [
                        {
                            "pregunta": "¿Qué es ESL?",
                            "respuestas": [
                                {
                                    "respuesta": "ESL significa 'Extended SQL Language', y es un conjunto más extenso de instrucciones que SQL.",
                                    "correcto": True
                                },
                                {
                                    "respuesta": "ESL significa 'English as a Second Language'.",
                                    "correcto": False
                                }
                            ]
                        },
                        {
                            "pregunta": "¿Cuáles son las ventajas de ESL versus SQL tradicional?",
                            "respuestas": [
                                {
                                    "respuesta": "ESL permite consultas más flexibles y poderosas, además de integrar mejor con otras tecnologías.",
                                    "correcto": True
                                },
                                {
                                    "respuesta": "ESL es menos eficiente y más limitado, por lo que solo se utiliza en aplicaciones especializadas.",
                                    "correcto": False
                                }
                            ]
                        },
                        {
                            "pregunta": "¿Cómo se realiza la validación de datos en una consulta ESL?",
                            "respuestas": [
                                {
                                    "respuesta": "Utilizando comandos como 'CONSTRAINTS'.",
                                    "correcto": True
                                },
                                {
                                    "respuesta": "No es posible validar datos en ESL.",
                                    "correcto": False
                                }
                            ]
                        }
                    ]
                },
                {
                    "tema": "SQL Avanzado",
                    "preguntas": [
                        {
                            "pregunta": "¿Qué es GROUP BY en SQL?",
                            "respuestas": [
                                {
                                    "respuesta": "Un comando que agrupa registros en consultas pivotando por atributos específicos.",
                                    "correcto": True
                                },
                                {
                                    "respuesta": "Se utiliza solo para realizar agrupamientos manuales en operaciones de búsqueda.",
                                    "correcto": False
                                }
                            ]
                        },
                        {
                            "pregunta": "¿Cómo se agrega temporalidad a una consulta?",
                            "respuestas": [
                                {
                                    "respuesta": "Usando comandos como 'TIMESTAMP' y 'DATE'.",
                                    "correcto": True
                                },
                                {
                                    "respuesta": "Temporalidad no es posible en SQL.",
                                    "correcto": False
                                }
                            ]
                        },
                        {
                            "pregunta": "¿Qué es la normalización en bases de datos?",
                            "respuestas": [
                                {
                                    "respuesta": "Una técnica que garantiza la eficiencia de consultas mediante el ordenamiento y separación de datos.",
                                    "correcto": True
                                },
                                {
                                    "respuesta": "No es necesario considerar la normalización en bases de datos.",
                                    "correcto": False
                                }
                            ]
                        }
                    ]
                },
                {
                    "tema": "Business Intelligence (BI)",
                    "preguntas": [
                        {
                            "pregunta": "¿Qué es Business Intelligence?",
                            "respuestas": [
                                {
                                    "respuesta": "El desarrollo de soluciones de inteligencia empresarial que ayudan a las decisiones de negocio.",
                                    "correcto": True
                                },
                                {
                                    "respuesta": "Solo es posible con bases de datos relacionales.",
                                    "correcto": False
                                }
                            ]
                        },
                        {
                            "pregunta": "¿Qué es un KPI (Indicador clave de desempeño)?",
                            "respuestas": [
                                {
                                    "respuesta": "Un indicador que refleja la performance de una métrica clave de la organización.",
                                    "correcto": True
                                },
                                {
                                    "respuesta": "Una variable de entrada para las consultas de BI.",
                                    "correcto": False
                                }
                            ]
                        },
                        {
                            "pregunta": "¿Cómo se realiza la visualización de datos en BI?",
                            "respuestas": [
                                {
                                    "respuesta": "Utilizando herramientas como Power BI, Tableau, etc.",
                                    "correcto": True
                                },
                                {
                                    "respuesta": "Solo es posible en visualizaciones 2D con gráficos.",
                                    "correcto": False
                                }
                            ]
                        }
                    ]
                },
                {
                    "tema": "Inteligencia Artificial (IA) y Big Data",
                    "preguntas": [
                        {
                            "pregunta": "¿Qué es IA?",
                            "respuestas": [
                                {
                                    "respuesta": "La inteligencia artificial es un campo de la ciencia que estudia el desarrollo de sistemas similares a la mente humana.",
                                    "correcto": True
                                },
                                {
                                    "respuesta": "IA sólo se aplica a la automatización de procesos en negocios.",
                                    "correcto": False
                                }
                            ]
                        },
                        {
                            "pregunta": "¿Qué es Big Data?",
                            "respuestas": [
                                {
                                    "respuesta": "Un marco de referencia para la gestión y análisis de datos extremadamente grandes.",
                                    "correcto": True
                                },
                                {
                                    "respuesta": "Datos de gran tamaño que no son adecuados para análisis convencional.",
                                    "correcto": False
                                }
                            ]
                        },
                        {
                            "pregunta": "¿Cómo se realiza el entrenamiento de un sistema IA?",
                            "respuestas": [
                                {
                                    "respuesta": "Entrenando al sistema con conjuntos de datos para que aprenda patrones y desarrolle habilidades autónomas.",
                                    "correcto": True
                                },
                                {
                                    "respuesta": "IA no es posible sin intervención humana en el proceso de entrenamiento.",
                                    "correcto": False
                                }
                            ]
                        }
                    ]
                }
            ]

    data = vid.search_videos_by_embedding(data)

    return jsonify(data), 200, {'ContentType': 'application/json'}
