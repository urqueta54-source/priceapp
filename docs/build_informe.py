import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Image,
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUT = "docs/informe.pdf"

# Carpeta donde viven las capturas de pantalla usadas en la sección de Resultados.
# Deben existir junto al repositorio antes de correr este script.
ASSETS_DIR = "docs/assets"
FIG_REPO = os.path.join(ASSETS_DIR, "fig1_repo_structure.png")
FIG_CI = os.path.join(ASSETS_DIR, "fig2_ci_pipeline.png")
FIG_SWAGGER = os.path.join(ASSETS_DIR, "fig3_swagger_endpoints.png")
FIG_PREDICT = os.path.join(ASSETS_DIR, "fig4_predict_example.png")

styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="H1",
        fontSize=17,
        spaceAfter=10,
        spaceBefore=4,
        textColor=colors.HexColor("#111111"),
        fontName="Helvetica-Bold",
    )
)
styles.add(
    ParagraphStyle(
        name="Subtitle",
        fontSize=9.5,
        leading=13,
        spaceAfter=14,
        fontName="Helvetica-Oblique",
        textColor=colors.HexColor("#444444"),
    )
)
styles.add(
    ParagraphStyle(
        name="H2",
        fontSize=12.5,
        spaceAfter=6,
        spaceBefore=14,
        textColor=colors.HexColor("#1a1a1a"),
        fontName="Helvetica-Bold",
    )
)
styles.add(
    ParagraphStyle(
        name="SubHead",
        fontSize=10,
        leading=13,
        spaceBefore=10,
        spaceAfter=4,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#1a1a1a"),
    )
)
styles.add(
    ParagraphStyle(name="Body", fontSize=10, leading=14.5, spaceAfter=6, fontName="Helvetica")
)
styles.add(
    ParagraphStyle(
        name="BodyItalic",
        fontSize=10,
        leading=14.5,
        spaceAfter=8,
        fontName="Helvetica-Oblique",
        textColor=colors.HexColor("#333333"),
    )
)
styles.add(
    ParagraphStyle(
        name="Caption",
        fontSize=8.5,
        leading=11,
        spaceAfter=10,
        fontName="Helvetica-Oblique",
        textColor=colors.HexColor("#555555"),
        alignment=TA_CENTER,
    )
)
styles.add(
    ParagraphStyle(
        name="CodeBlock",
        fontSize=8.7,
        leading=12,
        spaceAfter=8,
        fontName="Courier",
        textColor=colors.HexColor("#1a1a1a"),
        backColor=colors.HexColor("#f2f2f2"),
        borderPadding=6,
    )
)
styles.add(
    ParagraphStyle(name="Small", fontSize=8.5, leading=11, textColor=colors.HexColor("#555555"))
)

TABLE_HEAD_BG = colors.HexColor("#1a1a1a")
TABLE_ROW_ALT = colors.HexColor("#f4f4f4")
TABLE_GRID = colors.HexColor("#dddddd")


def styled_table(data, col_widths, font_size=8.7, header_font="Helvetica-Bold"):
    t = Table(data, colWidths=col_widths)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEAD_BG),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), header_font),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), font_size),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, TABLE_ROW_ALT]),
                ("GRID", (0, 0), (-1, -1), 0.5, TABLE_GRID),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return t


def bullets(items, style="Body"):
    return ListFlowable(
        [ListItem(Paragraph(x, styles[style])) for x in items],
        bulletType="bullet",
        leftIndent=14,
    )


def figure(path, width_cm, aspect_w, aspect_h, caption):
    """Inserta una imagen centrada con su leyenda debajo, manteniendo el aspect ratio original."""
    flow = []
    width = width_cm * cm
    height = width * (aspect_h / aspect_w)
    img = Image(path, width=width, height=height)
    img.hAlign = "CENTER"
    flow.append(img)
    flow.append(Paragraph(caption, styles["Caption"]))
    return flow


story = []

# ---------------------------------------------------------------------------
# Título y ficha del equipo
# ---------------------------------------------------------------------------
story.append(
    Paragraph("Servicio MLOps end-to-end: predicción de precios de vivienda", styles["H1"])
)
story.append(
    Paragraph(
        "MLOPS· MDS25· Segundo semestre 2026 | Integrantes: Samuel Ruiz, Rodrigo Velis, "
        "Sergio Aviles, Rodrigo Santander",
        styles["Subtitle"],
    )
)

