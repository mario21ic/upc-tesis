from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
#from langchain.llms import OpenAI
from langchain_openai import ChatOpenAI

# Definir dos modelos de lenguaje como "expertos"
expert_1 = ChatOpenAI(model_name="gpt-4o-mini")
expert_2 = ChatOpenAI(model_name="gpt-4o")

# Crear plantillas de prompt para ambos expertos
prompt_expert_1 = PromptTemplate(
    input_variables=["question"],
    template="Experto en criptografía: {question}"
)

prompt_expert_2 = PromptTemplate(
    input_variables=["question"],
    template="Experto en matemáticas: {question}"
)

# Crear cadenas con los modelos y sus respectivos prompts
chain_expert_1 = LLMChain(llm=expert_1, prompt=prompt_expert_1)
chain_expert_2 = LLMChain(llm=expert_2, prompt=prompt_expert_2)

# Implementar una función de gating para seleccionar el experto adecuado
def gating_function(question):
    if "criptografía" in question.lower() or "rsa" in question.lower():
        return chain_expert_1
    elif "matematicas" in question.lower() or "calculo" in question.lower():
        return chain_expert_2
    else:
        # En caso de que no coincida, usar un experto por defecto
        return chain_expert_1

# Definir una pregunta de entrada
#question = "¿Cómo funciona RSA en criptografía?"
question = "¿Que es calculo en matematicas?"

# Usar la función de gating para seleccionar el experto adecuado
selected_chain = gating_function(question)

# Ejecutar la cadena seleccionada para obtener la respuesta
response = selected_chain.run(question)

# Mostrar la pregunta y la respuesta
print(f"Model: {selected_chain}")
print(f"Pregunta: {question}")
print(f"Respuesta del experto seleccionado: {response}")

