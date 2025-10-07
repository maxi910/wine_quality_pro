## Guía de Contribución

Gracias por tu interés en contribuir.

### Flujo de trabajo
1. Crear rama: `git switch -c feature/descripcion-corta`.
2. Mantener la rama actualizada con `main` frecuentemente (`git fetch origin && git merge origin/main`).
3. Añadir/actualizar tests si cambias lógica.
4. Asegurar que `pytest -q` pasa.
5. Crear Pull Request descriptivo.

### Estilo de código
* Python >= 3.11.
* Nombrado claro en inglés (variables, funciones) aunque README esté en español.
* Evitar funciones muy largas (>50 líneas) — refactorizar.

### Commits
Formato recomendado (no obligatorio):
```
feat: añade función de carga
fix: corrige bug en validación de esquema
docs: actualiza README
refactor: reorganiza pipeline
test: añade pruebas de carga de datos
ci: ajusta workflow
```

### Tests
Coloca los tests en `tests/` usando `pytest`. Un test mínimo ya valida la carga de datos.

### Seguridad / Datos
No subir datos sensibles. Los datos públicos permanecen en `data/raw/`.

### Preguntas
Abrir un issue etiquetado como `question`.
