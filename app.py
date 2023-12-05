import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import plotly.express as px

# Configurar la página
st.set_page_config(layout='wide', initial_sidebar_state='expanded')

# Configurar el estilo de la página
# Estilos CSS básicos
css_styles = """
    .metric-container {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        margin-bottom: 15px;
    }

    .metric-title {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .metric-value {
        font-size: 24px;
        color: #2e86de;
    }
    .hallazgo-container {
        background-color: #f2f2f2;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    .titulo-hallazgo {
        font-size: 20px;
        font-weight: bold;
        color: #2e86de;
        margin-bottom: 10px;
    }

    .texto-hallazgo {
        font-size: 16px;
        color: #333;
    }

    .titulo-container {
        background-color: #f2f2f2;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    .titulo-accion {
        font-size: 20px;
        font-weight: bold;
        color: #ff6348;
        margin-bottom: 10px;
    }

    .texto-accion {
        font-size: 16px;
        color: #333;
    }
"""
# Aplicar estilos CSS
st.markdown(f'<style>{css_styles}</style>', unsafe_allow_html=True)

# Imagen de la aplicación
st.sidebar.image('images/belcorp.png', width=60)

# Título de la aplicación
st.sidebar.header('Aplicación de Análisis de Datos de Belcorp')

# Leer archivos
emp_df = pd.read_csv('data/Empleados.txt', sep='\t', encoding='UTF-16', dtype={'IDVENDEDOR': str, 'IDTIPOVENDEDOR': str})
clas_emp_df = pd.read_excel('data/Clasificación Vendedor.xlsx', dtype={'IDTIPOVENDEDOR': str})
ventas_df = pd.read_excel('data/Ventas.xlsx', dtype={'CODIGO VENDEDOR': str})
car_df = pd.read_excel('data/Caracteristicas.xlsx')
productos_df = pd.read_excel('data/Producto.xlsx')
precios_df = pd.read_excel('data/Precios.xlsx')
clas_df = pd.read_excel('data/Clasificación.xlsx', dtype={'IDCATEGORIA': str, 'IDSUBCATEGORIA': str, 'IDTIPO': str})
cat_df = pd.read_excel('data/Categoría.xlsx', dtype={'IDCATEGORIA': str})
subcat_df = pd.read_excel('data/Subcategoría.xlsx', dtype={'IDSUBCATEGORIA': str})
tipo_df = pd.read_excel('data/Tipo.xlsx', dtype={'IDTIPO': str})

# Crear un diccionario con los hallazgos
hallazgos = {
    "Primer Hallazgo": "Aquí irá la descripción del hallazgo 1.",
    "Segundo Hallazgo": "Descripción del hallazgo 2.",
    "Tercer Hallazgo": "Descripción del hallazgo 3.",
    "Cuarto Hallazgo": "Descripción del hallazgo 4."
}

