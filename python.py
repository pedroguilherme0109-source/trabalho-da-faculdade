"""
Sistema simples de gerenciamento escolar.

Entidades:
- Escola: nome, CNPJ, salas e professores; pode criar salas, associar professores
  e gerar um relatório.
- SalaDeAula: número, capacidade e bloco; pode verificar disponibilidade e
  receber uma turma.
- Professor: nome, CPF e especialidade; pode ministrar aulas e ser associado
  a várias escolas.
- Aluno: matrícula, nome e endereço; pode alterar o endereço, matricular-se
  em disciplinas e consultar notas.
- Endereco: rua, número, bairro e cidade; pode ser atualizado e formatado.

Relacionamentos:
- Escola e SalaDeAula: composição. A sala é criada e mantida pela escola e não
  tem significado no sistema sem ela.
- Escola e Professor: associação muitos-para-muitos. Ambos existem
  independentemente; não há relação de parte-todo.
- Aluno e Endereco: agregação. O endereço é criado no cadastro do aluno, mas
  pode ser separado, preservado e transferido para outro contexto.

Diagrama UML (Mermaid):

classDiagram
    Escola "1" *-- "1..*" SalaDeAula : possui
    Escola "0..*" -- "0..*" Professor : leciona em
    Aluno "0..1" o-- "0..1" Endereco : possui
"""

from __future__ import annotations


class Endereco:
    def __init__(self, rua: str, numero: str, bairro: str, cidade: str) -> None:
        self.rua = rua
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade

    def atualizar_endereco(
        self, rua: str, numero: str, bairro: str, cidade: str
    ) -> None:
        self.rua = rua
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade

    def formatar_endereco(self) -> str:
        return f"{self.rua}, {self.numero} - {self.bairro}, {self.cidade}"


class Aluno:
    def __init__(
        self,
        matricula: str,
        nome: str,
        rua: str,
        numero: str,
        bairro: str,
        cidade: str,
    ) -> None:
        self.matricula = matricula
        self.nome = nome
        self.endereco: Endereco | None = Endereco(rua, numero, bairro, cidade)
        self.disciplinas: list[str] = []
        self.notas: dict[str, list[float]] = {}

    def matricular_disciplina(self, disciplina: str) -> None:
        if disciplina not in self.disciplinas:
            self.disciplinas.append(disciplina)

    def registrar_nota(self, disciplina: str, nota: float) -> None:
        if disciplina not in self.disciplinas:
            raise ValueError(f"O aluno não está matriculado em {disciplina}.")
        if not 0 <= nota <= 10:
            raise ValueError("A nota deve estar entre 0 e 10.")
        self.notas.setdefault(disciplina, []).append(nota)

    def consultar_notas(self) -> dict[str, list[float]]:
        return {disciplina: notas.copy() for disciplina, notas in self.notas.items()}

    def atualizar_endereco(
        self, rua: str, numero: str, bairro: str, cidade: str
    ) -> None:
        if self.endereco is None:
            self.endereco = Endereco(rua, numero, bairro, cidade)
        else:
            self.endereco.atualizar_endereco(rua, numero, bairro, cidade)

    def liberar_endereco(self) -> Endereco:
        if self.endereco is None:
            raise ValueError("Este aluno não possui um endereço associado.")
        endereco = self.endereco
        self.endereco = None
        return endereco

    def definir_endereco(self, endereco: Endereco) -> None:
        self.endereco = endereco


class SalaDeAula:
    def __init__(self, numero: int, capacidade: int, bloco: str) -> None:
        if capacidade <= 0:
            raise ValueError("A capacidade da sala deve ser maior que zero.")
        self.numero = numero
        self.capacidade = capacidade
        self.bloco = bloco
        self.turma_alocada: str | None = None

    def alocar_turma(self, turma: str, quantidade_alunos: int) -> None:
        if not self.verificar_disponibilidade():
            raise ValueError("A sala já possui uma turma alocada.")
        if quantidade_alunos > self.capacidade:
            raise ValueError("A turma excede a capacidade da sala.")
        if quantidade_alunos < 0:
            raise ValueError("A quantidade de alunos não pode ser negativa.")
        self.turma_alocada = turma

    def verificar_disponibilidade(self) -> bool:
        return self.turma_alocada is None


class Professor:
    def __init__(self, nome: str, cpf: str, especialidade: str) -> None:
        self.nome = nome
        self.cpf = cpf
        self.especialidade = especialidade
        self.escolas: list[Escola] = []

    def ministrar_aula(self, disciplina: str) -> str:
        return f"{self.nome} está ministrando {disciplina}."

    def vincular_escola(self, escola: Escola) -> None:
        escola.adicionar_professor(self)


class Escola:
    def __init__(self, nome: str, cnpj: str) -> None:
        self.nome = nome
        self.cnpj = cnpj
        self.salas: list[SalaDeAula] = []
        self.professores: list[Professor] = []

    def adicionar_sala(
        self, numero: int, capacidade: int, bloco: str = "A"
    ) -> SalaDeAula:
        if any(sala.numero == numero and sala.bloco == bloco for sala in self.salas):
            raise ValueError(f"A sala {numero} do bloco {bloco} já existe.")
        sala = SalaDeAula(numero, capacidade, bloco)
        self.salas.append(sala)
        return sala

    def contratar_professor(self, professor: Professor) -> None:
        self.adicionar_professor(professor)

    def adicionar_professor(self, professor: Professor) -> None:
        if professor not in self.professores:
            self.professores.append(professor)
        if self not in professor.escolas:
            professor.escolas.append(self)

    def obter_relatorio(self) -> str:
        return (
            f"Escola: {self.nome}\n"
            f"CNPJ: {self.cnpj}\n"
            f"Salas: {len(self.salas)}\n"
            f"Professores: {len(self.professores)}"
        )


if __name__ == "__main__":
    escola = Escola("Escola Exemplo", "00.000.000/0001-00")
    sala = escola.adicionar_sala(101, 30, "A")

    professor = Professor("Ana Silva", "000.000.000-00", "Matemática")
    escola.contratar_professor(professor)

    aluno = Aluno("2026-001", "João Souza", "Rua Central", "123", "Centro", "São Paulo")
    aluno.matricular_disciplina("Matemática")
    aluno.registrar_nota("Matemática", 9.5)

    sala.alocar_turma("1º ano", 25)

    print(escola.obter_relatorio())
    print(professor.ministrar_aula("Matemática"))
    print(f"Endereço de {aluno.nome}: {aluno.endereco is None and 'Não possui endereço' or aluno.endereco.formatar_endereco()}")
    print(f"Notas de {aluno.nome}: {aluno.consultar_notas()}")
