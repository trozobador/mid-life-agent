# input/angela/

Coloque aqui os currículos reais da Angela (PDF/DOCX) e, opcionalmente, um
`profile_truth.md` com as regras de verdade (mesmo formato usado em
`input/ricardo/profile_truth.md`, `input/carol/profile_truth.md` e
`input/gabrielly/profile_truth.md`).

Depois de adicionar os arquivos, gere o `resume.json` dela com:

```bash
python src/scripts/ingest_resume.py --person angela
```

Isso cria `data/angela/resume.json`.

Depois, crie os perfis de vaga em `data/angela/job_profiles/*.txt` (veja o
README nessa pasta) e gere os currículos com:

```bash
python main.py --person angela --role <nome_do_perfil>
```
