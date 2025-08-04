# gunicorn_config.py

# Número de workers (processos) para o Gunicorn.
# Um bom ponto de partida é (2 x número de cores da CPU) + 1
workers = 5

# O endereço e a porta em que o Gunicorn irá escutar.
# O Render irá injetar a variável de ambiente PORT.
bind = "0.0.0.0:8000"

# O tipo de worker a ser usado. 'sync' é o padrão.
# 'gevent' ou 'eventlet' são boas escolhas para aplicações com muitas operações de I/O.
# Se você usar 'gevent' ou 'eventlet', não se esqueça de adicioná-los ao seu requirements.txt
# worker_class = 'gevent'

# Timeout para os workers. Se um worker ficar silencioso por mais tempo que isso, ele será reiniciado.
timeout = 120

# Nível de log. 'info' é um bom padrão.
loglevel = 'info'

# Local para os logs de acesso e erro.
# Para o Render, é uma boa prática enviar os logs para o stdout/stderr.
accesslog = '-'
errorlog = '-'