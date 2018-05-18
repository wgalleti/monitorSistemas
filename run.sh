#bin/bash

cd /home/deploy/projects/monitorSistemas/

.venv/bin/python -m logs.integracao
.venv/bin/python -m logs.processo_automatico
