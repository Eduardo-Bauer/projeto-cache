# 💾 Projeto Cache – Simulador de Memória Cache Configurável

Este projeto implementa um simulador de memória cache associativa por conjunto, permitindo a análise do impacto de diferentes parâmetros no desempenho da cache. A aplicação foi desenvolvida em linguagem C como parte de um trabalho acadêmico, com foco em práticas de arquitetura de computadores e otimização de acesso à memória.

---

## 🧠 Sobre o Projeto

A memória cache é um componente fundamental na hierarquia de memória, reduzindo a latência de acesso aos dados frequentemente utilizados pelo processador. Este simulador foi desenvolvido para explorar, de forma prática e analítica, os efeitos de diferentes configurações da cache em sua eficiência.

O programa permite modificar diversos parâmetros da memória cache e da memória principal, como:

- Tamanho do bloco
- Tamanho total da cache
- Associatividade
- Política de escrita (`write-through` ou `write-back`)
- Política de substituição (`LRU` ou `aleatória`)
- Tempos de acesso da cache e da memória principal

---

## 🛠️ Funcionalidades

- Configuração da cache via linha de comando
- Leitura de arquivos de simulação contendo endereços e operações (`R` para leitura, `W` para escrita)
- Cálculo de métricas:
  - Taxa de acertos por tipo de operação
  - Tempo médio de acesso
  - Total de acessos à memória principal
- Geração de relatório com os resultados
- Estrutura modular e organizada para facilitar manutenção

---

## 🔢 Parâmetros

| Parâmetro               | Exemplo        | Descrição                                                 |
|-------------------------|----------------|-------------------------------------------------------------|
| `POLITICA_ESCRITA`      | `0`            | 0 = write-through, 1 = write-back                         |
| `TAM_BLOCO`             | `128`          | Tamanho do bloco (em bytes, deve ser potência de 2)       |
| `TAM_CACHE`             | `8192`         | Tamanho total da cache (em bytes, deve ser potência de 2) |
| `ASSOCIATIVIDADE`       | `4`            | Número de blocos por conjunto (potência de 2)             |
| `POLITICA_SUBSTITUICAO` | `LRU` / `ALEATORIO` | Política de substituição aplicada                      |
| `ARQUIVO_ENTRADA`       | `oficial.cache`| Arquivo de entrada com operações de leitura/escrita       |

---

## 📂 Formato do Arquivo de Entrada

Cada linha do arquivo deve conter:

- Um endereço de 32 bits no formato hexadecimal
- Uma letra maiúscula indicando a operação:
  - `R` = Leitura (Read)
  - `W` = Escrita (Write)

### Exemplo:

0020a858 R

05fea840 W

001947a0 R

---

## 📈 Resultados da Simulação

A execução da simulação gera as seguintes informações:

- ✅ Parâmetros utilizados
- 📊 Total de leituras e escritas
- 🧮 Total de acessos à memória principal
- 📌 Taxas de acerto:
  - Por leitura
  - Por escrita
  - Global
- ⏱️ Tempo médio de acesso (em nanosegundos)
- 📁 Geração de um arquivo `.txt` com todos os dados da simulação

Todos os valores reais são apresentados com **quatro casas decimais de precisão**.

---

## 🧪 Aplicações e Análises

O simulador foi utilizado para conduzir uma série de experimentos, com o objetivo de avaliar o desempenho da memória cache em diferentes cenários:

1. **Impacto do Tamanho da Cache**
2. **Impacto do Tamanho do Bloco**
3. **Impacto da Associatividade**
4. **Comparação de Políticas de Substituição** (LRU vs Aleatória)
5. **Comparação entre Estratégias de Escrita** (Write-through vs Write-back)
6. **Avaliação Global da Melhor Configuração**

📊 Gráficos e tabelas foram gerados a partir dos resultados para facilitar a análise e comparação.

---

## 📄 Relatório Técnico

Um relatório completo foi desenvolvido com base nos experimentos realizados. O documento inclui:

- Estrutura e funcionamento do simulador
- Tabelas comparativas
- Gráficos por análise
- Discussões com embasamento teórico

📎 **[Acesse o relatório completo aqui](https://github.com/Eduardo-Bauer/projeto-cache/blob/main/relatorio.pdf)**

---

## 👨‍💻 Autores

- **Eduardo Felipe Bauer**
- **Gabriel Reinhardt dos Reis**
