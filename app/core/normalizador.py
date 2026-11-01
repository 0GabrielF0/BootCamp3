
def normalizar(entrada: str) -> str:
    """Normaliza a entrada conforme RN-03, sem decidir se é válida."""
    # Converte somente letras ASCII: "ß".upper() viraria "SS" e "ſ".upper() viraria "S" (RN-03.3).
    normalizada = "".join(
        caractere.upper() if caractere.isascii() else caractere
        for caractere in entrada.strip()
    )

    # Remove apenas um hífen separador na quarta posição.
    # Não remove hífens em outras posições nem hífens adicionais.
    if len(normalizada) == 8 and normalizada[3] == "-":
        normalizada = normalizada[:3] + normalizada[4:]

    return normalizada
