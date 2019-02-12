import altair as alt
import pandas as pd

# Altair plots render by default in JupyterLab and nteract
# Uncomment/run this line to enable Altair in the classic notebook (not in JupyterLab)
a= alt.renderers.enable('notebook')

blogs = pd.read_csv('blogtext.csv') # Importa los datos a un dataframe
blogs = blogs.drop_duplicates(['id'], keep='first') # Se remueven id duplicados para no contar la misma persona dos veces

total_tema = blogs.groupby(['topic']).size()
total_tema = total_tema.sort_values(ascending=True)
total_tema
# Separa en grupos de tamaño similar
i=0
grupo1 = blogs #
grupo2 = blogs #
grupo3 = blogs #

for tema in total_tema.index:
    i += 1
    if i > 28:
        grupo1 = (grupo1[grupo1['topic']!= tema])
    if i < 28 or i >38:
        grupo2 = (grupo2[grupo2['topic']!= tema])
    if i < 39:
        grupo3 = (grupo3[grupo3['topic']!= tema])



# Grafica 1
alt.data_transformers.enable('default', max_rows=None) #Seguro para graficas de altair
alt.Chart(grupo1,title='Relación Tema-Edad 1').mark_rect().encode(
           x=alt.X('age', bin=alt.Bin(maxbins=50), title='Edad'),
           color=alt.Color('count(*):Q', scale=alt.Scale(scheme='greenblue'), title='# Personas'),
           y=alt.Y('topic', title='Tema')
           )

# Grafica 2
alt.Chart(grupo2,title='Relacion Tema-Edad 2').mark_rect().encode(
           x=alt.X('age', bin=alt.Bin(maxbins=50), title='Edad'),
           color=alt.Color('count(*):Q', scale=alt.Scale(scheme='greenblue'), title='# Personas'),
           y=alt.Y('topic', title='Tema')
           )
# Grafica 3
alt.Chart(grupo3,title='Relación Tema-Edad 3').mark_rect().encode(
           x=alt.X('age', bin=alt.Bin(maxbins=50), title='Edad'),
           color=alt.Color('count(*):Q', scale=alt.Scale(scheme='greenblue'), title='# Personas'),
           y=alt.Y('topic', title='Tema')
           )
