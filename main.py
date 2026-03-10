from database import create_table
from models import create_user, get_users, update_user, delete_user


def menu():
    while True:
        print("\n=== CRUD de Usuários ===")
        print("1 - Cadastrar")
        print("2 - Listar")
        print("3 - Atualizar")
        print("4 - Deletar")
        print("0 - Sair")

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            nome = input("Nome: ").strip()
            email = input("Email: ").strip()

            if nome and email:
                create_user(nome, email)
                print("Usuário cadastrado com sucesso.")
            else:
                print("Nome e email são obrigatórios.")

        elif opcao == "2":
            usuarios = get_users()
            if not usuarios:
                print("Nenhum usuário cadastrado.")
            else:
                for user in usuarios:
                    print(f"ID: {user[0]} | Nome: {user[1]} | Email: {user[2]}")

        elif opcao == "3":
            try:
                user_id = int(input("ID do usuário: "))
                nome = input("Novo nome: ").strip()
                email = input("Novo email: ").strip()

                updated = update_user(user_id, nome, email)
                if updated:
                    print("Usuário atualizado com sucesso.")
                else:
                    print("Usuário não encontrado.")
            except ValueError:
                print("ID inválido.")

        elif opcao == "4":
            try:
                user_id = int(input("ID do usuário: "))
                deleted = delete_user(user_id)

                if deleted:
                    print("Usuário deletado com sucesso.")
                else:
                    print("Usuário não encontrado.")
            except ValueError:
                print("ID inválido.")

        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    create_table()
    menu()