#  Global Solution - Dynamic Programming (FIAP 2025)

## Tema
**Otimização de Portfólio de Projetos – O Futuro do Trabalho**

**Disciplina:** Dynamic Programming  
**Professor:** Marcelo Amorim  
**Curso:** Engenharia de Software  
**Ano:** 2025  

---

## 👥 Integrantes do Grupo
- Felipe do Nascimento Fernandes – RM554598  
- Henrique Ignacio Bartalo – RM555274  
- Gustavo Henrique Martins – RM556956  

---

## 🧩 Descrição do Projeto

O projeto implementa o problema de **Otimização de Portfólio de Projetos**, uma aplicação prática do **Problema da Mochila 0/1 (0/1 Knapsack Problem)**.

Em empresas de tecnologia e consultoria, a quantidade de **horas de especialistas** é limitada.  
Cada projeto requer uma quantidade de horas e oferece um valor associado (como lucro, impacto ou relevância).  
O objetivo é selecionar os projetos que **maximizam o valor total** sem ultrapassar o **limite de horas disponíveis**.

---

## ⚙️ Estrutura do Projeto

O código foi desenvolvido em **Python**, aplicando **quatro abordagens distintas** para resolver o mesmo problema.  
Cada uma demonstra uma forma diferente de pensamento algorítmico e eficiência computacional.

| Fase | Estratégia | Descrição | Complexidade |
|------|-------------|------------|---------------|
| 1️⃣ | **Gulosa (Greedy)** | Seleciona projetos pela melhor razão Valor/Horas (V/H). Simples, mas pode falhar no ótimo global. | O(n log n) |
| 2️⃣ | **Recursiva Pura** | Explora todas as combinações possíveis de projetos. Garantidamente correta, mas exponencial. | O(2ⁿ) |
| 3️⃣ | **Top-Down (Memoização)** | Utiliza recursão com cache, evitando recomputações de subproblemas. | O(n × C) |
| 4️⃣ | **Bottom-Up (Iterativa)** | Constrói uma tabela dinâmica para obter o ótimo global de forma eficiente. | O(n × C) |

> **n** = número de projetos  
> **C** = capacidade máxima (horas disponíveis)

---

## 📊 Dados Utilizados

| Projeto | Valor (V) | Horas (H) |
|----------|------------|-----------|
| A | 12 | 4 |
| B | 10 | 3 |
| C | 7 | 2 |
| D | 4 | 3 |

**Capacidade máxima:** 10 horas  

---

## 🧮 Resultados Obtidos

| Fase | Valor Máximo | Projetos Selecionados |
|------|----------------|------------------------|
| Greedy | 29 | ['A', 'B', 'C'] |
| Recursiva Pura | 29 | Ótimo |
| Memoização | 29 | Ótimo |
| Iterativa | 29 | Ótimo |

✅ As abordagens de **Programação Dinâmica** (Top-Down e Bottom-Up) encontraram o **resultado ótimo global**.  
⚠️ A abordagem **Gulosa (Greedy)**, apesar de rápida, pode falhar em cenários mais complexos, pois considera apenas ganhos locais.

---

## 🧠 Análise de Complexidade

| Estratégia | Tipo de Abordagem | Tempo | Espaço | Observações |
|-------------|-------------------|--------|---------|--------------|
| Greedy | Heurística | O(n log n) | O(1) | Rápida, porém não garante ótimo global |
| Recursiva Pura | Exaustiva | O(2ⁿ) | O(n) | Altamente custosa, usada apenas para demonstração conceitual |
| Memoização | PD Top-Down | O(n·C) | O(n·C) | Usa cache para subproblemas já resolvidos |
| Iterativa | PD Bottom-Up | O(n·C) | O(n·C) | Solução mais eficiente e previsível |

---

## 🖥️ Requisitos

- Python 3.10+ (recomendado)
- Nenhuma biblioteca externa além da biblioteca padrão

## ▶️ Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/sua-org/seu-repo.git
   cd seu-repo
   ```
2. Execute o arquivo principal:
```bash
   python main.py
   ```
3. O programa irá:

- Rodar os 4 casos de teste,
- Exibir os resultados de cada fase (Greedy, Recursiva, Memo, Bottom-Up),
- Mostrar a tabela de programação dinâmica (Bottom-Up) no Caso 1,
- Exibir a análise de complexidade ao final.

