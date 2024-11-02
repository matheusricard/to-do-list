import json
from datetime import datetime
from colorama import Fore, Style, init

# Inicializa o colorama para colorir o terminal
init()

# Lista de tarefas
tasks = []

# --- Funções de Utilidade ---

# Função para exibir o menu
def show_menu():
    print("\n--- Gerenciador de Tarefas ---")
    print("1. Adicionar Tarefa")
    print("2. Visualizar Tarefas")
    print("3. Marcar Tarefa como Concluída")
    print("4. Remover Tarefa")
    print("5. Editar Tarefa")
    print("6. Visualizar Tarefas por Prioridade ou Prazo")
    print("7. Sair")

# Função para adicionar uma tarefa com prazo e prioridade
def add_task():
    task_name = input("Digite a nova tarefa: ")
    deadline = input("Digite a data de prazo (YYYY-MM-DD): ")
    priority = input("Defina a prioridade (Alta, Média, Baixa): ")
    task = {
        "nome": task_name,
        "concluida": False,
        "criado_em": datetime.now().strftime("%Y-%m-%d"),
        "prazo": deadline,
        "prioridade": priority
    }
    tasks.append(task)
    print("Tarefa adicionada com sucesso!")

# Função para exibir as tarefas com cores
def view_tasks(filter_by=None):
    if not tasks:
        print("Nenhuma tarefa disponível.")
    else:
        filtered_tasks = tasks if filter_by is None else [task for task in tasks if task["concluida"] == filter_by]
        print("\nTarefas:")
        for i, task in enumerate(filtered_tasks):
            status = "Concluída" if task["concluida"] else "Pendente"
            color = Fore.GREEN if task["concluida"] else Fore.YELLOW
            prioridade = task.get("prioridade", "Não definida")
            print(f"{color}{i + 1}. {task['nome']} - {status} - Prazo: {task['prazo']} - Prioridade: {prioridade}{Style.RESET_ALL}")

# Função para marcar uma tarefa como concluída
def mark_task_completed():
    view_tasks()
    try:
        task_num = int(input("Digite o número da tarefa a ser marcada como concluída: ")) - 1
        if 0 <= task_num < len(tasks):
            tasks[task_num]["concluida"] = True
            print("Tarefa marcada como concluída!")
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada inválida. Digite um número.")

# Função para remover uma tarefa
def remove_task():
    view_tasks()
    try:
        task_num = int(input("Digite o número da tarefa a ser removida: ")) - 1
        if 0 <= task_num < len(tasks):
            tasks.pop(task_num)
            print("Tarefa removida!")
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada inválida. Digite um número.")

# Função para editar uma tarefa
def edit_task():
    view_tasks()
    try:
        task_num = int(input("Digite o número da tarefa que deseja editar: ")) - 1
        if 0 <= task_num < len(tasks):
            new_name = input("Digite o novo nome da tarefa ou pressione Enter para manter o atual: ")
            new_deadline = input("Digite o novo prazo (YYYY-MM-DD) ou pressione Enter para manter o atual: ")
            new_priority = input("Digite a nova prioridade (Alta, Média, Baixa) ou pressione Enter para manter a atual: ")

            if new_name:
                tasks[task_num]["nome"] = new_name
            if new_deadline:
                tasks[task_num]["prazo"] = new_deadline
            if new_priority:
                tasks[task_num]["prioridade"] = new_priority
            print("Tarefa atualizada com sucesso!")
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada inválida. Digite um número.")

# Função para salvar as tarefas em um arquivo JSON
def save_tasks():
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)

# Função para carregar as tarefas de um arquivo JSON
def load_tasks():
    global tasks
    try:
        with open("tasks.json", "r") as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = []

# Função para organizar e exibir tarefas por prazo ou prioridade
def view_tasks_sorted(by="prazo"):
    sorted_tasks = sorted(tasks, key=lambda x: x.get(by, ""))
    print("\nTarefas ordenadas:")
    for i, task in enumerate(sorted_tasks):
        status = "Concluída" if task["concluida"] else "Pendente"
        color = Fore.GREEN if task["concluida"] else Fore.YELLOW
        print(f"{color}{i + 1}. {task['nome']} - {status} - Prazo: {task['prazo']} - Prioridade: {task['prioridade']}{Style.RESET_ALL}")

# --- Programa Principal ---

def main():
    load_tasks()
    while True:
        show_menu()
        option = input("Escolha uma opção: ")
        
        if option == "1":
            add_task()
            save_tasks()
        elif option == "2":
            view_tasks()
        elif option == "3":
            mark_task_completed()
            save_tasks()
        elif option == "4":
            remove_task()
            save_tasks()
        elif option == "5":
            edit_task()
            save_tasks()
        elif option == "6":
            sort_option = input("Deseja ordenar por 'prazo' ou 'prioridade'? ").strip().lower()
            if sort_option in ["prazo", "prioridade"]:
                view_tasks_sorted(by=sort_option)
            else:
                print("Opção inválida. Ordenando por prazo.")
                view_tasks_sorted()
        elif option == "7":
            print("Saindo...")
            save_tasks()
            break
        else:
            print("Opção inválida. Tente novamente.")

# Iniciar o programa
if __name__ == "__main__":
    main()