# Funciones para cada hallazgo
def primer_hallazgo():
    df1 = pd.merge(ventas_df, emp_df, left_on='CODIGO VENDEDOR', right_on='IDVENDEDOR')
    df1 = pd.merge(df1, productos_df, on='IDCUC')
    df1 = df1[['NOMBRE', 'APELLIDO', 'Name', 'VENTAS']]
    df1['NOMBRE'] = df1['NOMBRE'] + ' ' + df1['APELLIDO']
    df1 = df1.drop(columns=['APELLIDO'])
    df1 = df1.rename(columns={'NOMBRE': 'VENDEDOR', 'Name': 'PRODUCTO'})
    df1 = df1.groupby(['VENDEDOR']).agg({'PRODUCTO': 'nunique', 'VENTAS': 'sum'}).reset_index()
    df1.columns = ['VENDEDOR', 'PRODUCTOS VENDIDOS', 'VENTAS']

    mean_products = df1['PRODUCTOS VENDIDOS'].mean()
    mean_venta = df1['VENTAS'].mean()


    st.subheader("Desconexión entre Variedad de Productos y Ventas en el Top 10 de Vendedores")

    col1, col2 = st.columns(2)

    with col1.container():
        st.markdown('<div class="metric-container"><div class="metric-title">Promedio de Productos Vendidos</div><div class="metric-value">{:.0f}</div></div>'.format(mean_products), unsafe_allow_html=True)

    with col2.container():
        st.markdown('<div class="metric-container"><div class="metric-title">Promedio de Ventas</div><div class="metric-value">{:.0f}</div></div>'.format(mean_venta), unsafe_allow_html=True)


    col1, col2 = st.columns(2)

    color_palette1 = sns.color_palette("Purples", n_colors=10)[::-1]
    color_palette2 = sns.color_palette("Blues", n_colors=10)[::-1]

    with col1:
        fig1, ax1 = plt.subplots(figsize=(12, 8))
        sns.barplot(x="VENDEDOR", y="PRODUCTOS VENDIDOS", data=df1.sort_values('PRODUCTOS VENDIDOS', ascending=False).head(10), ax=ax1, palette=color_palette1)
        for p in ax1.patches:
            ax1.annotate(f'{p.get_height():.0f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=10, color='black')
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=40, ha="right")
        ax1.set_title('Top 10 Vendedores por Productos Vendidos')
        ax1.set_xlabel('Vendedor')
        ax1.set_ylabel('Productos Vendidos')
        st.pyplot(fig1)
    with col2:
        fig2, ax2 = plt.subplots(figsize=(12, 8))
        sns.barplot(x="VENDEDOR", y="VENTAS", data=df1.sort_values('VENTAS', ascending=False).head(10), ax=ax2, palette=color_palette2)
        for p in ax2.patches:
            height = p.get_height()
            ax2.annotate(f'{height:.0f}\n{df1[df1["VENTAS"] == height]["PRODUCTOS VENDIDOS"].values[0]} productos',
                        (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=10, color='black')
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=40, ha="right")
        ax2.set_title('Top 10 Vendedores por Ventas')
        ax2.set_xlabel('Vendedor')
        ax2.set_ylabel('Ventas')
        st.pyplot(fig2)

    col1, col2 = st.columns((6, 4))
    with col1:
        st.markdown('<div class="titulo-container"><div class="titulo-hallazgo">Hallazgo:</div>Se ha descubierto un patrón interesante en el top 10 de vendedores con la mayor variedad de productos. A pesar de tener una amplia gama de productos en sus catálogos, no necesariamente son los líderes en términos de ventas. Incluso al observar el top 10 de vendedores con más ventas, notamos la presencia de uno que solo ofrece 38 productos y varios con alrededor de 150 productos.</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="titulo-container"><div class="titulo-accion">Posible Acción:</div>Se recomienda evaluar la rentabilidad de cada producto individual en el catálogo para identificar aquellos que generan mayores márgenes de ganancia. Para que así los vendedores no tengan que comprar mucha variedad de productos para vender.</div>', unsafe_allow_html=True)

