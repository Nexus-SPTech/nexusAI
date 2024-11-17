import os
from dotenv import load_dotenv
from groq import Groq

# Carregar variáveis de ambiente do .env
load_dotenv()


class GroqClient:
    def __init__(self):
        # Obter a chave de API do .env
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("A chave de API não foi definida. Verifique o .env ou as variáveis de ambiente.")

        # Inicialização do cliente Groq
        self.client = Groq()  # Assume que a biblioteca Groq está corretamente configurada para usar o env

        # Parâmetros específicos do modelo e mensagens
        self.model = "llama3-8b-8192"
        self.system_message = {
            "role": "system",
            "content": (
                "Você é um analista de dados da empresa Nexus, somos uma empresa focada "
                "em análise de dados escolares e com base nesses dados você irá fornecer "
                "insights e opiniões. Vale se orientar que a avaliação dos alunos é medida "
                "em porcentagens que vão de 0 a 100% e os alunos têm as seguintes matérias: "
                "Português, Matemática, Filosofia e Física. e responda na seguinte estrutura: 'Nexus AI: *conteudo separado por topicos 100% em pt-br e fale sempre dos alunos no plural* '"
            )
        }

    def ask_question(self, question):
        # Enviar a pergunta para a Groq
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                self.system_message,
                {"role": "user", "content": question}
            ],
            temperature=1,
            max_tokens=1140,
            top_p=1,
            stream=False,
            stop=None,
        )

        # Acessando o conteúdo da resposta corretamente
        try:
            # Acessando diretamente o atributo de content do objeto
            return completion.choices[0].message.content  # Acessa o conteúdo da mensagem
        except (IndexError, AttributeError):
            return 'Sem resposta'
