import streamlit as st
import pandas as pd
import sqlite3
from WebScraping import refresh_database


st.set_page_config(page_title="ScoutDatabase", page_icon="⚽", layout="wide")#🌎
@st.cache_data
def carregar_dados():
    conn = sqlite3.connect('ScoutDatabase.db')
    tabela = pd.read_sql('SELECT * FROM players',conn)
    tabela['Height (cm)'] = pd.to_numeric(tabela['Height (cm)'], errors='coerce')  # Converter para numérico
    tabela['Height (cm)'] = tabela['Height (cm)'].fillna(0).astype('int64')  # Substituir NaN por 0 e converter para int64

    tabela = tabela.astype({'Birth Date': 'datetime64[ns]', 'Contract Expires': 'datetime64[ns]',
                            'Loan Contract Expires': 'datetime64[ns]', 'Age':'int64', 'Height (cm)':'int64'})#, 'On Loan': 'boolean'
    flags = pd.read_sql('SELECT * FROM flags',conn)
    tabela = pd.merge(left=tabela, right=flags, how='left', left_on='Nationality', right_on='country')
    tabela = tabela[
        ['Position','Player img url', 'Short Name','Age','Team img url', 'flag_img_url',  'Team',  'Nationality',
         'Foot', 'On Loan', 'Height (cm)', 'Market Value', 'Birth Date', 'Contract Expires', 'Full Name',
         'On Loan From','Loan Contract Expires', 'Citizenship', 'Player Agent', 'Player Agent Link', 'Instagram', 'Player ID','Transfermarkt Profile', 'PlaymakerStats Profile']]#'On Loan From',
    conn.close()
    return tabela

dados = carregar_dados()
raw_data = dados.copy()

st.session_state['dados'] = dados



#st.page_link('ScoutDatabase.py')
#st.page_link("pages/Player.py")

with st.container():

    st.title('ScoutDatabase🌎')
    st.subheader(f'{len(raw_data)} Jogadores em monitoramento')
    st.write('Jogadores em Observação:\nAcessar [Transfermarkt](https://www.transfermarkt.com/)')
    refresh = st.button('Refresh Database')
    if refresh:
        with st.spinner('Atualizando a base de dados...'):
            refresh_database('ScoutDatabase.db')
            st.session_state['dados'] = carregar_dados()  # Recarrega os dados após o refresh
            st.success('Database refreshed com sucesso!')        

with st.sidebar:
    st.title('Filter Conditions🔍')
    nationality = st.multiselect('Nationality', ['Any'] + sorted(list(dados['Nationality'].unique())), default=['Any'])
    if 'Any' not in nationality:
        dados = dados[dados['Nationality'].isin(nationality)]

    age_min, age_max = st.slider(
        "Age",
        min_value=int(raw_data['Age'].min()),
        max_value=int(raw_data['Age'].max()),
        value=[int(dados['Age'].min()), int(dados['Age'].max())]
    )
    dados = dados[(dados['Age'] >= age_min) & (dados['Age'] <= age_max)]

    height_min, height_max = st.slider(
        "Height (cm)",
        min_value=int(raw_data['Height (cm)'].min()),
        max_value=int(raw_data['Height (cm)'].max()),
        value=[int(dados['Height (cm)'].min()), int(dados['Height (cm)'].max())]
    )
    dados = dados[
        (dados['Height (cm)'].isna()) | ((dados['Height (cm)'] >= height_min) & (dados['Height (cm)'] <= height_max))]

    foot = st.selectbox('Preferred Foot', ['Any'] + list(dados['Foot'].unique()))
    if foot != 'Any':
        dados = dados[dados['Foot'] == foot]

    position = st.multiselect('Main Position', ['Any'] + sorted(list(dados['Position'].unique())), default=['Any'])
    if 'Any' not in position:
        dados = dados[dados['Position'].isin(position)]

with st.container():
    st.write('---')

    scoutdatabase = st.data_editor(dados,
                        column_config={
                            "Player ID": None,
                            "Player img url": st.column_config.ImageColumn("Player", width='small'),
                            'Team img url': st.column_config.ImageColumn('Team', width='small'),
                            'flag_img_url': st.column_config.ImageColumn('Flag', width='small'),
                            'Birth Date': st.column_config.DateColumn('Birth Date', width='small', format="YYYY-MM-DD"),
                            'Contract Expires': st.column_config.DateColumn('Contract Expires', width='small',format="YYYY-MM-DD"),
                            'Loan Contract Expires': st.column_config.DateColumn('Loan Contract Expires',width='small',format="YYYY-MM-DD"),
                            'Player Agent Link': st.column_config.LinkColumn('Player Agent Link', width='small'),
                            'Transfermarkt Profile': st.column_config.LinkColumn('Transfermarkt Profile', width='large'),
                            'PlaymakerStats Profile': st.column_config.LinkColumn('PlaymakerStats Profile', width='large'),
                            'On Loan': st.column_config.CheckboxColumn('On Loan', width='small')
                        },
                        hide_index=True,
                        disabled=dados.columns
                    )

