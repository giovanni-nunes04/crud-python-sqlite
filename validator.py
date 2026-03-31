import re

class Validar:

    @staticmethod
    def nome(nome: str) -> bool:
        if not nome:
            return False
        return bool(re.fullmatch(r'[A-Za-zÀ-ÿ\s]+', nome.strip()))

    @staticmethod
    def endereco(endereco: str) -> bool:
        if not endereco:
            return False
        return bool(re.fullmatch(r'^[A-Za-zÀ-ÿ0-9\s,.\-]+$', endereco.strip()))

    @staticmethod
    def rg(rg: str) -> bool:
        if not rg:
            return False
        return bool(re.fullmatch(r'\d{7,9}', rg.strip()))

    @staticmethod
    def cpf(cpf: str) -> bool:
        if not cpf:
            return False
        return bool(re.fullmatch(r'^\d{11}$', cpf.strip()))

    @staticmethod
    def telefone(telefone: str) -> bool:
        if not telefone:
            return False
        return bool(re.fullmatch(r'\d{8,15}', telefone.strip()))

    @staticmethod
    def email(email: str) -> bool:
        if not email:
            return False
        return bool(re.fullmatch(r'[^@]+@[^@]+\.[^@]+', email.strip()))

    @staticmethod
    def senha(senha: str) -> bool:
        """Mínimo 8 caracteres, ao menos 1 maiúscula, 1 minúscula e 1 dígito."""
        if not senha:
            return False
        return bool(re.fullmatch(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$', senha.strip()))

    @staticmethod
    def cargo(cargo: str) -> bool:
        if not cargo:
            return False
        return bool(re.fullmatch(r'^[A-Za-zÀ-ÿ0-9\s]+$', cargo.strip()))

    @staticmethod
    def texto_livre(valor: str) -> bool:
        """Valida campos de texto geral (tarefa, local, funcao…)."""
        return bool(valor and valor.strip())

    @staticmethod
    def prioridade(valor: str) -> bool:
        return valor in ("baixa", "media", "alta")

    @staticmethod
    def status_tarefa(valor: str) -> bool:
        return valor in ("pendente", "em andamento", "concluida", "cancelada")

    @classmethod
    def funcionario(cls, data: dict) -> list[str]:
        erros = []

        regras = {
            "nome":     (cls.nome,     "Nome inválido (somente letras e espaços)."),
            "rg":       (cls.rg,       "RG inválido (somente dígitos, 7-9 caracteres)."),
            "cpf":      (cls.cpf,      "CPF inválido (somente 11 dígitos)."),
            "telefone": (cls.telefone, "Telefone inválido (8-15 dígitos)."),
            "email":    (cls.email,    "E-mail inválido."),
            "cargo":    (cls.cargo,    "Cargo inválido (letras e números)."),
            "endereco": (cls.endereco, "Endereço inválido."),
            "senha":    (cls.senha,    "Senha fraca (mín. 8 chars, maiúscula, minúscula e número)."),
            "dt_criacao": (cls.texto_livre, "Data de criação obrigatória."),
        }

        for campo, (fn, msg) in regras.items():
            valor = data.get(campo, "")
            if not fn(valor):
                erros.append(f"Campo '{campo}': {msg}")

        return erros

    @classmethod
    def tarefa(cls, data: dict) -> list[str]:
        """
        Valida todos os campos de uma tarefa.
        Retorna lista de erros; lista vazia = dados válidos.
        """
        erros = []

        campos_texto = ["funcionario", "funcao", "local",
                        "tarefa", "inicio_dt", "termino_dt",
                        "responsavel_registro", "dt_criacao"]

        for campo in campos_texto:
            if not cls.texto_livre(data.get(campo, "")):
                erros.append(f"Campo '{campo}' é obrigatório.")

        prioridade = data.get("prioridade", "")
        if not cls.prioridade(prioridade):
            erros.append("Campo 'prioridade' deve ser: baixa, media ou alta.")

        status = data.get("status", "")
        if not cls.status_tarefa(status):
            erros.append("Campo 'status' deve ser: pendente, em andamento, concluida ou cancelada.")

        return erros