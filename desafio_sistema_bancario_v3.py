from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
import textwrap

class Conta:
    def __init__(self,  numero,  cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_limite_saldo = valor > saldo     
         
        if excedeu_limite_saldo:
            print("\n Operação inválida, você não possui saldo suficiente!")
             
        elif valor > 0:
            self._saldo -= valor
            print("\n Saque realizado com sucesso!  O seu novo saldo é: R$", self.saldo)
            return True

        else:
            print("\n Operação falhou, o valor é inválido!") 
            
        return False

    def depositar(self, valor):   
        if valor > 0:
            self._saldo += valor
            print("Depósito feito com sucesso! O seu novo saldo é: R$", self.saldo)
            return True
        
        else:
            print("O depósito falhou! Insira um valor válido para o depósito!")
            return False


class Conta_Corrente(Conta):
    def __init__(self,  numero,  cliente, limite = 500, limite_saques = 3):
        super().__init__( numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes
             if transacao["tipo"] == "Saque"]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n Operação inválida! O limite por saque é R$ 500.00")

        elif excedeu_saques:
            print("\n Número diário de saques atingido! Retorne amanhã!")

        else:
            return super().sacar(valor)

        return False
    
    def __str__(self):
        return f"""
            Agência:\t{self.agencia}
            Titular:\t{self.cliente.nome}
        """

class Cliente():
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas_usuarios = []

    def transacao(self, conta, transacao):
        transacao.registrar(conta)

    def add_conta(self, conta):
        self.contas_usuarios.append(conta)    


class Pessoa_Fisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

class Historico():
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def add_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
            }
        )


class Transacao(ABC):
    @property 
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        registrar_transacao = conta.sacar(self.valor)

        if registrar_transacao:
            conta.historico.add_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        registrar_transacao = conta.depositar(self.valor)

        if registrar_transacao:
            conta.historico.add_transacao(self)

def menu():
    menu = """ \n

    [1]\t Depositar
    [2]\t Sacar
    [3]\t Extrato
    [4]\t Nova conta
    [5]\t Novo usuário
    [6]\t Lista total de contas
    [0]\t Sair

    => """

    return input(textwrap.dedent(menu))

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None
    
def acessar_conta_cliente(cliente):
    if not cliente.contas_usuarios:
        print("\n Conta não encontrada!")
    else:
        return cliente.contas_usuarios[0]   

def depositar(clientes):
    cpf = input("Informe o seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Usuário não encontrado!")
        return
    
    valor_deposito = float(input("Digite o quanto deseja depositar: "))
    transacao = Deposito(valor_deposito)

    conta = acessar_conta_cliente(cliente)
    if not conta:
        print("Conta não encontrada")
        return
    
    cliente.transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Usuário não encontrado!")
        return
    
    valor_saque = float(input("Digite o quanto deseja sacar: "))
    transacao = Saque(valor_saque)

    conta = acessar_conta_cliente(cliente)
    if not conta:
        print("Conta não encontrada")
        return
    
    cliente.transacao(conta, transacao)

def extrato(clientes):
    cpf = input("Informe o seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Usuário não encontrado!")
        return
    
    conta = acessar_conta_cliente(cliente)
    if not conta:
        print("Conta não encontrada!")
        return
    
    print("\n*****Veja o seu extrato a seguir*****")
    extrato_transacoes = conta.historico.transacoes

    extrato_cliente = ""
    if not extrato_transacoes:
        extrato_cliente = print("Não houveram transações")
    else:
        for transacao in extrato_transacoes:
            extrato_cliente += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato_cliente)  
    print(f"O seu saldo é:\n\tR$ {conta.saldo:.2f}")          

def novo_cliente(clientes):
    cpf = input("Informe o seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("Usuário com esse CPF já foi encontrado!")
        return
    
    nome = input("Digite o seu nome: ")
    data_nascimento = input("Informe a sua data de nascimento: ")
    endereco = input("Informe sua cidade, bairro, rua e estado: ")

    cliente = Pessoa_Fisica(nome=nome, cpf=cpf, data_nascimento=data_nascimento,  endereco=endereco)
    clientes.append(cliente)

    print("Usuário cadastrado no nosso sistema!")

def nova_conta(num_conta, clientes, contas_usuarios):
    cpf = input("Informe o seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Usuário não encontrado!")
        return
    
    conta = Conta_Corrente.nova_conta(cliente=cliente, numero=num_conta)
    contas_usuarios.append(conta)
    cliente.contas_usuarios.append(conta)

    print("Conta criada com sucesso!")

def lista_de_contas(contas_usuarios):
    print("Olá! Segue o registro de todas as contas cadastradas no sistema")
    for conta in contas_usuarios:
        print(textwrap.dedent(str(conta)))


def main():
    clientes_banco = []
    contas_usuarios = []

    while True:
        opcao = menu()

        if opcao == "1":
           depositar(clientes_banco)
            
        elif opcao == "2":
            sacar(clientes_banco)
                    
        elif opcao == "3":
           extrato(clientes_banco)

        elif opcao == "4":
            num_contas = len(contas_usuarios) + 1
            nova_conta(num_contas, clientes_banco, contas_usuarios)
                              
        elif opcao == "5":
            novo_cliente(clientes_banco)

        elif opcao == "6":
            lista_de_contas(contas_usuarios)      
        
        elif opcao == "0":
            break
      
        else:
            print("Operação inválida!") 

main()          