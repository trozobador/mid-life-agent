# input/carol/

Coloque aqui os currículos reais da Carol (PDF/DOCX) e, opcionalmente, um
`profile_truth.md` com as regras de verdade (mesmo formato usado em
`input/ricardo/profile_truth.md`).

Depois de adicionar os arquivos, gere o `resume.json` dela com:

```bash
python src/scripts/ingest_resume.py --person carol
```

Isso cria `data/carol/resume.json`.
