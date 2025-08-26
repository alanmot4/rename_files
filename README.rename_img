
 # README — rename_img.py

Descrição

Este README explica a estrutura de pastas e como usar o script `rename_img.py`, que renomeia e copia imagens (JPG/JPEG/TIF/PNG) a partir da pasta `imagens` para a pasta `renomeadas` mantendo a estrutura de subpastas.

Estrutura de pastas esperada (relative to repository root)

- imagens/
  - fotos/
    - <subpastas>/* (arquivos .jpg, .jpeg, .tif, .png)
- renomeadas/  (será criada automaticamente pelo script)

O script lê recursivamente de `imagens` e replica a hierarquia dentro de `renomeadas`.

Comportamento

- Processa somente arquivos com extensões: `.jpg`, `.jpeg`, `.tif`, `.png`.
- Sanitiza nomes: remove acentos, substitui `-` por `_`, substitui caracteres inválidos por `_` e reduz múltiplos underscores.
- Copia o arquivo para a nova pasta (escreve bytes). O comportamento original sobrescreve arquivos com o mesmo nome (sem criar sufixos).
- Gera um relatório CSV em `renomeadas/conversion_report.csv` com colunas: `Original Path`, `New Path`, `Status`.

Como rodar

No Powershell (na pasta do projeto):

```powershell
python .\rename_img.py
```

Recomendações / notas

- Faça backup antes de rodar em produção caso não queira sobrescrever arquivos já existentes.
- Para alterar comportamento (por exemplo, não sobrescrever), o script precisa ser modificado para checar existência e renomear com sufixo ou usar `shutil.copy2`.
- Requisitos: Python 3.6+ (sem dependências externas).


---

Arquivo: `rename_img.py` — purpose: renomear/copiar imagens mantendo estrutura e gerar relatório.


