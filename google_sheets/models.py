import logging
import sys
from collections import namedtuple
from decimal import Decimal, DecimalException

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

headers_data = dict(
    codigo=str,
    preco_tempo_real=Decimal,
    preco_inicio_pregao=Decimal,
    preco_alta_dia_atual=Decimal,
    preco_baixa_dia_atual=Decimal,
    volume_negociacoes_dia_atual=int,
    volume_medio_diario_negociacoes=int,
    numero_acoes_em_circulacao=int,
    alteracao_preco_desde_pregao_anterior=Decimal,
    variacao_percentual_preco_pregao_anterior=Decimal,
    preco_fechamento_dia_anterior=Decimal,
    preco_baixa_52_semanas=Decimal,
    percentual_relacao_baixa_52_semanas=float,
    valor_de_mercado=Decimal,
    data=str,
)

Stock = namedtuple('Stock', [*headers_data.keys()])


def format_value(data):
    method, value = data[0], data[1]
    value = value.replace('R$ ', '').replace('.', '').replace(',', '.').replace(' ', '')

    try:
        return method(value)
    except (DecimalException, ValueError):
        logging.exception(f'Could not convert value {data[1]} to {data[0]}', exc_info=True)
        return data[1]