# ---------------------------------------------------------------------------
# 1. Problema
# ---------------------------------------------------------------------------
story.append(Paragraph("1. Problema", styles["H2"]))
story.append(
    Paragraph(
        "Se aborda un problema de regresión: predecir el precio de venta (SalePrice, en USD) de una "
        "vivienda a partir de un subconjunto reducido de variables numéricas del inmueble. El objetivo "
        "del trabajo no es maximizar la sofisticación del modelo, sino construir un sistema completo y "
        "operable: entrenamiento reproducible, contrato de API validado, contenedor portable y un "
        "pipeline de integración y despliegue continuo.",
        styles["Body"],
    )
)

# ---------------------------------------------------------------------------
# 2. Datos
# ---------------------------------------------------------------------------
story.append(Paragraph("2. Datos", styles["H2"]))
story.append(
    Paragraph(
        'Se utilizó el dataset público <b>Ames Housing</b> (competencia Kaggle "House Prices: Advanced '
        'Regression Techniques"), con 1.460 registros y 81 columnas originales. De estas, se descartaron '
        "deliberadamente las 70 columnas categóricas para mantener el pipeline simple y 100% numérico, "
        "y se seleccionaron las 6 columnas numéricas sin valores nulos con mayor correlación lineal de "
        "Pearson respecto al precio de venta:",
        styles["Body"],
    )
)

data = [
    ["Variable", "Descripción", "Corr. con precio"],
    ["overall_qual", "Calidad general de materiales y acabados (1-10)", "0.79"],
    ["gr_liv_area", "Superficie habitable sobre el suelo (sqft)", "0.71"],
    ["garage_cars", "Capacidad del garaje (autos)", "0.64"],
    ["total_bsmt_sf", "Superficie total del sótano (sqft)", "0.61"],
    ["full_bath", "Baños completos sobre el suelo", "0.56"],
    ["year_built", "Año de construcción original", "0.52"],
]
story.append(styled_table(data, [3.3 * cm, 9.2 * cm, 3.2 * cm]))
story.append(Spacer(1, 8))
story.append(
    Paragraph(
        "El dataset crudo se versiona en <font face='Courier'>data/housing_train_raw.csv</font> dentro "
        "del repositorio.",
        styles["Body"],
    )
)

# ---------------------------------------------------------------------------
# 3. Modelo y entrenamiento
# ---------------------------------------------------------------------------
story.append(Paragraph("3. Modelo y entrenamiento", styles["H2"]))
story.append(
    Paragraph(
        "Se entrenó un pipeline de scikit-learn aplicando un modelo de "
        "<font face='Courier'>RandomForestRegressor</font> (200 árboles, profundidad máxima 12). "
        "Se usó una semilla fija (random state=42) y una separación explícita 80/20 entre entrenamiento y "
        "prueba, evaluando las métricas únicamente sobre el conjunto de prueba (datos no vistos durante "
        "el ajuste).",
        styles["Body"],
    )
)

metric_cell_style = ParagraphStyle(name="MetricCell", fontSize=8.7, leading=11, fontName="Helvetica")
metrics_data = [
    ["Métrica", "Valor", "Interpretación"],
    [
        Paragraph("R<super rise=3 size=6>2</super>", metric_cell_style),
        "0.888",
        "El modelo explica ~89% de la varianza del precio",
    ],
    ["RMSE", "$29,374", "Error cuadrático medio sobre el conjunto de prueba"],
    ["MAE", "$19,207", "Error absoluto promedio (~10-11% del precio medio, ~$180k)"],
]
story.append(styled_table(metrics_data, [2.3 * cm, 2.3 * cm, 11.1 * cm]))
story.append(Spacer(1, 8))
story.append(
    Paragraph(
        "Los artefactos (<font face='Courier'>model.pkl</font> y <font face='Courier'>metadata.json</font> "
        "con features, fecha de entrenamiento, semilla y métricas) se generan de forma reproducible mediante "
        "<font face='Courier'>src/train.py</font>, y se regeneran automáticamente en cada build de la imagen "
        "Docker.",
        styles["Body"],
    )
)

