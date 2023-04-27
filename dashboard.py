import streamlit as st
import pandas as pd
import plotly.express as px
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--filepath', help='path to csv file containing bank incomes and expenses')
parser.add_argument('--title', default='Report entrate uscite',
                    help='Main dashboard title')

args = parser.parse_args()

if __name__ == '__main__':
    df = pd.read_csv(args.filepath)
    df.Categoria.fillna('n.c.', inplace=True)
    df.Date = pd.to_datetime(df.Date) # ensure Date is parsed as Timestamp
    df.Date_Time = pd.to_datetime(df.Date_Time) # ensure Date is parsed as Timestamp

    st.title(args.title) 
    
    exclude_special = st.checkbox("Escludi transazioni speciali (giroconti, investimenti, ...)", value=True)

    if exclude_special:
        df_select = df.loc[~df.Transazione_speciale]
    else:
        df_select = df
    
    banche_select = st.multiselect("Seleziona banche", df.Banca.unique(), default=df.Banca.unique())
    df_select = df_select.loc[df.Banca.isin(banche_select)]

    tipo_trans_select = st.multiselect("Seleziona tipi transazione", df_select.Tipo_transazione.unique(), default=df_select.Tipo_transazione.unique())
    df_select = df_select.loc[df.Tipo_transazione.isin(tipo_trans_select)]

    cat_select = st.multiselect("Seleziona categorie", df_select.Categoria.unique(), default=df_select.Categoria.unique())
    df_select = df_select.loc[df.Categoria.isin(cat_select)]

    min_importo = int(df_select.Importo.min())-1
    max_importo = int(df_select.Importo.max())+1
    value_range = st.slider('Seleziona range di valori', min_importo, max_importo, 
                            (min_importo, max_importo))
    df_select = df_select.loc[(df_select.Importo >= value_range[0]) & (df_select.Importo <= value_range[1])]

    fig = px.scatter(df_select, x='Date', y="Importo", title='Singoli movimenti', hover_data=['Operazione','Dettagli'])
    
    st.plotly_chart(fig)

    monthly_data = df_select.set_index('Date_Time').groupby(pd.Grouper(freq='M'))['Importo'].agg(sum).reset_index()
    fig = px.line(monthly_data, x='Date_Time', y="Importo", title='Report mensile', markers=True)
    fig.add_hline(y=monthly_data.Importo.mean(), line_color='orange', line_dash="dash", 
                  annotation_text=f"media mensile: <b>{int(monthly_data.Importo.mean())} </b> Euro",
                  annotation=dict(font_size=15, font_color='orange'),
                  annotation_position="bottom right")
    fig.add_hline(y=monthly_data.tail(6).Importo.mean(), line_color='purple', line_dash="dash", 
                annotation_text=f"media mensile (ultimi 6 mesi): <b>{int(monthly_data.tail(6).Importo.mean())} </b> Euro",
                annotation=dict(font_size=15, font_color='purple'))
    fig.add_hline(y=0, line_color='green')
    st.plotly_chart(fig)

    monthly_data['Importo_cumulato'] = monthly_data.Importo.cumsum()
    fig = px.line(monthly_data, x='Date_Time', y="Importo_cumulato", title='Report mensile cumulato', markers=True)
    st.plotly_chart(fig)

    # report per banca e tipo transazione
    st.subheader("Totali per banca e tipo transazione")
    st.table(df_select.groupby(['Banca', 'Tipo_transazione'])['Importo'].sum().sort_values())

    # all selected data
    st.header('Dettagli movimenti')
    st.dataframe(df_select.drop(columns=['Valuta','Date_Time']))