"""
Para muchos casos de usos solo enviar un texto para ser procesado 
no es suficiente, por lo que se requiere de una secuencia de procesos 
que se ejecuten en orden. Para esto se puede utilizar las cadenas 
SimpleSequentialChain o SequentialChain que permiten encadenar varios 
procesos de manera secuencial.
"""

import os
from langchain import LLMChain, OpenAI, PromptTemplate
from langchain.chains import SimpleSequentialChain

API = os.environ['OPENAI_API_KEY']
llm = OpenAI(openai_api_key=API)

# PRIMER CHAIN
prompt = '''You are a great translator Spanish English. 
            Detect if the following text is in Spanish. If so, translate it to English, otherwise just return it:
            {pregunta}'''
template = PromptTemplate.from_template(prompt)

# # Armamos una cadena la cual va a recibir la salida de la cadena cadena_LLM y lo procesa para generar otro texto
cadena_lista = LLMChain(llm=llm, prompt=template, output_key="pregunta_traducida")

# # SEGUNDO CHAIN
prompt = '''You are a TI security expert.
            You are going to answer the following question on english and spanish:
            {pregunta_traducida}'''
template = PromptTemplate.from_template(prompt)
cadena_inicio = LLMChain(llm=llm, prompt=template, output_key="donde_iniciar")

# # EJECUTAMOS CHAIN
cadena_simple = SimpleSequentialChain(chains=[cadena_lista, cadena_inicio], verbose=True)
# cadena_simple.run("What is RSA?")
cadena_simple.run("Que es RSA?")