# ---------------------------------------------------------------------------
# 4. Resultados
# ---------------------------------------------------------------------------
story.append(Paragraph("4. Resultados", styles["H2"]))

story.append(
    Paragraph(
        "La Figura 1 muestra la estructura del repositorio del proyecto en GitHub (rama main), que "
        "organiza el sistema completo siguiendo las buenas prácticas de un proyecto MLOps productivo:",
        styles["Body"],
    )
)
story.extend(
    figure(FIG_REPO, 11, 836, 656, "Figura 1. Estructura del repositorio del proyecto en GitHub.")
)
story.append(
    Paragraph(
        "El repositorio separa claramente el código, los datos y la infraestructura del servicio: "
        "<font face='Courier'>src/</font> contiene el código de entrenamiento (train.py) y la lógica del "
        "modelo; <font face='Courier'>app/</font> contiene la API FastAPI que sirve las predicciones; "
        "<font face='Courier'>tests/</font> agrupa las pruebas unitarias y de integración usadas en el job "
        "test del pipeline de CI; <font face='Courier'>data/</font> y <font face='Courier'>docs/</font> "
        "almacenan el dataset crudo y la documentación del proyecto; <font face='Courier'>artifacts/</font> "
        "guarda los artefactos generados por el entrenamiento (model.pkl y metadata.json); y "
        "<font face='Courier'>.github/workflows/</font> contiene la definición del pipeline de CI/CD "
        "(ci.yml) analizado en la Figura 2. A nivel de raíz, el Dockerfile y docker-compose.yml definen la "
        "contenerización del servicio, mientras que pyproject.toml, requirements.txt y requirements-dev.txt "
        "fijan las dependencias del proyecto para asegurar reproducibilidad entre entornos de desarrollo, "
        "CI y producción. El repositorio registra 18 commits, con la última actualización correspondiente "
        "al README.md.",
        styles["Body"],
    )
)

story.append(
    Paragraph(
        "La Figura 2 muestra la ejecución del pipeline de integración continua (ci.yml) en GitHub Actions, "
        "activado automáticamente ante un push al repositorio. El workflow encadena cinco jobs "
        "secuenciales, cada uno condicionado al éxito del anterior:",
        styles["Body"],
    )
)
story.extend(
    figure(FIG_CI, 15.875, 1397, 158, "Figura 2. Ejecución del pipeline de CI/CD ante un push al repositorio.")
)
story.append(
    bullets(
        [
            "lint (23s): validación de estilo y calidad del código antes de continuar con el resto del "
            "pipeline.",
            "test (30s): ejecución de las pruebas unitarias del proyecto.",
            "build (57s): construcción de la imagen Docker del servicio, incluyendo el reentrenamiento "
            "del modelo (src/train.py) dentro del build.",
            "smoke-test (21s): verificación básica de que la imagen construida arranca y responde "
            "correctamente (ej. endpoint /health).",
            "publish: etapa de publicación/despliegue; en la ejecución registrada aparece sin completar "
            "(ícono en gris), pero el modelo fue desplegado en Render para consumo público.",
        ]
    )
)
story.append(Spacer(1, 6))
story.append(
    Paragraph(
        "Las primeras cuatro etapas se completaron exitosamente (ícono verde), con un tiempo total de "
        "ejecución de aproximadamente 131 segundos hasta el smoke-test inclusive. Esto confirma que el "
        "pipeline logra automatizar de extremo a extremo la validación de código, pruebas, construcción de "
        "la imagen y verificación de funcionamiento del servicio antes de cualquier publicación, "
        "cumpliendo el objetivo de integración continua.",
        styles["Body"],
    )
)
story.append(
    Paragraph(
        "Una vez construido y validado el servicio, se verificó su contrato de API mediante la "
        "documentación interactiva expuesta en /openapi.json que se muestra en la Figura 3.",
        styles["Body"],
    )
)
story.extend(
    figure(
        FIG_SWAGGER,
        12.17,
        1050,
        319,
        "Figura 3. Documentación interactiva (Swagger UI) de House Pricing API v1.0.0.",
    )
)
story.append(
    Paragraph(
        "La API expone cuatro endpoints bajo el grupo default: un GET /health para verificar el estado "
        "del servicio, un POST /predict para obtener el precio estimado de una única vivienda, un POST "
        "/predict/batch para procesar múltiples viviendas en una sola solicitud, y un GET /model/schema "
        "que expone el contrato de entrada esperado por el modelo (features requeridas y sus tipos). La "
        "disponibilidad de esta documentación generada automáticamente (estándar OpenAPI 3.1) confirma "
        "que el contrato de la API está formalmente especificado y es consultable, lo que facilita su "
        "integración con otros sistemas y su validación durante el smoke-test del pipeline de CI.",
        styles["Body"],
    )
)
story.append(
    Paragraph(
        "La Figura 4 muestra un ejemplo de invocación del endpoint POST /predict, con un cuerpo de "
        "solicitud (request body) que contiene las seis variables numéricas definidas en la Sección 2 "
        "como features del modelo:",
        styles["Body"],
    )
)
story.extend(
    figure(FIG_PREDICT, 10.59, 1050, 467, "Figura 4. Ejemplo de request body para el endpoint POST /predict.")
)
story.append(
    Paragraph(
        "En este caso se consulta el precio estimado de una vivienda con calidad general 7 (sobre 10), "
        "1.710 sqft de superficie habitable, garaje para 2 autos, 856 sqft de sótano, 2 baños completos y "
        "construida en 2003. El hecho de que se valide y acepte este cuerpo confirma que los esquemas "
        "Pydantic definidos en la API coinciden con las features usadas en el entrenamiento (Sección 2), "
        "cerrando el ciclo entre el contrato de datos y el modelo servido.",
        styles["Body"],
    )
)

