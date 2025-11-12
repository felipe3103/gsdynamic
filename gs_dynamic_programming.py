# -*- coding: utf-8 -*-
# ==========================================================
# GLOBAL SOLUTION – FIAP 2025
# Integrantes:
# Felipe do Nascimento Fernandes – RM554598
# Henrique Ignacio Bartalo – RM555274
# Gustavo Henrique Martins – RM556956
# Otimização de Portfólio de Projetos (Mochila 0/1)
# Fases: Greedy, Recursiva, Memo (Top-Down), Bottom-Up (Iterativa)
# Saída detalhada para 4 casos de teste (inclui tabela Bottom-Up no Caso 1)
# ==========================================================

from __future__ import annotations
from typing import List, Dict, Tuple
from functools import lru_cache

Projeto = Dict[str, int]  # {"nome": str, "valor": int, "horas": int}

# ----------------------------------------------------------
# Utilidades de impressão
# ----------------------------------------------------------
def linha(c: str = '-', n: int = 100) -> str:
    return c * n

def titulo(txt: str) -> None:
    print("\n" + linha('='))
    print(txt)
    print(linha('='))

def subtitulo(txt: str) -> None:
    print("\n" + linha('-'))
    print(txt)
    print(linha('-'))

def fmt_ve(v: int, h: int) -> str:
    return f"{(v / h):.2f}" if h else "∞"

def imprimir_tabela_bottom_up(header_proj: List[str], cap: int, T: List[List[int]]) -> None:
    print(linha('='))
    print("TABELA DE PROGRAMAÇÃO DINÂMICA BOTTOM-UP (valores ótimos parciais)")
    print(linha('='))
    caps = "\t".join([f"{c:<5d}" for c in range(0, cap + 1)])
    print(f"Proj\\Cap\t{caps}")
    print(linha('-'))
    zeros = "\t".join([f"{0:<5d}" for _ in range(0, cap + 1)])
    print(f"(nenhum)\t{zeros}")
    for i, nome in enumerate(header_proj, start=1):
        vals = "\t".join([f"{T[i][c]:<5d}" for c in range(0, cap + 1)])
        print(f"{nome:<8s}\t{vals}")
    print(linha('='))

# ----------------------------------------------------------
# FASE 1 – Estratégia Gulosa (Greedy) | O(n log n)
# ----------------------------------------------------------
def mochila_gulosa(projetos: List[Projeto], cap: int) -> Tuple[int, List[str], int]:
    """
    Seleciona por maior razão valor/horas (V/H). Não garante ótimo global.
    Retorna (valor_total, lista_nomes, horas_usadas).
    Desempate determinístico: maior valor, menor horas, nome lexicográfico.
    """
    ordem = sorted(
        projetos,
        key=lambda p: (p["valor"] / p["horas"], p["valor"], -p["horas"], p["nome"]),
        reverse=True,
    )
    v, h, esc = 0, 0, []
    for p in ordem:
        if h + p["horas"] <= cap:
            esc.append(p["nome"])
            v += p["valor"]
            h += p["horas"]
    return v, esc, h

# ----------------------------------------------------------
# FASE 2 – Recursiva Pura | O(2^n)
# ----------------------------------------------------------
def mochila_recursiva(projetos: List[Projeto], cap: int, n: int) -> int:
    """
    Retorna apenas o valor máximo (explora todas as combinações).
    Recorrência:
      max(i,c) = max( max(i-1,c), valor[i-1] + max(i-1, c - horas[i-1]) )
    Casos base: i==0 ou c==0 ⇒ 0.
    """
    if n == 0 or cap == 0:
        return 0
    if projetos[n - 1]["horas"] > cap:
        return mochila_recursiva(projetos, cap, n - 1)
    incluir = projetos[n - 1]["valor"] + mochila_recursiva(projetos, cap - projetos[n - 1]["horas"], n - 1)
    excluir = mochila_recursiva(projetos, cap, n - 1)
    return max(incluir, excluir)

def reconstruir_recursiva(projetos: List[Projeto], cap: int) -> Tuple[int, List[str], int]:
    """
    Reconstrói o conjunto ótimo para a versão recursiva pura
    comparando as decisões (pode reavaliar subproblemas).
    """
    n = len(projetos)
    valor_otimo = mochila_recursiva(projetos, cap, n)
    esc: List[str] = []
    c, i = cap, n
    horas_total = 0
    while i > 0 and c >= 0:
        sem = mochila_recursiva(projetos, c, i - 1)
        h = projetos[i - 1]["horas"]; v = projetos[i - 1]["valor"]
        com = v + mochila_recursiva(projetos, c - h, i - 1) if h <= c else -1
        if com >= sem and h <= c:
            esc.append(projetos[i - 1]["nome"])
            c -= h
            horas_total += h
        i -= 1
    esc.reverse()
    return valor_otimo, esc, horas_total

