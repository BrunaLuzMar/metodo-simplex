def ler_entrada(caminho="entrada.txt"):
    """
    Lê o arquivo de entrada e retorna n, m, c, A, b.
    """
    with open(caminho, "r") as f:
        linhas = f.readlines()

    n, m = map(int, linhas[0].split())
    c = list(map(float, linhas[1].split()))
    A, b = [], []

    for linha in linhas[2:2 + n]:
        valores = list(map(float, linha.split()))
        A.append(valores[:-1])
        b.append(valores[-1])

    return n, m, c, A, b
