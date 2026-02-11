import functools
import textwrap
from datetime import datetime
from abc import ABC, abstractmethod


# ================= DECORADOR =================

def log_transacao(func):
    """Decorador para registrar transações no sistema"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        data_hora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        classe = args[0].__class__.__name__ if args else 'Sistema'
        print(f'[LOG] {data_hora} - {classe}.{func.__name__}')
        return func(*args, **kwargs)
    return wrapper


# ================= MIXINS =================

class LogMixin:
    """Mixin para adicionar funcionalidade de log às classes"""
    
    def log(self, mensagem):
        data_hora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        print(f'[{self.__class__.__name__}] {data_hora} - {mensagem}')


class SerializacaoMixin:
    """Mixin para serializar objetos em formato legível"""
    
    def to_dict(self):
        """Converte o objeto em dicionário"""
        return {
            key: value for key, value in self.__dict__.items()
            if not key.startswith('_')
        }
    
    def __repr__(self):
        attrs = ', '.join(f'{k}={v}' for k, v in self.to_dict().items())
        return f'{self.__class__.__name__}({attrs})'


# ================= CLASSES BASE (TRANSAÇÕES) =================

class Transacao(ABC):
    """Classe abstrata base para transações"""
    
    @abstractmethod
    def registrar(self, conta):
        """Registra a transação em uma conta"""
        pass
    
    @abstractmethod
    def get_tipo(self):
        """Retorna o tipo da transação"""
        pass
    
    @abstractmethod
    def get_valor(self):
        """Retorna o valor da transação"""
        pass


class Deposito(Transacao, LogMixin):
    """Classe que representa um depósito"""
    
    def __init__(self, valor):
        self._valor = valor
    
    def get_tipo(self):
        return 'DEPÓSITO'
    
    def get_valor(self):
        return self._valor
    
    @log_transacao
    def registrar(self, conta):
        if self._valor <= 0:
            self.log(f'Falha no depósito: valor inválido R$ {self._valor:.2f}')
            print('❌ Operação falhou! Valor deve ser positivo.')
            return False
        
        conta._saldo += self._valor
        conta._historico.adicionar_transacao(self)
        self.log(f'Depósito de R$ {self._valor:.2f} realizado')
        print(f'✅ Depósito de R$ {self._valor:.2f} realizado com sucesso!')
        return True


class Saque(Transacao, LogMixin):
    """Classe que representa um saque"""
    
    def __init__(self, valor):
        self._valor = valor
    
    def get_tipo(self):
        return 'SAQUE'
    
    def get_valor(self):
        return self._valor
    
    @log_transacao
    def registrar(self, conta):
        if self._valor <= 0:
            self.log(f'Falha no saque: valor inválido R$ {self._valor:.2f}')
            print('❌ Operação falhou! Valor deve ser positivo.')
            return False
        
        if self._valor > conta._saldo:
            self.log('Falha no saque: saldo insuficiente')
            print('❌ Operação falhou! Saldo insuficiente.')
            return False
        
        if self._valor > conta._limite:
            self.log('Falha no saque: limite excedido')
            print(f'❌ Operação falhou! Limite de R$ {conta._limite:.2f} excedido.')
            return False
        
        numero_saques = conta.get_numero_saques_hoje()
        if numero_saques >= conta._limite_saques:
            self.log('Falha no saque: limite de saques diário excedido')
            print(f'❌ Operação falhou! Limite de {conta._limite_saques} saques diários excedido.')
            return False
        
        conta._saldo -= self._valor
        conta._historico.adicionar_transacao(self)
        self.log(f'Saque de R$ {self._valor:.2f} realizado')
        print(f'✅ Saque de R$ {self._valor:.2f} realizado com sucesso!')
        return True


# ================= HISTÓRICO =================

class Historico:
    """Classe para gerenciar o histórico de transações"""
    
    def __init__(self):
        self._transacoes = []
    
    def adicionar_transacao(self, transacao):
        """Adiciona uma transação ao histórico"""
        self._transacoes.append({
            'tipo': transacao.get_tipo(),
            'valor': transacao.get_valor(),
            'data': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        })
    
    def listar_transacoes(self):
        """Retorna todas as transações"""
        return self._transacoes
    
    def gerar_relatorio(self, tipo=None):
        """Gerador que filtra transações por tipo"""
        for transacao in self._transacoes:
            if tipo is None or transacao['tipo'] == tipo:
                yield transacao
    
    def __iter__(self):
        """Torna o histórico iterável"""
        return iter(self._transacoes)
    
    def __len__(self):
        """Retorna o número de transações"""
        return len(self._transacoes)


# ================= CLIENTE =================

class Cliente(LogMixin, SerializacaoMixin):
    """Classe que representa um cliente do banco"""
    
    def __init__(self, nome, cpf, data_nascimento, endereco):
        self._nome = nome
        self._cpf = cpf
        self._data_nascimento = data_nascimento
        self._endereco = endereco
        self._contas = []
    
    @property
    def nome(self):
        return self._nome
    
    @property
    def cpf(self):
        return self._cpf
    
    def adicionar_conta(self, conta):
        """Adiciona uma conta ao cliente"""
        self._contas.append(conta)
        self.log(f'Conta {conta.numero} adicionada ao cliente {self._nome}')
    
    def listar_contas(self):
        """Retorna todas as contas do cliente"""
        return self._contas
    
    def __str__(self):
        return f'{self._nome} (CPF: {self._cpf})'


# ================= CONTA =================

class Conta(LogMixin, SerializacaoMixin):
    """Classe que representa uma conta bancária"""
    
    def __init__(self, numero, agencia, cliente, limite=500, limite_saques=3):
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._saldo = 0
        self._limite = limite
        self._limite_saques = limite_saques
        self._historico = Historico()
    
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
    def saldo(self):
        return self._saldo
    
    @property
    def historico(self):
        return self._historico
    
    def get_numero_saques_hoje(self):
        """Conta quantos saques foram feitos hoje"""
        data_hoje = datetime.now().strftime('%d/%m/%Y')
        saques_hoje = 0
        
        for transacao in self._historico.listar_transacoes():
            if transacao['tipo'] == 'SAQUE' and transacao['data'].startswith(data_hoje):
                saques_hoje += 1
        
        return saques_hoje
    
    @log_transacao
    def depositar(self, valor):
        """Realiza um depósito na conta"""
        deposito = Deposito(valor)
        return deposito.registrar(self)
    
    @log_transacao
    def sacar(self, valor):
        """Realiza um saque da conta"""
        saque = Saque(valor)
        return saque.registrar(self)
    
    def exibir_extrato(self):
        """Exibe o extrato da conta"""
        print('\n' + '='*50)
        print(f'EXTRATO - Conta: {self._numero} | Agência: {self._agencia}'.center(50))
        print(f'Titular: {self._cliente.nome}'.center(50))
        print('='*50)
        
        if len(self._historico) == 0:
            print('Não foram realizadas movimentações.'.center(50))
        else:
            for transacao in self._historico:
                tipo = transacao['tipo']
                valor = transacao['valor']
                data = transacao['data']
                print(f"{data} | {tipo:<10} | R$ {valor:>10.2f}")
        
        print('-'*50)
        print(f"SALDO ATUAL: R$ {self._saldo:.2f}".rjust(50))
        print('='*50 + '\n')
    
    def __str__(self):
        return f'Conta {self._numero} - Ag: {self._agencia} - Titular: {self._cliente.nome} - Saldo: R$ {self._saldo:.2f}'


# ================= BANCO =================

class Banco(LogMixin):
    """Classe que gerencia o banco"""
    
    def __init__(self, nome):
        self._nome = nome
        self._clientes = []
        self._contas = []
        self._agencia_padrao = '0001'
    
    def buscar_cliente(self, cpf):
        """Busca um cliente pelo CPF"""
        for cliente in self._clientes:
            if cliente.cpf == cpf:
                return cliente
        return None
    
    @log_transacao
    def criar_cliente(self, nome, cpf, data_nascimento, endereco):
        """Cria um novo cliente"""
        if self.buscar_cliente(cpf):
            print('❌ Já existe cliente com esse CPF!')
            return None
        
        cliente = Cliente(nome, cpf, data_nascimento, endereco)
        self._clientes.append(cliente)
        self.log(f'Cliente {nome} criado com sucesso')
        print(f'✅ Cliente {nome} criado com sucesso!')
        return cliente
    
    @log_transacao
    def criar_conta(self, cpf):
        """Cria uma nova conta para um cliente"""
        cliente = self.buscar_cliente(cpf)
        
        if not cliente:
            print('❌ Cliente não encontrado!')
            return None
        
        numero_conta = len(self._contas) + 1
        conta = Conta(numero_conta, self._agencia_padrao, cliente)
        
        self._contas.append(conta)
        cliente.adicionar_conta(conta)
        
        self.log(f'Conta {numero_conta} criada para {cliente.nome}')
        print(f'✅ Conta {numero_conta} criada com sucesso!')
        return conta
    
    def listar_clientes(self):
        """Lista todos os clientes"""
        print('\n' + '='*50)
        print('CLIENTES DO BANCO'.center(50))
        print('='*50)
        
        if not self._clientes:
            print('Nenhum cliente cadastrado.'.center(50))
        else:
            for cliente in self._clientes:
                print(f'• {cliente}')
                contas = cliente.listar_contas()
                if contas:
                    for conta in contas:
                        print(f'  └─ Conta: {conta.numero} | Saldo: R$ {conta.saldo:.2f}')
        
        print('='*50 + '\n')
    
    def listar_contas(self):
        """Lista todas as contas usando iterador"""
        print('\n' + '='*50)
        print('CONTAS DO BANCO'.center(50))
        print('='*50)
        
        if not self._contas:
            print('Nenhuma conta cadastrada.'.center(50))
        else:
            for conta in ContaIterador(self._contas):
                print(f"Ag: {conta['agencia']} | Conta: {conta['numero']:04d} | "
                      f"Titular: {conta['titular']:<20} | Saldo: R$ {conta['saldo']:>10.2f}")
        
        print('='*50 + '\n')


# ================= ITERADOR =================

class ContaIterador:
    """Iterador para percorrer contas"""
    
    def __init__(self, contas):
        self._contas = contas
        self._index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index < len(self._contas):
            conta = self._contas[self._index]
            self._index += 1
            return {
                'agencia': conta.agencia,
                'numero': conta.numero,
                'titular': conta.cliente.nome,
                'saldo': conta.saldo
            }
        raise StopIteration


# ================= MENU =================

def menu():
    """Exibe o menu principal"""
    opcoes = """\n
    ╔════════════════════════════════════╗
    ║      SISTEMA BANCÁRIO - MENU       ║
    ╠════════════════════════════════════╣
    ║  [D]  Depositar                    ║
    ║  [S]  Sacar                        ║
    ║  [E]  Extrato                      ║
    ║  [NU] Novo Cliente                 ║
    ║  [NC] Nova Conta                   ║
    ║  [LC] Listar Contas                ║
    ║  [LU] Listar Clientes              ║
    ║  [R]  Relatório de Transações      ║
    ║  [Q]  Sair                         ║
    ╚════════════════════════════════════╝
    
    ➡️  Escolha uma opção: """
    return input(textwrap.dedent(opcoes)).upper()


# ================= MAIN =================

def main():
    """Função principal do sistema"""
    banco = Banco('Banco PyDIO')
    
    print('\n' + '='*50)
    print('BEM-VINDO AO SISTEMA BANCÁRIO'.center(50))
    print('='*50)
    
    while True:
        opcao = menu()
        
        if opcao == 'D':
            cpf = input('CPF do cliente: ')
            cliente = banco.buscar_cliente(cpf)
            
            if not cliente:
                print('❌ Cliente não encontrado!')
                continue
            
            contas = cliente.listar_contas()
            if not contas:
                print('❌ Cliente não possui contas!')
                continue
            
            if len(contas) > 1:
                print('\nContas disponíveis:')
                for i, conta in enumerate(contas, 1):
                    print(f'{i}. Conta {conta.numero} - Saldo: R$ {conta.saldo:.2f}')
                escolha = int(input('Escolha a conta: ')) - 1
                conta = contas[escolha]
            else:
                conta = contas[0]
            
            try:
                valor = float(input('Valor do depósito: R$ '))
                conta.depositar(valor)
            except ValueError:
                print('❌ Valor inválido!')
        
        elif opcao == 'S':
            cpf = input('CPF do cliente: ')
            cliente = banco.buscar_cliente(cpf)
            
            if not cliente:
                print('❌ Cliente não encontrado!')
                continue
            
            contas = cliente.listar_contas()
            if not contas:
                print('❌ Cliente não possui contas!')
                continue
            
            if len(contas) > 1:
                print('\nContas disponíveis:')
                for i, conta in enumerate(contas, 1):
                    print(f'{i}. Conta {conta.numero} - Saldo: R$ {conta.saldo:.2f}')
                escolha = int(input('Escolha a conta: ')) - 1
                conta = contas[escolha]
            else:
                conta = contas[0]
            
            try:
                valor = float(input('Valor do saque: R$ '))
                conta.sacar(valor)
            except ValueError:
                print('❌ Valor inválido!')
        
        elif opcao == 'E':
            cpf = input('CPF do cliente: ')
            cliente = banco.buscar_cliente(cpf)
            
            if not cliente:
                print('❌ Cliente não encontrado!')
                continue
            
            contas = cliente.listar_contas()
            if not contas:
                print('❌ Cliente não possui contas!')
                continue
            
            if len(contas) > 1:
                print('\nContas disponíveis:')
                for i, conta in enumerate(contas, 1):
                    print(f'{i}. Conta {conta.numero}')
                escolha = int(input('Escolha a conta: ')) - 1
                conta = contas[escolha]
            else:
                conta = contas[0]
            
            conta.exibir_extrato()
        
        elif opcao == 'NU':
            print('\n--- CADASTRO DE NOVO CLIENTE ---')
            nome = input('Nome completo: ')
            cpf = input('CPF (somente números): ')
            data_nascimento = input('Data de nascimento (dd/mm/aaaa): ')
            endereco = input('Endereço completo: ')
            
            banco.criar_cliente(nome, cpf, data_nascimento, endereco)
        
        elif opcao == 'NC':
            cpf = input('CPF do cliente: ')
            banco.criar_conta(cpf)
        
        elif opcao == 'LC':
            banco.listar_contas()
        
        elif opcao == 'LU':
            banco.listar_clientes()
        
        elif opcao == 'R':
            cpf = input('CPF do cliente: ')
            cliente = banco.buscar_cliente(cpf)
            
            if not cliente:
                print('❌ Cliente não encontrado!')
                continue
            
            contas = cliente.listar_contas()
            if not contas:
                print('❌ Cliente não possui contas!')
                continue
            
            if len(contas) > 1:
                print('\nContas disponíveis:')
                for i, conta in enumerate(contas, 1):
                    print(f'{i}. Conta {conta.numero}')
                escolha = int(input('Escolha a conta: ')) - 1
                conta = contas[escolha]
            else:
                conta = contas[0]
            
            print('\n' + '='*50)
            print('RELATÓRIO DE TRANSAÇÕES'.center(50))
            print('='*50)
            
            tipo_filtro = input('Filtrar por tipo? (D=Depósito, S=Saque, Enter=Todos): ').upper()
            tipo = None
            if tipo_filtro == 'D':
                tipo = 'DEPÓSITO'
            elif tipo_filtro == 'S':
                tipo = 'SAQUE'
            
            for transacao in conta.historico.gerar_relatorio(tipo):
                print(f"{transacao['data']} | {transacao['tipo']:<10} | R$ {transacao['valor']:>10.2f}")
            
            print('='*50 + '\n')
        
        elif opcao == 'Q':
            print('\n' + '='*50)
            print('OBRIGADO POR USAR NOSSO SISTEMA!'.center(50))
            print('='*50 + '\n')
            break
        
        else:
            print('❌ Opção inválida! Tente novamente.')


if __name__ == '__main__':
    main()