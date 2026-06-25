# Diamonds Price Prediction - Render

Proyecto Flask para desplegar el modelo de predicción de precio de diamantes.

## Archivos incluidos

- `app.py`: aplicación Flask.
- `modelo_diamonds.pkl`: pipeline entrenado real del proyecto.
- `requirements.txt`: dependencias fijadas, incluyendo `scikit-learn==1.6.1` para compatibilidad con el modelo.
- `Procfile`: comando de inicio para Render.
- `runtime.txt`: versión de Python recomendada.
- `templates/index.html`: formulario web.
- `static/style.css`: estilos.
- `URL_Render.txt`: archivo para pegar la URL pública final.

## Render

Build Command:

```bash
pip install -r requirements.txt
```

Start Command:

```bash
gunicorn app:app
```

## Variables del formulario

- carat
- cut
- color
- clarity
- depth
- table
- x
- y
- z

El modelo aplica internamente las transformaciones guardadas en el pipeline.