def segundo_hallazgo():
    df2 = pd.merge(emp_df, ventas_df, left_on='IDVENDEDOR', right_on='CODIGO VENDEDOR')
    df2 = pd.merge(df2, clas_df, on='IDCUC')
    df2 = pd.merge(df2, cat_df, on='IDCATEGORIA')
    df2 = df2[['GENERO', 'VENTAS', 'Categoría']]
    df2 = df2.rename(columns={'Categoría': 'CATEGORIA'})
    df2['VENTAS TOTALES'] = df2.groupby(['GENERO', 'CATEGORIA'])['VENTAS'].transform('sum')
    df2 = df2.drop(columns=['VENTAS'])
    df2 = df2.drop_duplicates()

    mean_man = df2[df2['GENERO'] == 'Hombre']['VENTAS TOTALES'].mean()
    mean_woman = df2[df2['GENERO'] == 'Mujer']['VENTAS TOTALES'].mean()

    custom_palette = ['#5e3c99', '#8250c7', '#a262d4', '#c173e1', '#e186f0']

    st.subheader("Disparidad Significativa en Ventas por Género y Categoría")

    col1_t, col2_t = st.columns((3, 7))

    with col1_t:
        st.markdown("&nbsp;")
        st.markdown('<div class="metric-container"><div class="metric-title">Promedio de Ventas Totales de Hombres</div><div class="metric-value">{:.0f}</div></div>'.format(mean_man), unsafe_allow_html=True)
        st.markdown('<div class="metric-container"><div class="metric-title">Promedio de Ventas Totales de Mujeres</div><div class="metric-value">{:.0f}</div></div>'.format(mean_woman), unsafe_allow_html=True)

    with col2_t:
        fig = px.bar(df2, x="GENERO", y="VENTAS TOTALES", color="CATEGORIA", barmode="group", 
                     title='Ventas Totales por Género y Categoría', 
                     labels={'VENTAS TOTALES': 'Ventas Totales', 'GENERO': 'Género'},
                     color_discrete_sequence=custom_palette)
        st.plotly_chart(fig)
    
    col1, col2 = st.columns((6, 4))
    with col1:
        st.markdown('<div class="hallazgo-container"><div class="titulo-hallazgo">Hallazgo:</div>Se ha identificado una marcada disparidad en las ventas totales entre hombres y mujeres en diversas categorías de productos. En el ámbito del Cuidado Personal, por ejemplo, las mujeres registran aproximadamente nueve veces más ventas en comparación con los hombres. Es importante señalar que, aunque la categoría de Cuidado Personal lidera las ventas en general, para los hombres es una de las categorías con menor rendimiento a pesar de su contribución al total de ventas.</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="hallazgo-container"><div class="titulo-accion">Posible Acción:</div>Se recomienda implementar estrategias específicas para incentivar a los vendedores masculinos a explorar y promover productos de la categoría Cuidado Personal. Esto podría incluir capacitación adicional, material de marketing específico y destacar los beneficios de estos productos en particular.</div>', unsafe_allow_html=True)

def tercer_hallazgo():
    df3 = pd.merge(ventas_df, clas_df, on='IDCUC')
    df3 = pd.merge(df3, cat_df, on='IDCATEGORIA')
    df3 = pd.merge(df3, subcat_df, on='IDSUBCATEGORIA')
    df3 = df3[df3['Categoría'] == 'FRAGANCIAS']
    df3 = df3[['AÑO', 'VENTAS', 'SubCategoría']]
    df3 = df3.rename(columns={'SubCategoría': 'SUBCATEGORIA'})
    df3 = df3.groupby(['SUBCATEGORIA', 'AÑO']).agg({'VENTAS': 'sum'}).reset_index()
    df3 = df3.sort_values(by=['SUBCATEGORIA', 'AÑO'])

    df3_aux = df3.copy()
    df3_aux['VENTAS DIFERENCIA'] = df3_aux.groupby(['SUBCATEGORIA'])['VENTAS'].diff()
    df3_aux = df3_aux.dropna()
    df3_aux = df3_aux[['SUBCATEGORIA', 'VENTAS DIFERENCIA']]
    df3_aux = df3_aux.sort_values(by=['VENTAS DIFERENCIA'], ascending=False)
    df3_aux = df3_aux.reset_index(drop=True)

    st.subheader("Aumento Significativo en las Ventas de Fragancias en Subcategorías Específicas")

    col1, col2 = st.columns((3, 7))

    with col1:
        st.markdown("&nbsp;")
        st.table(df3_aux)

    with col2:
        fig = px.line(df3, x='AÑO', y='VENTAS', color='SUBCATEGORIA', markers=True, title='Crecimiento de Ventas por Subcategoría a lo Largo del Tiempo')
        fig.update_layout(xaxis_title='Año', yaxis_title='Ventas')
        st.plotly_chart(fig)

    col1, col2 = st.columns((5.3, 4.7))

    with col1:
        st.markdown('<div class="hallazgo-container"><div class="titulo-hallazgo">Hallazgo:</div>Se han identificado tres tendencias clave en las ventas de fragancias durante el período de 2015 a 2016. En primer lugar, se observa un notable aumento en las ventas de productos dirigidos a damas, con un incremento cercano a las 700,000 unidades. En contraste, se evidencia una disminución de casi 200,000 unidades en las ventas de productos para caballeros. Por último, se destaca un aumento de casi 300,000 unidades en las ventas de productos para el cuidado del baño familiar, indicando un significativo crecimiento en esta categoría específica.</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="hallazgo-container"><div class="titulo-accion">Posible Acción:</div>Se sugiere mantener la actual estrategia de marketing para los productos destinados a damas. Además, se recomienda fomentar el desarrollo y la promoción de productos de baño familiar para potenciar aún más las ventas en esta categoría. Por último, se aconseja llevar a cabo campañas publicitarias o de marketing específicamente orientadas a los productos dirigidos a caballeros, con el objetivo de incrementar sus ventas y no estar en negativo en comparación a años anteriores.</div>', unsafe_allow_html=True)        

