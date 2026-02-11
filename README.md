# Sistema Bancário em Python

> Um sistema bancário completo desenvolvido em Python que demonstra conceitos avançados de POO, incluindo classes abstratas, mixins, decoradores e padrões de projeto. Simula operações reais como depósitos, saques, extratos e gerenciamento de contas com validações e histórico completo de transações.

Fala dev! Esse é um projeto de sistema bancário que simula operações reais de um banco. Foi feito para praticar conceitos avançados de Programação Orientada a Objetos em Python, mas de um jeito que você consegue entender o que tá rolando.

## O que esse projeto faz?

Imagina um banco de verdade, mas no terminal. Você pode:

- Criar clientes com CPF, nome, endereço e tudo mais
- Abrir contas bancárias para esses clientes
- Fazer depósitos e saques (com validações, claro)
- Consultar extratos detalhados
- Ver relatórios de transações filtrados
- Listar todos os clientes e contas

E o melhor: tudo isso seguindo boas práticas de programação e com logs automáticos de tudo que acontece no sistema.

## Como rodar?

É bem tranquilo, só precisa ter Python 3.6+ instalado:

```bash
python sistema_bancario_2.py
```

Pronto! O menu vai aparecer e você já pode começar a brincar com o sistema.

## O que tem de legal aqui?

### Conceitos de POO que você vai encontrar:

- **Abstração**: Classes abstratas que definem contratos (tipo a `Transacao`)
- **Encapsulamento**: Atributos protegidos com `_` e properties
- **Herança**: Classes que herdam comportamentos de outras
- **Polimorfismo**: Mesma interface, comportamentos diferentes
- **Mixins**: Pequenas classes que dão super poderes pra outras classes

### Padrões de projeto:

- **Strategy Pattern**: Cada tipo de transação sabe se validar
- **Iterator Pattern**: Jeito customizado de percorrer listas
- **Decorator Pattern**: Logs automáticos nas funções importantes

### Funcionalidades Python modernas:

- Decoradores (`@log_transacao`)
- Generators (relatórios eficientes)
- Properties (getters elegantes)
- Type hints implícitos
- Context managers (com os mixins)

## Como usar?

### 1. Criar um cliente

```
Escolha: NU (Novo Usuário)
Digite o nome, CPF, data de nascimento e endereço
```

### 2. Criar uma conta

```
Escolha: NC (Nova Conta)
Digite o CPF do cliente já cadastrado
```

### 3. Fazer um depósito

```
Escolha: D (Depositar)
Digite o CPF, escolha a conta e o valor
```

### 4. Fazer um saque

```
Escolha: S (Sacar)
Mesma coisa: CPF, conta e valor
```

**Atenção**: Tem regras! Você só pode sacar até R$ 500 por vez e fazer no máximo 3 saques por dia. É igual banco de verdade, né?

### 5. Ver o extrato

```
Escolha: E (Extrato)
Vai aparecer todas as movimentações e o saldo atual
```

## Estrutura do código

O código tá organizado assim:

```
Sistema Bancário
├── Decoradores (log automático)
├── Mixins (funcionalidades reutilizáveis)
├── Transações (Deposito e Saque)
├── Histórico (registro de tudo)
├── Cliente (dados pessoais)
├── Conta (operações bancárias)
├── Banco (gerenciamento geral)
├── Iterador (listagem customizada)
└── Interface (menu e interação)
```

## Regras de negócio implementadas

- Depósitos só aceitam valores positivos
- Saques validam saldo disponível
- Limite de R$ 500,00 por saque
- Máximo de 3 saques por dia
- CPF único por cliente
- Um cliente pode ter várias contas
- Histórico completo de todas as transações

## Tecnologias

- Python 3.6+
- Bibliotecas padrão: `functools`, `datetime`, `abc`, `textwrap`
- Zero dependências externas!

## O que você pode aprender aqui?

Se você tá estudando Python, esse projeto é ótimo pra entender:

1. **Como estruturar projetos maiores** sem virar uma bagunça
2. **POO na prática**: não é só teoria de livro, é código real funcionando
3. **Design patterns**: ver como os padrões resolvem problemas de verdade
4. **Clean code**: código legível que outros devs (e você daqui 6 meses) vão entender
5. **Validações e tratamento de erros**: como fazer um sistema robusto

## Nível de dificuldade

**Intermediário a avançado**

Se você já sabe o básico de Python (classes, funções, if/else), vai conseguir entender. Se ainda tá começando, pode ser um pouco desafiador, mas é um ótimo código pra estudar e ir pesquisando cada parte.

## Contribuindo

Achou algum bug? Tem uma ideia pra melhorar? Fica à vontade pra abrir uma issue ou mandar um PR. Toda contribuição é bem-vinda!

Algumas ideias de melhorias:

- [ ] Adicionar persistência de dados (salvar em arquivo/banco de dados)
- [ ] Interface gráfica com Tkinter ou PyQt
- [ ] API REST com Flask/FastAPI
- [ ] Testes unitários com pytest
- [ ] Transferências entre contas
- [ ] Diferentes tipos de conta (corrente, poupança)
- [ ] Autenticação com senha

## Considerações finais

Esse projeto foi feito com carinho pra demonstrar que Python não é só sobre escrever código que funciona, mas sobre escrever código que é **fácil de entender, manter e evoluir**.