# ---------------------------------------------------------------------------
# 5. Limitaciones conocidas y trabajo futuro
# ---------------------------------------------------------------------------
story.append(Paragraph("5. Limitaciones conocidas y trabajo futuro", styles["H2"]))
story.append(
    bullets(
        [
            "Se descartaron 70 columnas categóricas (ej. Neighborhood, ExterQual) que aportarían señal "
            "significativa en un modelo de producción real; con más tiempo se agregaría un encoder "
            "dentro del mismo Pipeline de sklearn.",
            "No hay monitoreo de data drift ni reentrenamiento automático.",
            "No hay autenticación en la API (pensado para uso académico/demo).",
            "El modelo no reporta intervalos de confianza por predicción.",
            "No hay versionado formal de datasets (ej. DVC).",
            "El plan gratuito de Render duerme el servicio tras inactividad; el primer request "
            "post-inactividad puede tardar 30-50s.",
        ]
    )
)

# ---------------------------------------------------------------------------
# 6. Model Card
# ---------------------------------------------------------------------------
story.append(Paragraph("6. Model Card", styles["H2"]))
story.append(
    Paragraph(
        "Resumen del modelo en producción — House Pricing API v1.0.0, servido en "
        "mlops-pricing-app.onrender.com (/docs). Entrenado el 2026-08-16 (autor: Sergio Avilés Rosales, "
        "integrante del equipo).",
        styles["BodyItalic"],
    )
)

story.append(Paragraph("Uso previsto", styles["SubHead"]))
story.append(
    Paragraph(
        "Estimación automatizada y referencial del precio de venta de una vivienda residencial a partir "
        "de sus características físicas principales, orientada a aplicaciones de apoyo en decisiones de "
        "compra/venta o valoración inmobiliaria, y como demostración académica de un pipeline MLOps "
        "completo. Los usuarios previstos son desarrolladores e investigadores que consumen la API REST "
        "expuesta por la aplicación FastAPI del proyecto.",
        styles["Body"],
    )
)
story.append(Paragraph("Usos fuera de alcance:", styles["Body"]))
story.append(
    bullets(
        [
            "Tasación oficial o legal de inmuebles.",
            "Valoración de propiedades comerciales o industriales.",
            "Decisiones financieras o crediticias vinculantes sin revisión de un profesional del sector.",
            "Mercados inmobiliarios distintos al de Ames, Iowa (EE. UU.), sobre el cual fue entrenado el "
            "dataset.",
        ]
    )
)