def cuarto_hallazgo():
    df4 = pd.merge(ventas_df, emp_df, left_on='CODIGO VENDEDOR', right_on='IDVENDEDOR')
    df4 = df4[['NSE VIVIENDA', 'VENTAS']]

    mean_nse_alto = df4[df4['NSE VIVIENDA'] == 'Alto/Medio']['VENTAS'].mean()
    mean_nse_medio = df4[df4['NSE VIVIENDA'] == 'Medio Bajo']['VENTAS'].mean()
    mean_nse_bajo = df4[df4['NSE VIVIENDA'] == 'Bajo/Muy Bajo']['VENTAS'].mean()

    df4 = df4.groupby(['NSE VIVIENDA']).agg({'VENTAS': 'sum'}).reset_index()

    st.subheader("Mayor Volumen de Ventas en Niveles Socioeconómicos Bajos")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-container"><div class="metric-title">Promedio de Ventas en NSE Bajo</div><div class="metric-value">{:.0f}</div></div>'.format(mean_nse_bajo), unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-container"><div class="metric-title">Promedio de Ventas en NSE Medio</div><div class="metric-value">{:.0f}</div></div>'.format(mean_nse_medio), unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-container"><div class="metric-title">Promedio de Ventas en NSE Alto</div><div class="metric-value">{:.0f}</div></div>'.format(mean_nse_alto), unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        custom_palette = ['#5e3c99', '#b58fc5', '#d8bfd8']
        fig = px.pie(df4, names='NSE VIVIENDA', values='VENTAS', 
             title='Ventas Totales por NSE',
             color_discrete_sequence=custom_palette)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig)
    with col2:
        st.markdown('<div class="hallazgo-container"><div class="titulo-hallazgo">Hallazgo:</div>Se ha descubierto que los vendedores con niveles socioeconómicos bajos generan un mayor volumen de ventas en comparación con otros niveles socioeconómicos. Puede haber factores específicos que pueden estar contribuyendo a esta situación.</div>', unsafe_allow_html=True)
        st.markdown('<div class="hallazgo-container"><div class="titulo-accion">Posible Acción:</div>Se recomienda dar premios, regalos o más beneficios a este sector de los vendedores por su gran esfuerzo. Asimismo, obtener vendedores con nivel socioeconómico medio y bajo para mejorar las ventas. Una posibilidad es que los de más alto nivel no se enfocan porque ser vendedor no es su único trabajo.</div>', unsafe_allow_html=True)

selected_hallazgo = st.sidebar.selectbox("Seleccione el Hallazgo", list(hallazgos.keys()))

if selected_hallazgo == "Primer Hallazgo":
    primer_hallazgo()
elif selected_hallazgo == "Segundo Hallazgo":
    segundo_hallazgo()
elif selected_hallazgo == "Tercer Hallazgo":
    tercer_hallazgo()
elif selected_hallazgo == "Cuarto Hallazgo":
    cuarto_hallazgo()
