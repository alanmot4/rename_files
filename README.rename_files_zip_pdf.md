# README — rename_files_zip_pdf.py

Descrição

Este README explica a estrutura de pastas e como usar o script `rename_files_zip_pdf.py`. O script renomeia e copia arquivos PDF e arquivos compactados (zip/rar/7z/tar/gz/...) de duas raízes de entrada para duas pastas de saída, preservando a hierarquia de pastas e gerando relatórios CSV.

Estrutura de pastas esperada (relative to repository root)

- imagens/                 -> (opcional, mapeado para `renomeadas`)
  - <subpastas>/*           (se houver PDFs/arquivos compactados dentro de `imagens` será processado)
- Pandora/                 -> mapeado para `saida/pandora`
  - laminas/               (ex.: .pdf)
  - site/                  (ex.: .zip, .pdf)
- renomeadas/              (será criada automaticamente se não existir)
- saida/pandora/           (será criada automaticamente se não existir)

Comportamento

- Processa somente arquivos com extensões: `.pdf`, `.zip`, `.rar`, `.7z`, `.tar`, `.gz`, `.tgz`, `.tar.gz`.
- Mantém a estrutura relativa: por exemplo `Pandora/laminas/arquivo.pdf` -> `saida/pandora/laminas/arquivo.pdf`.
- Não extrai o conteúdo de arquivos compactados — apenas copia/renomeia os arquivos compactados.
- Sanitiza nomes: remove acentos, substitui espaços e `-` por `_`, remove caracteres não permitidos, reduz múltiplos underscores.
- Evita sobrescrever: se o arquivo destino já existir, adiciona sufixo `_1`, `_2`, ... ao nome.
- Preserva metadados de arquivo ao copiar (`shutil.copy2`).
- Gera um relatório CSV em `renomeadas/conversion_report.csv` (para a raiz `imagens`) e em `saida/pandora/conversion_report.csv` (para `Pandora`) com colunas: `Original Path`, `New Path`, `Status`.

Como rodar

No Powershell (na pasta do projeto):

```powershell
python .\rename_files_zip_pdf.py
```

Observações / casos especiais

- Se uma raiz de entrada (`imagens` ou `Pandora`) não existir, o script apenas loga e pula essa raiz.
- Se você já rodou o script antes e criou arquivos em `saida/pandora` ou `renomeadas`, novas execuções podem criar arquivos com sufixos `_1` porque o script evita sobrescrever por padrão.
  - Se preferir rodar do zero sem sufixos, remova as pastas de saída antes de rodar (ex.: `Remove-Item -Recurse -Force .\renomeadas` e `Remove-Item -Recurse -Force .\saida\pandora`).

Recomendações

- Faça backup/cópia das pastas de destino antes de rodar pela primeira vez.
- Se quiser que o script sobrescreva arquivos ao invés de criar sufixos, informe e eu atualizo o comportamento.
- Requisitos: Python 3.6+ (não requer dependências externas além da biblioteca padrão).


---

Arquivo: `rename_files_zip_pdf.py` — purpose: renomear/copiar PDFs e arquivos compactados mantendo estrutura e gerar relatórios.
