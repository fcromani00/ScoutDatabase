# import pandas as pd
# import sqlite3
from WebScraping import refresh_database
# from WebScraping import scraping_playmaker
# from WebScraping import scraping_transfermarkt


refresh_database('ScoutDatabase.db')

# scraping_playmaker('https://www.playmakerstats.com/player/brayan-medina/960088')
# # scraping_transfermarkt('')

# # Ler as diferentes planilhas (sheets) da planilha Excel
# flags = pd.read_excel('ScoutDatabase.xlsx', sheet_name='Flags')
# players = pd.read_excel('ScoutDatabase.xlsx', sheet_name='Players')
# performance = pd.read_excel('ScoutDatabase.xlsx', sheet_name='PerformanceSeasons')

# # Exibir as colunas da tabela 'Players' para verificação
# print(players.columns)

# # Conectar ao banco de dados SQLite (será criado se não existir)
# conn = sqlite3.connect('ScoutDatabase2.db')
# cur = conn.cursor()

# # Inserir os dados de cada tabela no banco de dados SQLite
# flags.to_sql('flags', conn, if_exists='replace', index=False)
# players.to_sql('players', conn, if_exists='replace', index=False)
# performance.to_sql('performance_seasons', conn, if_exists='replace', index=False)

# # Realizar uma consulta na tabela 'players'
# cur.execute("SELECT * FROM players")
# rows = cur.fetchall()

# # Exibir os resultados da consulta
# for row in rows:
#     print(row)

# # Fechar o cursor e a conexão com o banco de dados
# cur.close()
# conn.close()


