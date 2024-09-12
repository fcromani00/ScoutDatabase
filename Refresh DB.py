import pandas as pd
import sqlite3

def refresh_database(df):
  conn = sqlite3.connect('ScoutDatabase2.db')
  players = pd.read_sql('SELECT * FROM players', conn)
  performance = pd.read_sql('SELECT * FROM performance_seasons', conn)

  for link in players[['Transfermarkt Profile', 'Playmaker Profile']].itterows():
      dict_transfermarkt = { # Criando dict pra armazenar as informações
        'Player ID':'000000',
        'Short Name': pd.NA,
        'Full Name': pd.NA,
        'Birth Date': pd.NA,
        'Age': pd.NA,
        'Nationality':pd.NA,
        'Citizenship': pd.NA,
        'Team': pd.NA,
        'Position': pd.NA,
        'Market Value': pd.NA,
        'Foot': pd.NA,
        'Height (cm)': pd.NA,
        'Player Agent': pd.NA,
        'Player Agent Link':pd.NA,
        'Contract Expires':pd.NA,
        'On Loan': False,
        'Loan Contract Expires' : pd.NA,
        'Instagram': pd.NA,
        'Flag img url':pd.NA,
        'Player img url':pd.NA,
        'Team img url':  pd.NA,
        'Transfermarkt Profile': pd.NA,
        'PlaymakerStats Profile': pd.NA
      }
      dict_playmaker = dict_scoutdatabase
      dict_transfermarkt = dict_scoutdatabase

      link_TF = row.iloc[1] # Pegando o link na base_links['LINK Transfermarkt']
      if link_TF != '':
        dict_transfermarkt = scraping_transfermarkt(link_TF) # Fazendo scraping utilizando o link

      link_PMS = row.iloc[2] # Pegando o link na base_links['LINK Playmaker']
      if link_PMS != '':
        dict_playmaker, seasons_results_df = scraping_playmaker(link_PMS) # Fazendo scraping utilizando o link
      tb_seasons_results = pd.concat([tb_seasons_results, seasons_results_df], ignore_index=True)


      dict_scoutdatabase['Player ID'] = dict_playmaker['Player ID']

      for key, value in dict_scoutdatabase.items():
        if pd.isna(dict_scoutdatabase[key]) and not pd.isna(dict_transfermarkt[key]):
          dict_scoutdatabase[key] = dict_transfermarkt[key]
        elif pd.isna(dict_scoutdatabase[key]) and not pd.isna(dict_playmaker[key]):
          dict_scoutdatabase[key] = dict_playmaker[key]

        df_player_info = pd.DataFrame([dict_scoutdatabase])

      df_scoutdatabase = pd.concat([df_scoutdatabase, df_player_info], ignore_index=True)