# ----------------------------------------------------------
# FASE 3 – Programação Dinâmica Top-Down (Memoização) | O(n*C)
# ----------------------------------------------------------
def mochila_memoizada(projetos: List[Projeto], cap: int) -> Tuple[int, List[str], int]:
    """
    Retorna (valor_ótimo, escolhidos, horas_usadas) com memoização e reconstrução.
    """
    n = len(projetos)

    @lru_cache(maxsize=None)
    def solve(i: int, c: int) -> int:
        if i == 0 or c == 0:
            return 0
        h = projetos[i - 1]["horas"]; v = projetos[i - 1]["valor"]
        if h > c:
            return solve(i - 1, c)
        return max(solve(i - 1, c), v + solve(i - 1, c - h))

    # Reconstrução do conjunto ótimo
    esc, c, i, horas_total = [], cap, n, 0
    while i > 0 and c >= 0:
        sem = solve(i - 1, c)
        h = projetos[i - 1]["horas"]; v = projetos[i - 1]["valor"]
        com = v + solve(i - 1, c - h) if h <= c else -1
        if com >= sem and h <= c:
            esc.append(projetos[i - 1]["nome"])
            c -= h; horas_total += h
        i -= 1
    esc.reverse()
    return solve(n, cap), esc, horas_total

# ----------------------------------------------------------
# FASE 4 – Programação Dinâmica Bottom-Up (Iterativa) | O(n*C)
# ----------------------------------------------------------
def mochila_iterativa(projetos: List[Projeto], cap: int) -> Tuple[int, List[str], int, List[List[int]]]:
    """
    Constrói T[i][c] = melhor valor com i primeiros projetos e capacidade c.
    Retorna (valor_ótimo, escolhidos, horas_usadas, tabela T).
    """
    n = len(projetos)
    T = [[0] * (cap + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        v = projetos[i - 1]["valor"]; h = projetos[i - 1]["horas"]
        for c in range(0, cap + 1):
            if h <= c:
                T[i][c] = max(T[i - 1][c], v + T[i - 1][c - h])
            else:
                T[i][c] = T[i - 1][c]

    # Reconstrução
    esc, c, i, horas_total = [], cap, n, 0
    while i > 0 and c >= 0:
        if T[i][c] != T[i - 1][c]:
            esc.append(projetos[i - 1]["nome"])
            horas_total += projetos[i - 1]["horas"]
            c -= projetos[i - 1]["horas"]
        i -= 1
    esc.reverse()
    return T[n][cap], esc, horas_total, T

# ----------------------------------------------------------
# Impressão de um caso completo (todas as fases)
# ----------------------------------------------------------
def imprimir_caso(titulo_caso: str, cap: int, projetos: List[Projeto], mostrar_tabela: bool = False) -> Tuple[int, int, int, int]:
    subtitulo(titulo_caso)
    print(f"\nCapacidade: {cap} (horas-especialista)")
    print("Projetos (Nome, Valor, Horas, V/H):")
    for p in projetos:
        print(f"  ({p['nome']}, V={p['valor']}, H={p['horas']}, V/H={fmt_ve(p['valor'], p['horas'])})")

    # Fase 1 – Greedy
    vg, eg, hg = mochila_gulosa(projetos, cap)
    print("\n[FASE 1 – ESTRATÉGIA GULOSA (GREEDY)]")
    print(f"  Valor Total: {vg}")
    print(f"  Projetos Selecionados: {eg}")
    print(f"  Horas Utilizadas: {hg}")

    # Fase 2 – Recursiva (com reconstrução para mostrar coerência)
    vr, er, hr = reconstruir_recursiva(projetos, cap)
    print("\n[FASE 2 – SOLUÇÃO RECURSIVA PURA]")
    print(f"  Valor Total: {vr}")
    print(f"  Projetos Selecionados: {er}")
    print(f"  Horas Utilizadas: {hr}")

    # Fase 3 – Memo (Top-Down)
    vm, em, hm = mochila_memoizada(projetos, cap)
    print("\n[FASE 3 – PROGRAMAÇÃO DINÂMICA TOP-DOWN (MEMOIZAÇÃO)]")
    print(f"  Valor Total: {vm}")
    print(f"  Projetos Selecionados: {em}")
    print(f"  Horas Utilizadas: {hm}")

    # Fase 4 – Bottom-Up (Iterativa)
    vb, eb, hb, T = mochila_iterativa(projetos, cap)
    print("\n[FASE 4 – PROGRAMAÇÃO DINÂMICA BOTTOM-UP (ITERATIVA)]")
    print(f"  Valor Total: {vb}")
    print(f"  Projetos Selecionados: {eb}")
    print(f"  Horas Utilizadas: {hb}")

    if mostrar_tabela:
        imprimir_tabela_bottom_up([p['nome'] for p in projetos], cap, T)

    # Resumo comparativo
    print("\n✓ COMPARATIVO:")
    print(f"  - Greedy:     {vg} {'(ÓTIMA)' if vg == vb else '(NÃO ÓTIMA)'}")
    print(f"  - Recursiva:  {vr} {'(ÓTIMA)' if vr == vb else '(NÃO ÓTIMA)'}")
    print(f"  - Memo (TD):  {vm} {'(ÓTIMA)' if vm == vb else '(NÃO ÓTIMA)'}")
    print(f"  - Bottom-Up:  {vb} (ÓTIMA)")
    return vg, vr, vm, vb

# ----------------------------------------------------------
# Análise de complexidade
# ----------------------------------------------------------
def analise_complexidade() -> None:
    print(linha('='))
    print("RESUMO DE COMPLEXIDADE")
    print(linha('='))
    print("\nFASE 1 – GREEDY:")
    print("  Tempo: O(n log n) (ordenação); Espaço: O(1)")
    print("  Observação: Heurística local; pode falhar para 0/1 knapsack.")
    print("\nFASE 2 – RECURSIVA PURA:")
    print("  Tempo: O(2^n); Espaço: O(n) (profundidade da pilha)")
    print("  Observação: Explora todas as combinações; ineficiente.")
    print("\nFASE 3 – MEMO (TOP-DOWN):")
    print("  Tempo: O(n*C); Espaço: O(n*C) (cache)")
    print("\nFASE 4 – BOTTOM-UP (ITERATIVA):")
    print("  Tempo: O(n*C); Espaço: O(n*C) (tabela)")
    print("\nConclusão: as Fases 3 e 4 garantem ótimo; a 4 é prática e sem overhead de recursão.")

# ----------------------------------------------------------
# Execução dos 4 casos (com asserts de validação)
# ----------------------------------------------------------
if __name__ == "__main__":
    titulo("TESTES DO PROBLEMA DA MOCHILA 0/1 (OTIMIZAÇÃO DE PORTFÓLIO)")

    # CASO 1 – ENUNCIADO (A, B, C, D | C=10) -> Ótimo = 29 com {A,B,C}
    projetos1 = [
        {"nome": "A", "valor": 12, "horas": 4},
        {"nome": "B", "valor": 10, "horas": 3},
        {"nome": "C", "valor": 7,  "horas": 2},
        {"nome": "D", "valor": 4,  "horas": 3},
    ]
    cap1 = 10
    vg1, vr1, vm1, vb1 = imprimir_caso("CASO 1: Exemplo do Enunciado", cap1, projetos1, mostrar_tabela=True)
    # Validação do caso 1
    assert vb1 == 29, "Bottom-Up (caso 1) deveria ser 29"
    assert vm1 == 29, "Memo (caso 1) deveria ser 29"
    assert vr1 == 29, "Recursiva (caso 1) deveria ser 29"
    assert vg1 == 29, "Greedy (caso 1) deveria ser 29 (neste dataset ele acerta)"

    # CASO 2 – GREEDY FALHA (clássico): cap=50; X(60,10), Y(100,20), Z(120,30)
    # Greedy costuma escolher X+Y (=160); Ótimo é Y+Z (=220)
    projetos2 = [
        {"nome": "X", "valor": 60,  "horas": 10},
        {"nome": "Y", "valor": 100, "horas": 20},
        {"nome": "Z", "valor": 120, "horas": 30},
    ]
    cap2 = 50
    vg2, vr2, vm2, vb2 = imprimir_caso("CASO 2: Demonstração de Falha do Greedy", cap2, projetos2, mostrar_tabela=False)
    # Validação do caso 2
    assert vg2 < 220, "Greedy (caso 2) deve ser < 220 (subótimo)"
    assert vb2 == 220 and vm2 == 220 and vr2 == 220, "Ótimo (caso 2) deveria ser 220"

    # CASO 3 – CAPACIDADE PEQUENA no dataset default (C=5) → ótimo esperado B+C=17
    projetos3 = projetos1[:]  # A,B,C,D iguais
    cap3 = 5
    vg3, vr3, vm3, vb3 = imprimir_caso("CASO 3: Capacidade Pequena (default com C=5)", cap3, projetos3, mostrar_tabela=False)
    assert vb3 == vm3 == vr3 == 17, "Ótimo (caso 3) deveria ser 17 (B+C)"
    assert vg3 <= 17, "Greedy não deve superar o ótimo"

    # CASO 4 – CAPACIDADE EXATA no dataset default (C=9) → ótimo esperado A+C+D=23
    projetos4 = projetos1[:]
    cap4 = 9
    vg4, vr4, vm4, vb4 = imprimir_caso("CASO 4: Capacidade Exata (default com C=9)", cap4, projetos4, mostrar_tabela=False)
    assert vb4 == vm4 == vr4 == 23, "Ótimo (caso 4) deveria ser 23 (A+C+D)"
    # Greedy pode ser igual ou menor; não forçamos valor específico

    analise_complexidade()
    print("\n" + linha('='))
    print("TODOS OS TESTES E FASES EXECUTADOS COM SUCESSO ✔")
    print(linha('='))
