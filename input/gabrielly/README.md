# input/gabrielly/

Coloque aqui os currículos reais da Gabrielly (PDF/DOCX) e, opcionalmente, um
`profile_truth.md` com as regras de verdade (mesmo formato usado em
`input/ricardo/profile_truth.md` e `input/carol/profile_truth.md`). Um
`profile_truth.md` em branco já foi criado nesta pasta — preencha-o com os
dados dela antes de gerar currículos.

Depois de adicionar os arquivos, gere o `resume.json` dela com:

```bash
python src/scripts/ingest_resume.py --person gabrielly
```

Isso cria `data/gabrielly/resume.json`.

Depois, crie os perfis de vaga em `data/gabrielly/job_profiles/*.txt` (veja o
README nessa pasta) e gere os currículos com:

```bash
python main.py --person gabrielly --role <nome_do_perfil>
```
