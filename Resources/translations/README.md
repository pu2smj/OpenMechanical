# Sobre tradues do OpenMechanical Workbench

## Estrutura

- `OpenMechanical.ts` — arquivo modelo (fonte) para extrao de strings
- `OpenMechanical_en.ts` — traduo para Ingls (padro)
- `OpenMechanical_pt-BR.ts` — traduo para Portugus (Brasil)
- `OpenMechanical_<locale>.qm` — arquivos compilados gerados por `lrelease`

## Fluxo do Tradutor

1. Atualize as strings fonte:
   ```
   python compile_translations.py
   ```
2. Abra o arquivo `.ts` no Qt Linguist e traduza
3. Compile para `.qm`:
   ```
   lrelease OpenMechanical_<locale>.ts
   ```

## Locales Suportados (FreeCAD)

Veja `compile_translations.py` para a lista completa de locales.

## Adicionando um Novo Idioma

1. Crie `OpenMechanical_<locale>.ts` copiando o modelo
2. Traduza as strings
3. Compile para `.qm`
4. Coloque o `.qm` em `Resources/translations/`