story.append(Paragraph("Datos y features del modelo", styles["SubHead"]))
story.append(
    Paragraph(
        'Dataset Ames Housing (competencia Kaggle "House Prices: Advanced Regression Techniques"), '
        "archivo housing_train_raw.csv, con 1.460 registros y 81 columnas originales. Se seleccionaron "
        "las 6 columnas numéricas sin nulos con mayor correlación con SalePrice; las ~70 restantes "
        "(mayormente categóricas) se descartaron para mantener el pipeline simple y 100% numérico. La "
        "partición entrenamiento/prueba y su detalle se muestran en la sección de métricas de desempeño "
        "más abajo.",
        styles["Body"],
    )
)
features_data = [
    ["Feature", "Columna orig.", "Descripción", "Tipo", "Rango válido", "Corr."],
    ["overall_qual", "OverallQual", "Calidad general de materiales y acabados", "int", "1 - 10", "0.79"],
    ["gr_liv_area", "GrLivArea", "Superficie habitable sobre el suelo (sqft)", "float", "> 0, <= 15.000", "0.71"],
    ["garage_cars", "GarageCars", "Capacidad del garaje (n° de autos)", "int", "0 - 10", "0.64"],
    ["total_bsmt_sf", "TotalBsmtSF", "Superficie total del sótano (sqft)", "float", ">= 0, <= 15.000", "0.61"],
    ["full_bath", "FullBath", "Baños completos sobre el suelo", "int", "0 - 10", "0.56"],
    ["year_built", "YearBuilt", "Año de construcción original", "int", "1800 - 2026", "0.52"],
    ["price (target)", "SalePrice", "Precio de venta (USD)", "float", "—", "—"],
]
story.append(
    styled_table(
        features_data,
        [2.3 * cm, 2.3 * cm, 5.4 * cm, 1.2 * cm, 3.2 * cm, 1.5 * cm],
        font_size=8.0,
    )
)
story.append(Spacer(1, 8))

story.append(Paragraph("Modelo y parámetros", styles["SubHead"]))
story.append(
    Paragraph(
        "El modelo utilizado es un RandomForestRegressor de scikit-learn (v1.6.0), un algoritmo de "
        "ensamble basado en árboles de decisión, elegido por su capacidad de capturar relaciones no "
        "lineales entre las variables del inmueble y su precio de venta sin requerir un preprocesamiento "
        "extenso de las features (más allá del escalado). Se implementa como un Pipeline de scikit-learn "
        "compuesto por un StandardScaler seguido del RandomForestRegressor, con los siguientes "
        "parámetros:",
        styles["Body"],
    )
)
params_data = [
    ["Parámetro", "Valor"],
    ["Algoritmo", "Random Forest Regressor"],
    ["Número de árboles", "200"],
    ["Profundidad máxima", "12"],
    ["Semilla aleatoria", "42 (random_state)"],
    ["Serialización", "joblib (.pkl)"],
    ["Framework", "scikit-learn (Pipeline)"],
]
story.append(styled_table(params_data, [5.5 * cm, 10.0 * cm]))
story.append(Spacer(1, 8))

story.append(Paragraph("Métricas de desempeño (conjunto de prueba)", styles["SubHead"]))
story.append(
    Paragraph(
        "Evaluadas exclusivamente sobre el conjunto de prueba (292 registros no vistos durante el "
        "ajuste), tras una partición aleatoria 80/20 (1.168 registros de entrenamiento / 292 de prueba) "
        "sobre el total de 1.460 registros, con random_state=42.",
        styles["Body"],
    )
)
mc_metrics_data = [
    ["Métrica", "Valor", "Interpretación"],
    ["RMSE", "$29,374.31", "Error cuadrático medio (USD)"],
    ["MAE", "$19,207.23", "Error absoluto promedio (~10-11% del precio medio)"],
    [
        Paragraph("R<super rise=3 size=6>2</super>", metric_cell_style),
        "0.8875",
        "~89% de la varianza explicada",
    ],
]
story.append(styled_table(mc_metrics_data, [2.3 * cm, 2.6 * cm, 10.6 * cm]))
story.append(Spacer(1, 6))
story.append(
    Paragraph(
        "El modelo explica ~89% de la varianza (R<super rise=2 size=6>2</super>) y se equivoca en promedio ~$19.2k (MAE) sobre un "
        "precio medio de ~$180k (~10-11% de error relativo) — razonable usando solo 6 variables y sin "
        "ubicación (Neighborhood), uno de los predictores más fuertes en el dataset completo.",
        styles["BodyItalic"],
    )
)

