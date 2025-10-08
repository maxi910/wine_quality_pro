# Flujo de Trabajo del Equipo - Wine Quality Pro

## 🤝 Colaboradores
- **Maxi910** - Propietario del repositorio
- **[Nombre del compañero]** - Colaborador

## 📋 Reglas de Colaboración

### 1. Antes de empezar a trabajar
```bash
git pull origin main  # Siempre actualizar antes de trabajar
```

### 2. Crear una rama para cada funcionalidad nueva
```bash
git checkout -b feature/nombre-descriptivo
# Ejemplo: git checkout -b feature/mejora-algoritmo-xgboost
```

### 3. Commits descriptivos
- Usar mensajes claros: `feat: añade validación cruzada al modelo`
- Hacer commits pequeños y frecuentes
- Prefijos recomendados:
  - `feat:` para nuevas funcionalidades
  - `fix:` para corrección de bugs
  - `docs:` para documentación
  - `test:` para pruebas
  - `refactor:` para refactorización

### 4. Antes de hacer merge
```bash
# Asegurarse que todo funciona
python -m pytest tests/
python src/wine_quality/main.py --help
```

### 5. Pull Requests (Recomendado)
- Crear Pull Request en GitHub para revisión de código
- El otro compañero revisa antes de hacer merge
- Usar el template de PR (ver abajo)

## 🔄 Flujo Rápido (Alternativo)
Si prefieren un flujo más directo:
```bash
git pull origin main    # Actualizar
# ... trabajar ...
git add .
git commit -m "descripción clara"
git push origin main
```

## 📝 Template de Pull Request
```
## Descripción
Breve descripción de los cambios

## Cambios realizados
- [ ] Funcionalidad A
- [ ] Corrección B
- [ ] Documentación C

## Testing
- [ ] Tests pasan
- [ ] Código probado manualmente

## Screenshots (si aplica)
[Capturas de pantalla o gráficos]
```

## 📁 Organización de tareas
Usar GitHub Issues para:
- Reportar bugs
- Proponer nuevas funcionalidades
- Asignar tareas

## 🚨 Reglas importantes
1. **NUNCA** hacer push directo a `main` sin coordinar
2. **SIEMPRE** hacer pull antes de trabajar
3. **COMUNICAR** los cambios importantes en Issues/Discord/Slack
4. **REVISAR** el código del compañero cuando sea posible