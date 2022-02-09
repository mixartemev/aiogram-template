import decimal


def m_form(d: decimal, pres: int = 2) -> str:
    if not d:
        return d
    is_dec = d % 1
    d = round(d, pres if is_dec else None)
    return f'{d:,}'.replace(',', ' ')