story.append(Paragraph("Interfaz de servicio (API)", styles["SubHead"]))
api_data = [
    ["Método", "Ruta", "Descripción"],
    ["GET", "/health", "Estado del servicio y si el modelo está cargado"],
    ["POST", "/predict", "Predicción para una sola vivienda"],
    ["POST", "/predict/batch", "Predicción para hasta 1000 viviendas (campo items)"],
    ["GET", "/model/schema", "Features esperadas y sus tipos"],
    ["GET", "/docs", "Documentación interactiva (Swagger UI)"],
]
story.append(styled_table(api_data, [2.0 * cm, 3.5 * cm, 10.0 * cm]))
story.append(Spacer(1, 6))
story.append(
    Paragraph(
        "Ejemplo: entrada overall_qual=7, gr_liv_area=1710, total_bsmt_sf=856, garage_cars=2, "
        "full_bath=2, year_built=2003 -&gt; predicted_price = $190,718.24 (precio real: $208,500). "
        "Entradas inválidas devuelven siempre error controlado 422, nunca 500 genérico.",
        styles["Body"],
    )
)

story.append(Paragraph("Limitaciones y consideraciones del modelo", styles["SubHead"]))
story.append(
    Paragraph(
        "A diferencia de las limitaciones de infraestructura y pipeline descritas en la Sección 5, estas "
        "limitaciones son propias del alcance y comportamiento del modelo predictivo en sí:",
        styles["Body"],
    )
)
story.append(
    bullets(
        [
            "Cobertura geográfica: entrenado con datos de Ames, Iowa (EE. UU.); la precisión puede "
            "degradarse en otros mercados.",
            "Cobertura temporal: no captura tendencias de mercado recientes ni fluctuaciones "
            "posteriores al dataset.",
            "Variables limitadas: usa solo 6 de las ~80 variables disponibles; atributos como calidad "
            "del barrio o número de habitaciones no están incluidos, y no se consideran variables "
            "categóricas (zonificación, estilo arquitectónico, condición de venta).",
            "Outliers: viviendas con superficies o precios muy por encima del rango de entrenamiento "
            "pueden producir predicciones menos confiables.",
        ]
    )
)
story.append(
    Paragraph(
        "Consideraciones éticas: las predicciones no deben utilizarse como único criterio en decisiones "
        "de compra, venta o financiamiento. El modelo no fue evaluado para detectar posibles sesgos "
        "hacia ciertos tipos de propiedades o compradores, por lo que se recomienda revisar sus "
        "resultados junto a un profesional del sector inmobiliario antes de tomar decisiones "
        "vinculantes.",
        styles["Body"],
    )
)

story.append(Paragraph("Artefactos y reproducibilidad", styles["SubHead"]))
story.append(
    Paragraph(
        "El pipeline entrenado (StandardScaler + RandomForestRegressor) se serializa en "
        "artifacts/model.pkl, junto con artifacts/metadata.json (features, métricas, versión y fecha de "
        "entrenamiento). Para reentrenar el modelo desde cero:",
        styles["Body"],
    )
)
story.append(Paragraph("python src/train.py --data data/housing_train_raw.csv --out artifacts", styles["CodeBlock"]))
story.append(
    Paragraph(
        "Todos los resultados son deterministas gracias al uso de random_state=42 en las operaciones "
        "con aleatoriedad (split de datos y muestreo bootstrap de los árboles).",
        styles["Body"],
    )
)

story.append(Paragraph("Uso de asistentes de IA", styles["SubHead"]))
story.append(
    Paragraph(
        "Se usó Claude (Anthropic) para generar la estructura inicial del proyecto (carpetas, "
        "Dockerfile, docker-compose.yml, workflow de GitHub Actions), redactar los tests de pytest sobre "
        "el contrato ya definido de la API, y depurar errores de despliegue en Render. El diseño del "
        "esquema de features, la selección de columnas del dataset y las decisiones de arquitectura del "
        "modelo fueron revisadas y validadas por el equipo.",
        styles["Body"],
    )
)

# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
doc = SimpleDocTemplate(
    OUT,
    pagesize=letter,
    topMargin=1.8 * cm,
    bottomMargin=1.8 * cm,
    leftMargin=1.8 * cm,
    rightMargin=1.8 * cm,
)
doc.build(story)
print(f"Generado {OUT}")
