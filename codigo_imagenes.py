import altair as alt
import pandas as pd
import re

# Altair plots render by default in JupyterLab and nteract
# Uncomment/run this line to enable Altair in the classic notebook (not in JupyterLab)
a= alt.renderers.enable('notebook')
blogs = pd.read_csv('blogtext.csv') # Cargar base de datos

blogs.loc[97,'text']
# FUNCIONES
# Entrega una LISTA con las direcciones url que encuentra en el bloque de texto
def Find_url(string): 
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string) 
    return url 

# Entrega una LISTA con las Imagenes que encuentra en el bloque de texto
def Find_img(string):
    img = re.findall('.jpg|.JPG|.png|.PNG|.jpeg|.JPEG|.TIF', string)
    if len(img) == 0:
        img = re.findall('/photos', string)
    return img

# Cuenta el numero de imagenes encontradas
def Conteo(string):
    return len(Find_img(string))

# Convierte las listas de Find_url en un STRING
def Links(string):
    if len(Find_url(string)) == 0:
        return 'No hay links'
    else:
        fullStr = '-'.join(Find_url(string))
        return fullStr
    
# Convierte las listas de Find_img en un STRING
def Imagenes(string):
    if len(Find_img(string)) == 0:
        return 'No hay imagenes'
    else:
        fullStr2 = '-'.join(Find_img(string))
        return fullStr2
 
blogs_con_links = blogs['text'].apply(Links) 
blogs_con_links =(blogs_con_links[blogs_con_links != "No hay links"]) #Eliminar filas sin links
blogs_con_links.head()

Imgs_en_blog = blogs_con_links.apply(Imagenes)
Imgs_en_blog =(Imgs_en_blog[Imgs_en_blog != 'No hay imagenes']) #Eliminar filas sin imagenes
Imgs_en_blog = Imgs_en_blog.apply(Conteo) #Contar Imagenes por entrada
Imgs_en_blog.head()

max_filas = len(Imgs_en_blog) 

# Dataframe con la fecha y el conteo de imagenes de la entrada
conteo_con_fecha = pd.DataFrame(index=range(0,max_filas),columns=['Fecha','Imagenes'], dtype='float') #df vacio
for i in range(0,max_filas):
    conteo_con_fecha.iloc[ i , 1] = Imgs_en_blog.iloc[i]
    pos_fila = Imgs_en_blog.index[i] 
    conteo_con_fecha.iloc[ i , 0] = blogs.iloc[pos_fila, 5]

conteo_con_fecha.head()

# Eliminacion errores puntuales en to_datetime                                    
conteo_con_fecha =(conteo_con_fecha[conteo_con_fecha['Fecha']!='01,Agosto,2004'])
conteo_con_fecha =(conteo_con_fecha[conteo_con_fecha['Fecha']!='03,Juni,2004'])
conteo_con_fecha =(conteo_con_fecha[conteo_con_fecha['Fecha']!='20,giugno,2004'])
conteo_con_fecha =(conteo_con_fecha[conteo_con_fecha['Fecha']!='21,avril,2004'])
conteo_con_fecha =(conteo_con_fecha[conteo_con_fecha['Fecha']!='01,janvier,2004'])
conteo_con_fecha =(conteo_con_fecha[conteo_con_fecha['Fecha']!='15,julio,2004'])

# Se convierte la fecha al formato de pandas
conteo_con_fecha['Fecha'] =  pd.to_datetime(conteo_con_fecha['Fecha'])

# Grafica cambio anual
alt.data_transformers.enable('default', max_rows=None)
alt.Chart(conteo_con_fecha).mark_line().encode(
    x=alt.X('Fecha:T', timeUnit='year',title='Año'),
    y=alt.Y('sum(Imagenes):Q',title='# Imagenes ref')
)

#Grafica cambio mensual
alt.Chart(conteo_con_fecha).mark_line().encode(
    x=alt.X('Fecha:T', timeUnit='month',title='Mes'),
    y=alt.Y('sum(Imagenes):Q', scale=alt.Scale(clamp = True, domain=(0,200)),title='# Imagenes ref'),
    color =alt.Color('Fecha:O', timeUnit='year', scale=alt.Scale(scheme='magma'),title='Año')
)

 #Zoom en la grafica cambio mensual
alt.Chart(conteo_con_fecha).mark_line().encode(
    x=alt.X('Fecha:T', timeUnit='month',title='Mes'),
    y=alt.Y('sum(Imagenes):Q', scale=alt.Scale(clamp = True, domain=(0,20)),title='# Imagenes ref'),
    color =alt.Color('Fecha:O', timeUnit='year', scale=alt.Scale(scheme='magma'),title='Año')
)
