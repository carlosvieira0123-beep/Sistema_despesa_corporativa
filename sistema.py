# Projeto integrador - Gestão de TI

import csv
import json
import os

ARQUIVO = "despesas.csv"


# Carrega as despesas salvas no arquivo CSV.
def carregar_despesas():
    despesas = []

    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8", newline="") as arquivo:
            leitor = csv.DictReader(arquivo)

            for linha in leitor:
                linha["codigo"] = int(linha["codigo"])
                linha["valor"] = float(linha["valor"])
                despesas.append(linha)

        return despesas

    # Se existir o arquivo antigo, importa os dados para o CSV.
    if os.path.exists("dados.json"):
        with open("dados.json", "r", encoding="utf-8") as arquivo:
            despesas = json.load(arquivo)

        salvar_despesas(despesas)
        return despesas

    return []


# Salva as despesas no arquivo CSV.
def salvar_despesas(despesas):
    campos = ["codigo", "funcionario", "viagem", "data", "categoria",
              "descricao", "valor", "status"]

    with open(ARQUIVO, "w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(despesas)


# Gera o próximo código de despesa.
def gerar_codigo(despesas):
    if len(despesas) == 0:
        return 1001

    maior = 1000
    for despesa in despesas:
        if despesa["codigo"] > maior:
            maior = despesa["codigo"]

    return maior + 1


# Pede um texto e não aceita o campo vazio.
def ler_texto(mensagem):
    while True:
        texto = input(mensagem).strip()
        if texto != "":
            return texto
        print("ERRO: este campo não pode ficar vazio.")


# Recebe e confere a data.
def ler_data():
    while True:
        data = input("Data DD/MM/AAAA: ").strip()

        if len(data) == 8 and data.isdigit():
            data = data[:2] + "/" + data[2:4] + "/" + data[4:]

        partes = data.split("/")

        if len(partes) == 3:
            dia = partes[0]
            mes = partes[1]
            ano = partes[2]

            if len(dia) == 2 and len(mes) == 2 and len(ano) == 4:
                if dia.isdigit() and mes.isdigit() and ano.isdigit():
                    dia = int(dia)
                    mes = int(mes)
                    ano = int(ano)

                    if 1 <= mes <= 12:
                        dias = [31, 29 if ano % 4 == 0 else 28, 31, 30, 31, 30,
                                31, 31, 30, 31, 30, 31]
                        if 1 <= dia <= dias[mes - 1]:
                            return f"{dia:02d}/{mes:02d}/{ano}"

        print("ERRO: informe uma data válida.")


# Recebe e confere o valor da despesa.
def ler_valor():
    while True:
        entrada = input("Valor da despesa: R$ ").replace(",", ".")
        try:
            valor = float(entrada)
            if valor > 0:
                return valor
            print("ERRO: o valor deve ser maior que zero.")
        except ValueError:
            print("ERRO: informe um valor válido.")


# Cadastra uma nova despesa.
def cadastrar_despesa(despesas):
    print("\n--- CADASTRO DE DESPESA ---")
    funcionario = ler_texto("Funcionário: ")
    viagem = ler_texto("Viagem: ")
    data = ler_data()
    categoria = ler_texto("Categoria: ")
    descricao = ler_texto("Descrição: ")
    valor = ler_valor()

    codigo = gerar_codigo(despesas)

    despesa = {
        "codigo": codigo,
        "funcionario": funcionario,
        "viagem": viagem,
        "data": data,
        "categoria": categoria,
        "descricao": descricao,
        "valor": valor,
        "status": "Pendente"
    }

    despesas.append(despesa)
    salvar_despesas(despesas)

    print("\nDespesa cadastrada com sucesso!")
    print("Código:", codigo)
    print("Status: Pendente")


# Mostra todas as despesas cadastradas.
def listar_despesas(despesas):
    print("\n--- DESPESAS CADASTRADAS ---")
    if len(despesas) == 0:
        print("Nenhuma despesa cadastrada.")
        return

    for despesa in despesas:
        print(
            despesa["codigo"],
            "|", despesa["funcionario"],
            "|", despesa["categoria"],
            "| R$", f"{despesa['valor']:.2f}",
            "|", despesa["status"]
        )


# Busca uma despesa pelo código.
def buscar_despesa(despesas):
    print("\n--- BUSCAR DESPESA ---")
    if len(despesas) == 0:
        print("Nenhuma despesa cadastrada.")
        return

    codigo = input("Digite o código da despesa: ")
    if not codigo.isdigit():
        print("ERRO: informe um código numérico.")
        return

    codigo = int(codigo)
    for despesa in despesas:
        if despesa["codigo"] == codigo:
            print("\nDespesa encontrada:")
            print("Código:", despesa["codigo"])
            print("Funcionário:", despesa["funcionario"])
            print("Viagem:", despesa["viagem"])
            print("Data:", despesa["data"])
            print("Categoria:", despesa["categoria"])
            print("Descrição:", despesa["descricao"])
            print("Valor: R$", f"{despesa['valor']:.2f}")
            print("Status:", despesa["status"])
            return

    print("Despesa não encontrada.")


# Mostra um resumo das despesas.
def relatorio_despesas(despesas):
    print("\n--- RELATÓRIO DE DESPESAS ---")
    if len(despesas) == 0:
        print("Nenhuma despesa cadastrada.")
        return

    total = 0
    maior = despesas[0]
    menor = despesas[0]
    totais_funcionarios = {}

    for despesa in despesas:
        valor = despesa["valor"]
        total = total + valor

        if valor > maior["valor"]:
            maior = despesa
        if valor < menor["valor"]:
            menor = despesa

        funcionario = despesa["funcionario"]
        if funcionario not in totais_funcionarios:
            totais_funcionarios[funcionario] = 0
        totais_funcionarios[funcionario] = totais_funcionarios[funcionario] + valor

    media = total / len(despesas)

    print("Total de despesas:", len(despesas))
    print("Valor total: R$", f"{total:.2f}")
    print("Valor médio: R$", f"{media:.2f}")

    print("\nMaior despesa:")
    print("Código:", maior["codigo"])
    print("Funcionário:", maior["funcionario"])
    print("Valor: R$", f"{maior['valor']:.2f}")

    print("\nMenor despesa:")
    print("Código:", menor["codigo"])
    print("Funcionário:", menor["funcionario"])
    print("Valor: R$", f"{menor['valor']:.2f}")

    print("\nTotal por funcionário:")
    for funcionario in totais_funcionarios:
        print(funcionario, ": R$", f"{totais_funcionarios[funcionario]:.2f}")


# Mostra as opções do programa.
def menu():
    print("\n======================================")
    print("   SISTEMA DE CONTROLE DE REEMBOLSOS")
    print("======================================")
    print("1 - Cadastrar despesa")
    print("2 - Listar despesas")
    print("3 - Buscar despesa")
    print("4 - Relatório")
    print("5 - Sair")


# Controla o funcionamento do programa.
def main():
    despesas = carregar_despesas()

    print("\nSistema de despesas corporativa - Gestão de TI")
    print("Sistema iniciado.")
    print(len(despesas), "despesa(s) carregada(s).")

    while True:
        menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_despesa(despesas)
        elif opcao == "2":
            listar_despesas(despesas)
        elif opcao == "3":
            buscar_despesa(despesas)
        elif opcao == "4":
            relatorio_despesas(despesas)
        elif opcao == "5":
            print("Sistema encerrado.")
            break
        else:
            print("ERRO: opção inválida.")


main()
