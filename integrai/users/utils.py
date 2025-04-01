import re


def is_valid_name_and_email(message):

    # Remover espaços antes e depois da string
    message = message.strip()

    # Verificar se a mensagem contém exatamente uma vírgula
    if message.count(',') != 1:
        print("Formato inválido: a mensagem deve conter exatamente uma vírgula.")
        return None

    # Separar a mensagem em nome e email
    name, email = message.split(',', 1)
    name = name.strip()
    email = email.strip()

    # Validar o email
    if not is_valid_email(email):
        print(f"Email inválido: {email}")
        return None

    # Verificar se o nome e o email não estão vazios
    if not name or not email:
        print("Nome ou email não podem estar vazios.")
        return None

    return [name, email]


def is_valid_email(email):
    """
    Valida se o email possui uma estrutura mínima válida.

    :param email: O email a ser validado
    :return: True se o email for válido, False caso contrário
    """
    # Expressão regular simples para verificar se o email contém @ e .
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    return bool(re.match(email_regex, email))


def ranking():
    from .models import User
    # Obtém todos os usuários ordenados pelo quiz_score em ordem decrescente
    users = User.objects.all().order_by('-quiz_score')[:10]  # Pega os 10 melhores usuários

    # Formata o ranking como uma string
    ranking_string = "🏆 *Ranking dos Melhores Jogadores*\n\n"

    for posicao, user in enumerate(users, start=1):
        ranking_string += f"{posicao} - {user.name} - {user.quiz_score}\n\n"

    return ranking_string


