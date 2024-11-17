from database import MySQLDatabase
from groq_integration import GroqClient

class DataApplication:
    def __init__(self):
        self.db = MySQLDatabase()
        self.groq_client = GroqClient()

    def run(self):
        self.db.connect()

        # Executa o SELECT fornecido
        select_query = """
        SELECT
    a.serie,
    a.periodo,
    a.genero,
    a.idade,
    a.fkInstituicao,
    i.nome_departamento AS instituicao_nome,
    i.distrito_estadual,
    i.municipio,
    i.regiao_metropolitana,
    d.nome_disciplina,
    na.nota,
    CASE 
        WHEN na.nota >= 90 THEN 'Excelente'
        WHEN na.nota >= 75 THEN 'Bom'
        WHEN na.nota >= 50 THEN 'Satisfatório'
        ELSE 'Insatisfatório'
    END AS desempenho,
    AVG(na.nota) OVER (PARTITION BY a.codAluno) AS media_aluno,
    AVG(na.nota) OVER (PARTITION BY a.serie) AS media_serie,
    AVG(na.nota) OVER (PARTITION BY d.idDisciplina) AS media_disciplina
FROM 
    aluno a
JOIN 
    instituicao i ON a.fkInstituicao = i.codInstituicao
JOIN 
    notas_aluno na ON a.codAluno = na.fkAluno
JOIN 
    disciplina d ON na.fkDisciplina = d.idDisciplina
ORDER BY 
    a.serie, a.codAluno, d.nome_disciplina;
"""
        results = self.db.execute_select(select_query)

        if results:
            # Exemplo de como usar o primeiro resultado como uma pergunta para a GroqIA
            question = f"{results[0][0]}, Série {results[0][1]}, Disciplina: {results[0][9]}, Nota: {results[0][10]}, Desempenho: {results[0][11]}, Média do Aluno: {results[0][12]}, Média da Série: {results[0][13]}, Média da Disciplina: {results[0][14]}"
            print(f'{question}')
            # Pergunta à GroqIA
            print("IA Analisando os dados")
            response = self.groq_client.ask_question(question)

            # Salva a resposta no banco de dados
            print("Salvando no banco de dados")
            insert_query = "INSERT INTO nexus_ia (resposta) VALUES (%s)"
            self.db.execute_insert(insert_query, (response,))

        self.db.close()

if __name__ == "__main__":
    app = DataApplication()
    app.run()
