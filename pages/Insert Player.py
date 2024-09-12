import pandas as pd
import streamlit as st
import sqlite3
from WebScraping import scraping_transfermarkt
from WebScraping import scraping_playmaker

st.set_page_config('Insert Player', page_icon="⚽")

st.title('Insert Player')
st.write('''Use these sites to insert new players:\n
[Transfermarkt](https://www.transfermarkt.com/)\n
[Playmaker](https://www.playmakerstats.com/)''')

tb_seasons_results = pd.DataFrame()
df_scoutdatabase = pd.DataFrame()
dict_scoutdatabase = {
    'Player img url': pd.NA,
    'Team img url': pd.NA,
    'Short Name': pd.NA,
    'Position': pd.NA,
    'Player ID': '000000',
    'Nationality': pd.NA,
    'Team': pd.NA,
    'Age': pd.NA,
    'Foot': pd.NA,
    'On Loan': pd.NA,
    'Birth Date': pd.NA,
    'Height (cm)': pd.NA,
    'Market Value': pd.NA,
    'Contract Expires': pd.NA,
    'Full Name': pd.NA,
    'On Loan From': pd.NA,
    'Loan Contract Expires': pd.NA,
    'Citizenship': pd.NA,
    'Player Agent': pd.NA,
    'Player Agent Link': pd.NA,
    'Instagram': pd.NA,
    'Flag img url': pd.NA
}

with st.form('Data Source'):
  st.write('Use links from the same player in both sites')
  link_TF = st.text_input('Player Profile in link Transfermarkt')
  if link_TF != '':
    dict_transfermarkt = scraping_transfermarkt(link_TF)

  link_PMS = st.text_input('Player Profile link in Playmaker')
  if link_PMS != '':
    dict_playmaker, tb_seasons_results = scraping_playmaker(link_PMS)

  submit = st.form_submit_button("Check collected data")
  if submit:
    try:

      dict_scoutdatabase['Player ID'] = dict_playmaker['Player ID']
      for key, value in dict_scoutdatabase.items():
        if pd.isna(
            dict_scoutdatabase[key]) and not pd.isna(dict_transfermarkt[key]):
          dict_scoutdatabase[key] = dict_transfermarkt[key]
        elif pd.isna(
            dict_scoutdatabase[key]) and not pd.isna(dict_playmaker[key]):
          dict_scoutdatabase[key] = dict_playmaker[key]

        df_player_info = pd.DataFrame([dict_scoutdatabase])
        df_player_performance = tb_seasons_results

    except:
      st.write('Error: Please check the link and try again')

st.write('---')

try:
  st.data_editor(df_player_info,
    column_config={
     "Player img url":st.column_config.ImageColumn("Player", width='small'),
     'Team img url':st.column_config.ImageColumn('Team', width='small'),
     'Player Agent Link':st.column_config.LinkColumn('Player Agent Link',width='small')
  },
  hide_index=True)
  st.data_editor(df_player_performance)
  insert = st.button('Insert Player in ScoutDatabase')
  if insert:
    conn = sqlite3.connect('ScoutDatabase.db')
    dados = pd.concat([dados, df_player_info], ignore_index=True)
    dados.to_sql('players', conn, if_exists='replace', index=False)

    performance = pd.concat([performance, df_player_performance], ignore_index=True)
    performance.to_sql('performance_seasons', conn, if_exists='replace', index=False)
    conn.close()

    st.success('Player inserted successfully')

    
except:
  st.dataframe(pd.DataFrame())
