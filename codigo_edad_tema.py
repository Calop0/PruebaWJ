import altair as alt
import pandas as pd

# Altair plots render by default in JupyterLab and nteract
# Uncomment/run this line to enable Altair in the classic notebook (not in JupyterLab)
a= alt.renderers.enable('notebook')

blogs = pd.read_csv('blogtext.csv') # Importa los datos a un dataframe
blogs = blogs.drop_duplicates(['id'], keep='first') # Se remueven id duplicados para no contar la misma persona dos veces
