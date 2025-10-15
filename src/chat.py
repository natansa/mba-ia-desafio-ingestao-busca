from search import search_prompt
from ingest import ingest_pdf

def main():
    print("=" * 60)
    print("BEM-VINDO AO CHAT RAG")
    print("=" * 60)
    
    llm_model = input("\n*ATENÇÃO: caso o documento já tenha sido processado por outro modelo, utilize o mesmo modelo para continuar a conversa.* \n\nDeseja utilizar OPENAI ou GEMINI? ").strip().lower()
    processar = input("\n*ATENÇÃO: caso o documento já tenha sido processado por outro modelo, será necessário processar o documento novamente.* \n\nDeseja processar o arquivo document.pdf antes de iniciar? (sim/não): ").strip().lower()
    
    if processar in ("sim", "s", "yes", "y"):
        try:
            print("\n[PROCESSANDO O PDF...]")
            ingest_pdf(llm_model=llm_model)
            print("[SUCESSO] Documento processado e armazenado com sucesso!")
        except Exception as e:
            print(f"\n[ERRO AO PROCESSAR]: {e}")
            print("Você ainda pode continuar e fazer perguntas se o documento já foi processado anteriormente.\n")
    
    print("\nDigite 'sair' ou 'exit' para encerrar o chat.\n")

    while True:
        try:
            question = input("\n[FAÇA SUA PERGUNTA]: ").strip()
            
            if question.lower() in ("sair", "exit", "quit", ""):
                print("\nEncerrando o chat. Até logo!")
                break
            
            print("\n[PROCESSANDO...]")
            response = search_prompt(question=question, llm_model=llm_model)
            
            print(f"\n[RESPOSTA]: {response}")
            
        except KeyboardInterrupt:
            print("\n\nChat interrompido pelo usuário. Até logo!")
            break
        except Exception as e:
            print(f"\n[ERRO]: {e}")
            print("Tente novamente ou digite 'sair' para encerrar.")

if __name__ == "__main__":
    main()