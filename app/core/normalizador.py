
def normalizar(entrada: str) -> str:
    """Normaliza a entrada conforme RN-03, sem decidir se é válida."""
    normalizada = entrada.strip().upper()

    # Remove apenas um hífen separador na quarta posição.
    # Não remove hífens em outras posições nem hífens adicionais.
    if len(normalizada) == 8 and normalizada[3] == "-":
        normalizada = normalizada[:3] + normalizada[4:]

    return normalizada
