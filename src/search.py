import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.
- Ao final da resposta informe o modelo LLM que foi utilizado para responder a pergunta.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_prompt(question=None, llm_model=None):
  if not question:
    raise SystemExit("Question is not set")

  if llm_model == "openai":
    for k in ("OPENAI_API_KEY", "DATABASE_URL","PG_VECTOR_COLLECTION_NAME"):
      if not os.getenv(k):
        raise RuntimeError(f"Environment variable {k} is not set")
  elif llm_model == "gemini":
    for k in ("GOOGLE_API_KEY", "DATABASE_URL","PG_VECTOR_COLLECTION_NAME"):
      if not os.getenv(k):
        raise RuntimeError(f"Environment variable {k} is not set")
  else:
    raise SystemExit("Invalid LLM model")

  if llm_model == "openai":
    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL"))
  elif llm_model == "gemini":
    embeddings = GoogleGenerativeAIEmbeddings(model=os.getenv("GOOGLE_EMBEDDING_MODEL"))
  else:
    raise SystemExit("Invalid LLM model")

  if not embeddings:
    raise SystemExit("Failed to create embeddings")
  
  vectorStore = PGVector(
    embeddings=embeddings,
    collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
    connection=os.getenv("DATABASE_URL"),
    use_jsonb=True,
  )
  if not vectorStore:
    raise SystemExit("Failed to create vector store")

  results = vectorStore.similarity_search_with_score(question, k=10)
  if not results:
    raise SystemExit("Failed to get results from vector store")

  context = "\n\n".join([doc.page_content for doc, score in results])
  if not context:
    raise SystemExit("Failed to get context from results")

  prompt = PROMPT_TEMPLATE.format(
    contexto=context,
    pergunta=question
  )
  if not prompt:
    raise SystemExit("Failed to get prompt from context")

  if llm_model == "openai":
    llm = ChatOpenAI(model=os.getenv("OPENAI_LLM_MODEL"), temperature=0.1)
  elif llm_model == "gemini":
    llm = ChatGoogleGenerativeAI(model=os.getenv("GOOGLE_LLM_MODEL"), temperature=0.1)
  else:
    raise SystemExit("Invalid LLM model")

  if not llm:
    raise SystemExit("Failed to create LLM")

  response = llm.invoke(prompt)
  if not response:
    raise SystemExit("Failed to get response from LLM")
  
  return response.content