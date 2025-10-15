# 🤖 Chat RAG - Sistema de Perguntas e Respostas sobre Documentos PDF

> **Desafio MBA Engenharia de Software com IA - Full Cycle**

Sistema de chat inteligente baseado em **RAG (Retrieval-Augmented Generation)** que permite fazer perguntas sobre documentos PDF usando modelos de IA da **OpenAI** ou **Google Gemini**.

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Arquitetura RAG](#-arquitetura-rag)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Pré-requisitos](#-pré-requisitos)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Como Usar](#-como-usar)
- [Modelos Suportados](#-modelos-suportados)
- [Troubleshooting](#-troubleshooting)
- [Considerações Importantes](#-considerações-importantes)

---

## 🎯 Sobre o Projeto

Este projeto implementa um sistema completo de **RAG (Retrieval-Augmented Generation)** que:

1. **Processa documentos PDF** dividindo-os em chunks menores
2. **Gera embeddings vetoriais** usando modelos da OpenAI ou Google Gemini
3. **Armazena vetores** em um banco PostgreSQL com extensão pgvector
4. **Busca por similaridade semântica** para encontrar trechos relevantes
5. **Gera respostas contextualizadas** usando LLMs (Large Language Models)

O sistema garante que as respostas sejam baseadas **exclusivamente no conteúdo do documento**, evitando alucinações e informações externas.

---

## 🏗️ Arquitetura RAG

```
┌─────────────────┐
│  document.pdf   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  1. INGESTÃO (ingest.py)                                │
│  - Carrega o PDF                                        │
│  - Divide em chunks (1000 chars, overlap 150)           │
│  - Gera embeddings (OpenAI ou Gemini)                   │
│  - Armazena no PostgreSQL com pgvector                  │
└────────┬────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  PostgreSQL + pgvector                                  │
│  Collection: document_collection                        │
└────────┬────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  2. BUSCA (search.py)                                   │
│  - Recebe pergunta do usuário                           │
│  - Converte pergunta em embedding                       │
│  - Busca top 10 chunks mais similares                   │
│  - Monta contexto com os chunks encontrados             │
└────────┬────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  3. GERAÇÃO DE RESPOSTA                                 │
│  - Preenche template de prompt com contexto + pergunta  │
│  - Envia para LLM (gpt-5-nano ou gemini-2.5-flash-lite) │
│  - Retorna resposta baseada apenas no contexto          │
└────────┬────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  4. CHAT (chat.py)                                      │
│  - Interface interativa para o usuário                  │
│  - Loop de perguntas e respostas                        │
└─────────────────────────────────────────────────────────┘
```

---

## ✨ Funcionalidades

✅ **Suporte a múltiplos modelos**: OpenAI (gpt-5-nano) e Google Gemini (gemini-2.5-flash-lite)  
✅ **Processamento inteligente de PDF**: Divisão em chunks com overlap para manter contexto  
✅ **Busca semântica avançada**: Utiliza embeddings vetoriais para encontrar informações relevantes  
✅ **Respostas contextualizadas**: LLM responde apenas com base no documento fornecido  
✅ **Interface de chat interativa**: Conversação contínua com o sistema  
✅ **Processamento sob demanda**: Opção de processar o PDF direto no chat  
✅ **Validação rigorosa**: Previne alucinações e respostas fora do contexto  
✅ **Armazenamento persistente**: Não precisa reprocessar o PDF a cada execução  

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Finalidade |
|------------|--------|------------|
| Python | 3.9+ | Linguagem principal |
| LangChain | 0.3.27 | Framework RAG |
| PostgreSQL | 17 | Banco de dados |
| pgvector | 0.7.0 | Extensão de vetores |
| OpenAI API | 1.102.0 | Embeddings e LLM |
| Google Gemini API | 2.1.9 | Embeddings e LLM |
| Docker | Latest | Containerização do banco |
| python-dotenv | 1.1.1 | Gerenciamento de variáveis de ambiente |

---

## 📦 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.9+** ([Download](https://www.python.org/downloads/))
- **Docker & Docker Compose** ([Download](https://www.docker.com/products/docker-desktop/))
- **Git** ([Download](https://git-scm.com/downloads))
- **Chave de API OpenAI** ([Obter chave](https://platform.openai.com/api-keys))
- **Chave de API Google Gemini** ([Obter chave](https://aistudio.google.com/app/apikey))

---

## 📁 Estrutura do Projeto

```
mba-ia-desafio-ingestao-busca/
│
├── src/
│   ├── ingest.py       # Script de processamento e ingestão do PDF
│   ├── search.py       # Lógica de busca e geração de respostas
│   └── chat.py         # Interface de chat interativo
│
├── venv/               # Ambiente virtual Python (não versionado)
├── document.pdf        # Documento a ser processado
├── docker-compose.yml  # Configuração do PostgreSQL + pgvector
├── requirements.txt    # Dependências Python
├── .env.example        # Exemplo de configuração
├── .env                # Suas credenciais (não versionado)
├── .gitignore          # Arquivos ignorados pelo Git
└── README.md           # Este arquivo
```

---

## 🚀 Instalação

### 1️⃣ Clone o repositório

```bash
git clone https://github.com/natansa/mba-ia-desafio-ingestao-busca
cd mba-ia-desafio-ingestao-busca
```

### 2️⃣ Crie e ative o ambiente virtual

**Windows (Git Bash):**
```bash
python -m venv venv
source venv/Scripts/activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Suba o banco de dados PostgreSQL

```bash
docker-compose up -d
```

**Verificar se está rodando:**
```bash
docker ps
```

Você deve ver o container `postgres_rag` em execução.

---

## ⚙️ Configuração

### 1️⃣ Crie o arquivo `.env`

Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

### 2️⃣ Configure as variáveis de ambiente

Edite o arquivo `.env` e adicione suas credenciais:

```env
# =============================================================================
# BANCO DE DADOS
# =============================================================================
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=document_collection

# =============================================================================
# DOCUMENTO PDF
# =============================================================================
PDF_PATH=../document.pdf

# =============================================================================
# OPENAI
# =============================================================================
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_LLM_MODEL=gpt-5-nano

# =============================================================================
# GOOGLE GEMINI
# =============================================================================
GOOGLE_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GOOGLE_EMBEDDING_MODEL=models/embedding-001
GOOGLE_LLM_MODEL=gemini-2.5-flash-lite
```

### 3️⃣ Coloque seu documento PDF

Certifique-se de que o arquivo `document.pdf` está na raiz do projeto (ou ajuste o caminho no `.env`).

---

## 💬 Como Usar

### Opção 1: Processamento Integrado (Recomendado)

Execute o chat e escolha processar o PDF quando solicitado:

```bash
python src/chat.py
```

**Fluxo interativo:**

```
============================================================
BEM-VINDO AO CHAT RAG
============================================================

*ATENÇÃO: caso o documento já tenha sido processado por outro modelo, 
utilize o mesmo modelo para continuar a conversa.*

Deseja utilizar OPENAI ou GEMINI? openai

*ATENÇÃO: caso o documento já tenha sido processado por outro modelo, 
será necessário processar o documento novamente.*

Deseja processar o arquivo document.pdf antes de iniciar? (sim/não): sim

[PROCESSANDO O PDF...]
[SUCESSO] Documento processado e armazenado com sucesso!

Digite 'sair' ou 'exit' para encerrar o chat.

[FAÇA SUA PERGUNTA]: Qual é o tema principal do documento?

[PROCESSANDO...]

[RESPOSTA]: O documento trata sobre... [resposta baseada no PDF]

[FAÇA SUA PERGUNTA]: 
```

### Opção 2: Processamento Manual

Processe o PDF primeiro (necessário passar o modelo como argumento):

```bash
python src/ingest.py <openai|gemini>
```
**Somente OPENAI:**
```bash
python src/ingest.py openai
```
**Somente GEMINI:**
```bash
python src/ingest.py gemini
```

Depois inicie o chat:

```bash
python src/chat.py
```

### Comandos disponíveis no chat:

- Digite sua pergunta e pressione **Enter**
- Digite `sair`, `exit`, `quit` ou pressione **Enter** vazio para encerrar
- Use **Ctrl+C** para interromper a qualquer momento

---

## 🤖 Modelos Suportados

### OpenAI

**Embeddings:**
- `text-embedding-3-small`

**LLMs:**
- `gpt-5-nano`

### Google Gemini

**Embeddings:**
- `models/embedding-001`

**LLMs:**
- `gemini-2.5-flash-lite`

---

## 🔧 Troubleshooting

### ❌ Erro: `FileNotFoundError: File ...document.pdf not found`

**Solução:** Verifique se:
- O arquivo `document.pdf` está na raiz do projeto
- O caminho no `.env` está correto: `PDF_PATH=../document.pdf`

### ❌ Erro: `Environment variable X is not set`

**Solução:** Verifique se o arquivo `.env` existe e contém todas as variáveis necessárias.

### ❌ Erro: `Connection refused` ou `Failed to connect to database`

**Solução:** 
```bash
# Verifique se o Docker está rodando
docker ps

# Se não estiver, suba o banco novamente
docker-compose up -d

# Verifique os logs do container
docker logs postgres_rag
```

### ❌ Erro: `Invalid API key` ou `Authentication failed`

**Solução:** Verifique se suas chaves de API no `.env` estão corretas:
- OpenAI: `OPENAI_API_KEY=sk-proj-...`
- Gemini: `GOOGLE_API_KEY=AIzaSy...`

### ❌ Erro: `Invalid LLM model`

**Solução:** Certifique-se de digitar exatamente `openai` ou `gemini` (minúsculas) quando solicitado.

### ❌ Banco de dados corrompido ou duplicação de documentos

**Solução:** Recrie o banco do zero:
```bash
# Pare e remova os containers
docker-compose down -v

# Suba novamente
docker-compose up -d

# Reprocesse o PDF
python src/chat.py
```

---

## ⚠️ Considerações Importantes

### 🔐 Segurança
- **NUNCA** compartilhe suas chaves de API publicamente
- **NUNCA** faça commit do arquivo `.env`
- Use o `.env.example` como referência, mas mantenha suas credenciais privadas

### 💰 Custos
- OpenAI e Gemini cobram por uso de API
- Embeddings são baratos
- LLMs têm custos variados
- Monitore seu uso nos dashboards das plataformas

### 🔄 Consistência de Modelos
- **IMPORTANTE**: Use o mesmo modelo de embedding que foi usado para processar o documento
- Se processar com OpenAI, continue usando OpenAI
- Se processar com Gemini, continue usando Gemini
- Misturar modelos resultará em erro

### 📊 Performance
- **Chunk size**: 1000 caracteres (ajustável em `ingest.py`)
- **Chunk overlap**: 150 caracteres (mantém contexto entre chunks)
- **Top K**: 10 chunks mais relevantes (ajustável em `search.py`)
- **Temperature**: 0.1 (respostas mais determinísticas)

### 📝 Limitações
- Funciona apenas com arquivos PDF
- Máximo de tokens por consulta depende do modelo escolhido
- Respostas limitadas ao conteúdo do documento processado

---

## 📚 Referências

- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [pgvector Documentation](https://github.com/pgvector/pgvector)

---

## 👨‍💻 Autor

**https://github.com/natansa**

---

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais.

---

**Dúvidas?** Revise o [Troubleshooting](#-troubleshooting) ou consulte os logs de erro para mais informações.
