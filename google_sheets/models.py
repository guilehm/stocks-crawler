import logging
import sys
from collections import namedtuple
from decimal import Decimal, DecimalException

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def format_value(method, value):
    value = value.replace('R$ ', '').replace('.', '').replace(',', '.').replace(' ', '')

    try:
        return method(value)
    except (DecimalException, ValueError):
        logging.exception(f'Could not convert value {value} to {method}', exc_info=True)
        return value


headers_info = dict(
    codigo=str,
    preco_tempo_real=lambda x: format_value(Decimal, x),
    preco_inicio_pregao=lambda x: format_value(Decimal, x),
    preco_alta_dia_atual=lambda x: format_value(Decimal, x),
    preco_baixa_dia_atual=lambda x: format_value(Decimal, x),
    volume_negociacoes_dia_atual=lambda x: format_value(int, x),
    volume_medio_diario_negociacoes=lambda x: format_value(int, x),
    numero_acoes_em_circulacao=lambda x: format_value(int, x),
    alteracao_preco_desde_pregao_anterior=lambda x: format_value(Decimal, x),
    variacao_percentual_preco_pregao_anterior=lambda x: format_value(Decimal, x),
    preco_fechamento_dia_anterior=lambda x: format_value(Decimal, x),
    preco_baixa_52_semanas=lambda x: format_value(Decimal, x),
    percentual_relacao_baixa_52_semanas=lambda x: format_value(float, x),
    valor_de_mercado=lambda x: format_value(Decimal, x),
    data=None,
)

Stock = namedtuple('Stock', headers_info.keys())
