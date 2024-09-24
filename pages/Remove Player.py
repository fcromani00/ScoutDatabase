from WebScraping import remove_player
from ScoutDatabase import carregar_dados
import streamlit as st


st.set_page_config('Remove Player', page_icon="⚽")

st.title('Remove Player')

player_name = st.selectbox('Choose the player to remove', st.session_state['dados']['Short Name'].unique())

df_player_info = st.session_state.dados[st.session_state.dados['Short Name']==player_name]

st.subheader(f"{df_player_info['Full Name'].iloc[0]} - {df_player_info['Team'].iloc[0]}")
st.write(f"Position: {df_player_info['Position'].iloc[0]}")
st.image([df_player_info['Player img url'].iloc[0],df_player_info['Team img url'].iloc[0]], use_column_width='auto')

st.dataframe(df_player_info)

st.session_state['player_id'] = df_player_info['Player ID'].iloc[0]

remove = st.button('Remove Player')
if remove:
  remove_player(st.session_state.player_id, 'ScoutDatabase.db')
  del st.session_state.player_id
  st.session_state.dados = carregar_dados()
  st.success('Player removed successfully')

st.write(st.session_state.player_id)