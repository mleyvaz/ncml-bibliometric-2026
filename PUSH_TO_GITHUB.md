# Como subir este repositorio a GitHub

Guia rapida para publicar el repo en tu cuenta de GitHub @mleyvaz.

## Opcion A — Via GitHub CLI (recomendado si ya tienes `gh` instalado)

```bash
cd C:\Users\HP\Documents\NCML_Bibliometric\github_repo

# 1. Iniciar repo local
git init
git add .
git status      # revisar que NO se esten subiendo PDFs ni archivos pesados
git commit -m "Initial release: NCML Bibliometric Retrospective 2018-2026"

# 2. Crear repo remoto publico y hacer push en un solo paso
gh repo create mleyvaz/ncml-bibliometric-2026 --public \
    --description "Bibliometric retrospective of Neutrosophic Computing and Machine Learning journal (2018-2026)" \
    --push --source=.

# 3. Verificar
gh repo view --web
```

## Opcion B — Via git + web UI (manual)

1. Crear repositorio vacio en https://github.com/new
   - Nombre: `ncml-bibliometric-2026`
   - Descripcion: Bibliometric retrospective of NCML 2018-2026
   - Publico
   - NO inicializar con README, LICENSE ni .gitignore (ya los tenemos)

2. Desde la carpeta local:

```bash
cd C:\Users\HP\Documents\NCML_Bibliometric\github_repo
git init
git branch -M main
git add .
git commit -m "Initial release: NCML Bibliometric Retrospective 2018-2026"
git remote add origin https://github.com/mleyvaz/ncml-bibliometric-2026.git
git push -u origin main
```

## Verificaciones post-push

- [ ] El README se renderiza correctamente
- [ ] Los 22 scripts estan visibles en `scripts/`
- [ ] Las 11 figuras PNG se pre-visualizan en `figures/`
- [ ] El archivo Excel de 19 hojas aparece en `data/`
- [ ] Ninguno de los 728 PDFs esta subido (estan en `.gitignore`)
- [ ] El tamano total del repo esta entre 20 y 30 MB

## Siguiente paso: obtener DOI (opcional, recomendable)

Para citar el repositorio con un DOI permanente:

1. Ir a https://zenodo.org/ y autorizar la integracion con GitHub.
2. Activar el repo `mleyvaz/ncml-bibliometric-2026` en las opciones de Zenodo.
3. En GitHub, crear un release (ej. `v1.0.0`). Esto dispara la publicacion
   automatica en Zenodo, que asigna un DOI permanente.
4. Actualizar el `README.md` y `CITATION.cff` con el DOI asignado.

## Notas de seguridad

- El archivo `.gitignore` excluye PDFs, textos completos, backups, venvs, y
  cualquier `.env`. Reviselo antes del primer commit.
- El repositorio NO contiene credenciales ni keys. Los API de OpenAlex y
  DataCite son publicos.
- El `User-Agent` en los scripts identifica al EiC; si prefieres anonimato,
  cambialo antes de publicar.
