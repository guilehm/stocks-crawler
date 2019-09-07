from collections import namedtuple

headers = [
    'codigo',
    'preco_tempo_real',
    'preco_inicio_pregao',
    'preco_alta_dia_atual',
    'preco_baixa_dia_atual',
    'volume_negociacoes_dia_atual',
    'volume_medio_diario_negociacoes',
    'numero_acoes_em_circulacao',
    'alteracao_preco_desde_pregao_anterior',
    'variacao_percentual_preco_pregao_anterior',
    'preco_fechamento_dia_anterior',
    'preco_baixa_52_semanas',
    'percentual_relacao_baixa_52_semanas',
    'valor_de_mercado'
]

Stock = namedtuple('Stock', [*headers])
