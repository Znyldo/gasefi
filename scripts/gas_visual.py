import streamlit as st
import pandas as pd
import plotly.express as px
import visual_config as vc

@st.cache_data
def load_data_viana1(path: str):
    data = pd.read_excel(path, sheet_name="VIANA 1")
    data.rename(columns={'Kg/h': 'Kilograma'}, inplace=True)
    data['HeatRate'] = data['HeatRate']/1000
    data[['HeatRate','Efficiency_%','PCI_KJ/Kg','Kilograma','MWh']] = data[['HeatRate','Efficiency_%','PCI_KJ/Kg','Kilograma','MWh']].round(2)
    
    if data.empty:
        st.warning("The dataset is empty.")
        
    return data
@st.cache_data
def load_data_lorm1(path: str):
    data = pd.read_excel(path, sheet_name = "LORM 1")
    data.rename(columns={'Kg/h': 'Kilograma'}, inplace=True)
    data['HeatRate'] = data['HeatRate']/1000
    data[['HeatRate','Efficiency_%','PCI_KJ/Kg','Kilograma','MWh']] = data[['HeatRate','Efficiency_%','PCI_KJ/Kg','Kilograma','MWh']].round(2)
    
    if data.empty:
        st.warning("The dataset is empty.")
        
    return data
@st.cache_data
def load_data_povoacao(path: str):
    data = pd.read_excel(path, sheet_name = "POVOACAO")
    data.rename(columns={'Kg/h': 'Kilograma'}, inplace=True)
    data['HeatRate'] = data['HeatRate']/1000
    data[['HeatRate','Efficiency_%','PCI_KJ/Kg','Kilograma','MWh']] = data[['HeatRate','Efficiency_%','PCI_KJ/Kg','Kilograma','MWh']].round(2)
    
    if data.empty:
        st.warning("The dataset is empty.")
        
    return data
@st.cache_data
def load_data_lorm(path: str):
    data = pd.read_excel(path, sheet_name = "LORM")
    data['HeatRate'] = data['HeatRate']/1000
    data[['HeatRate','Efficiency_%','MWh']] = data[['HeatRate','Efficiency_%','MWh']].round(2)
    
    if data.empty:
        st.warning("The dataset is empty.")
        
    return data

def format_change(val):
    """Change the color of the text based on the value."""
    return "color: green;" if (val > 44.34 and val < 45.01) else "color: darkorange;" if (val < 44.34 and val > 43.68) else "color: red;" if (val < 43.68) else "color: blue;"

path_data = "/Users/uzieljunior/Library/CloudStorage/OneDrive-EnevaS.A/EFICIÊNCIA/data/USINAS - Geração e Consumo_output.xlsx"

def main():
    st.set_page_config(page_title="Gás e Eficiência", page_icon=":fire:",layout="wide")
    st.title("Gas e Eficiência")
    df_gas_viana1 = load_data_viana1(path_data)
    df_gas_lorm1 = load_data_lorm1(path_data)
    df_gas_povoacao = load_data_povoacao(path_data)
    df_gas_lorm = load_data_lorm(path_data)
    
    tab_viana1, tab_lorm1, tab_povoacao, tab_lorm = st.tabs(["VIANA 1", "LORM 1", "POVOACAO", "LORM"])

### VIANA 1 TAB
    with tab_viana1:
        with st.expander("**_Clique para ver os dados_**"):
            st.dataframe(df_gas_viana1, hide_index=True)
            
        st.markdown("---")
        colum1, colum2 = st.columns([0.2,0.7])  
        with colum1:  
            if 'Data' in df_gas_viana1.columns:
                uniques_dates = sorted(df_gas_viana1['Data'].dropna().unique())
                selected_date = st.selectbox("Selecione a data", 
                                                options=uniques_dates, 
                                                format_func=lambda x: x.strftime("%Y-%m-%d"),
                                                key='viana1')
                selected_row = df_gas_viana1[df_gas_viana1['Data'] == selected_date].iloc[0]
            else:
                st.info("Coluna 'Data' não encontrada.")
                selected_row = df_gas_viana1.iloc[-1]

        ignore_columns = ['Data', 'Kilograma', 'MWh', 'PCI_KJ/Kg', 'HeatRate', 'Efficiency_%']
        comp_columns = [col for col in df_gas_viana1.columns if col not in ignore_columns and 'Molar_mass_part' not in col and 'mass_frac' not in col and 'g/mol' not in col]

        col1, col2, col3, col4 = st.columns([0.25,0.15,0.25,0.25])

        with col1:
            if comp_columns:
                comp_values = selected_row[comp_columns]
                fig = px.pie(values=comp_values.values,
                            names=comp_columns,
                            hole=0.5,
                            color_discrete_sequence=vc.paleta_cores_eneva)
                st.plotly_chart(fig)
            else:
                st.info("Colunas de composição do gás não encontradas.")

            if 'HeatRate' in df_gas_viana1.columns and pd.notnull(selected_row['HeatRate']):
                heat_rate = selected_row['HeatRate']
                st.write(f"**Heat Rate:** {heat_rate} KJ/Kg")
            
            if 'Efficiency_%' in df_gas_viana1.columns and pd.notnull(selected_row['Efficiency_%']):
                efficiency = selected_row['Efficiency_%']
                css_style = format_change(efficiency)
                st.markdown(f"**Eficiência:** <span style='{css_style}'>{efficiency:.2f}%</span>", unsafe_allow_html=True)
                
        with col2:
            hr_viana1 = df_gas_viana1[['Data', 'HeatRate', 'Efficiency_%']].dropna()
            styled_df = hr_viana1.style.format({'HeatRate': '{:.2f}', 'Efficiency_%': '{:.2f}', 'Data': '{:%Y-%m-%d}'}).applymap(format_change, subset=['Efficiency_%'])
            st.dataframe(styled_df, hide_index=True)

        with col3:
            monthly_avg = hr_viana1.set_index('Data').resample('ME').mean().reset_index()
            fig_hr = px.scatter(monthly_avg,
                                 x='Data', 
                                 y='HeatRate', 
                                 title='Heat Rate VIANA 1 - Média Mensal',
                                 labels={'Data': '', 'HeatRate': 'Heat Rate (KJ/Kg)'},
                                 text='HeatRate',
                                 color_discrete_sequence=vc.paleta_cores_eneva)
            
            fig_hr.update_traces(marker_symbol='diamond', 
                                 marker_size=10,
                                 texttemplate='<b>%{text:.0f}</b>',
                                 textposition='top center')

            st.plotly_chart(fig_hr, 
                            use_container_width=True)
            hr_mean = hr_viana1['HeatRate'].mean()
            st.write(f"**Heat Rate médio:** {hr_mean:.2f} KJ/Kg")

        with col4:    
            fig_eff = px.scatter(monthly_avg, 
                                 x='Data', 
                                 y='Efficiency_%', 
                                 title='Eficiência VIANA 1 - Média Mensal',
                                 labels={'Data': '', 'Efficiency_%': 'Eficiência (%)'},
                                 text='Efficiency_%',
                                 color_discrete_sequence=vc.paleta_cores_eneva[4:])
            
            fig_eff.update_traces(marker_symbol='triangle-up',
                                  marker_size=10,
                                  texttemplate='<b>%{y:.2f}</b>',
                                  textposition='top center')
            
            st.plotly_chart(fig_eff, 
                            use_container_width=True)
            
            eff_mean = hr_viana1['Efficiency_%'].mean()
            css_style = format_change(eff_mean)
            st.markdown(f'**Eficiência média:** <span style="{css_style}">{eff_mean:.2f}%</span>', unsafe_allow_html=True)

### LORM 1 TAB           
    with tab_lorm1:
        with st.expander("**_Clique para ver os dados_**"):
            st.dataframe(df_gas_lorm1, hide_index=True)

        st.markdown("---")
        colum1, colum2 = st.columns([0.2,0.7])
        with colum1:
            if 'Data' in df_gas_lorm1.columns:
                uniques_dates = sorted(df_gas_lorm1['Data'].dropna().unique())
                selected_date = st.selectbox("Selecione a data", 
                                                options=uniques_dates, 
                                                format_func=lambda x: x.strftime("%Y-%m-%d"),
                                                key='lorm1')
                selected_row = df_gas_lorm1[df_gas_lorm1['Data'] == selected_date].iloc[0]
            else:
                st.info("Coluna 'Data' não encontrada.")
                selected_row = df_gas_lorm1.iloc[-1]

        ignore_columns = ['Data', 'Kilograma', 'MWh', 'PCI_KJ/Kg', 'HeatRate', 'Efficiency_%']
        comp_columns = [col for col in df_gas_viana1.columns if col not in ignore_columns and 'Molar_mass_part' not in col and 'mass_frac' not in col and 'g/mol' not in col]

        col1, col2, col3, col4 = st.columns([0.25,0.15,0.25,0.25])

        with col1:
            if comp_columns:
                comp_values = selected_row[comp_columns]
                fig_lorm1 = px.pie(values=comp_values.values,
                            names=comp_columns,
                            hole=0.5,
                            color_discrete_sequence=vc.paleta_cores_eneva)
                st.plotly_chart(fig_lorm1, use_container_width=True, key='lorm1_pie')
            else:
                st.info("Colunas de composição do gás não encontradas.")

            if 'HeatRate' in df_gas_viana1.columns and pd.notnull(selected_row['HeatRate']):
                heat_rate = selected_row['HeatRate']
                st.write(f"**Heat Rate:** {heat_rate} KJ/Kg")
            
            if 'Efficiency_%' in df_gas_viana1.columns and pd.notnull(selected_row['Efficiency_%']):
                efficiency = selected_row['Efficiency_%']
                css_style = format_change(efficiency)
                st.markdown(f"**Eficiência:** <span style='{css_style}'>{efficiency:.2f}%</span>", unsafe_allow_html=True)

        with col2:
            hr_lorm1 = df_gas_lorm1[['Data', 'HeatRate', 'Efficiency_%']].dropna()
            styled_df = hr_lorm1.style.format({'HeatRate': '{:.2f}', 'Efficiency_%': '{:.2f}', 'Data': '{:%Y-%m-%d}'}).applymap(format_change, subset=['Efficiency_%'])
            st.dataframe(styled_df, hide_index=True)

        with col3:
            monthly_avg = hr_lorm1.set_index('Data').resample('ME').mean().reset_index()
            fig_hr = px.scatter(monthly_avg,
                                 x='Data', 
                                 y='HeatRate', 
                                 title='Heat Rate LORM 1 - Média Mensal',
                                 labels={'Data': '', 'HeatRate': 'Heat Rate (KJ/Kg)'},
                                 text='HeatRate',
                                 color_discrete_sequence=vc.paleta_cores_eneva)        

            fig_hr.update_traces(marker_symbol='diamond', 
                                 marker_size=10,
                                 texttemplate='<b>%{text:.0f}</b>',
                                 textposition='top center')
            st.plotly_chart(fig_hr, 
                            use_container_width=True)
            hr_mean = hr_lorm1['HeatRate'].mean()
            st.write(f"**Heat Rate médio:** {hr_mean:.2f} KJ/Kg")

        with col4:
            fig_eff = px.scatter(monthly_avg, 
                                 x='Data', 
                                 y='Efficiency_%', 
                                 title='Eficiência LORM 1 - Média Mensal',
                                 labels={'Data': '', 'Efficiency_%': 'Eficiência (%)'},
                                 text='Efficiency_%',
                                 color_discrete_sequence=vc.paleta_cores_eneva[4:])
            
            fig_eff.update_traces(marker_symbol='triangle-up',
                                  marker_size=10,
                                  texttemplate='<b>%{y:.2f}</b>',
                                  textposition='top center')

            st.plotly_chart(fig_eff, 
                            use_container_width=True)

            eff_mean = hr_lorm1['Efficiency_%'].mean()
            css_style = format_change(eff_mean)
            st.markdown(f'**Eficiência média:** <span style="{css_style}">{eff_mean:.2f}%</span>', unsafe_allow_html=True)

### POVOACAO TAB
    with tab_povoacao:
        with st.expander("**_Clique para ver os dados_**"):
            st.dataframe(df_gas_povoacao, hide_index=True)

        st.markdown("---")
        colum1, colum2 = st.columns([0.2,0.7])
        with colum1:
            if 'Data' in df_gas_povoacao.columns:
                uniques_dates = sorted(df_gas_povoacao['Data'].dropna().unique())
                selected_date = st.selectbox("Selecione a data", 
                                                options=uniques_dates, 
                                                format_func=lambda x: x.strftime("%Y-%m-%d"),
                                                key='povoacao')
                selected_row = df_gas_povoacao[df_gas_povoacao['Data'] == selected_date].iloc[0]
            else:
                st.info("Coluna 'Data' não encontrada.")
                selected_row = df_gas_povoacao.iloc[-1]


        ignore_columns = ['Data', 'Kilograma', 'MWh', 'PCI_KJ/Kg', 'HeatRate', 'Efficiency_%']
        comp_columns = [col for col in df_gas_viana1.columns if col not in ignore_columns and 'Molar_mass_part' not in col and 'mass_frac' not in col and 'g/mol' not in col]

        col1, col2, col3, col4 = st.columns([0.25,0.15,0.25,0.25])

        with col1:
            if comp_columns:
                comp_values = selected_row[comp_columns]
                fig_pov = px.pie(values=comp_values.values,
                            names=comp_columns,
                            hole=0.5,
                            color_discrete_sequence=vc.paleta_cores_eneva)
                st.plotly_chart(fig_pov, use_container_width=True, key='povoacao_pie')
            else:
                st.info("Colunas de composição do gás não encontradas.")

            if 'HeatRate' in df_gas_viana1.columns and pd.notnull(selected_row['HeatRate']):
                heat_rate = selected_row['HeatRate']
                st.write(f"**Heat Rate:** {heat_rate} KJ/Kg")
            
            if 'Efficiency_%' in df_gas_viana1.columns and pd.notnull(selected_row['Efficiency_%']):
                efficiency = selected_row['Efficiency_%']
                css_style = format_change(efficiency)
                st.markdown(f"**Eficiência:** <span style='{css_style}'>{efficiency:.2f}%</span>", unsafe_allow_html=True)

        with col2:
            hr_povoacao = df_gas_povoacao[['Data', 'HeatRate', 'Efficiency_%']].dropna()
            styled_df = hr_povoacao.style.format({'HeatRate': '{:.2f}', 'Efficiency_%': '{:.2f}', 'Data': '{:%Y-%m-%d}'}).applymap(format_change, subset=['Efficiency_%'])
            st.dataframe(styled_df, hide_index=True)

        with col3:
            monthly_avg = hr_povoacao.set_index('Data').resample('ME').mean().reset_index()
            fig_hr = px.scatter(monthly_avg,
                                 x='Data', 
                                 y='HeatRate', 
                                 title='Heat Rate POVOACAO - Média Mensal',
                                 labels={'Data': '', 'HeatRate': 'Heat Rate (KJ/Kg)'},
                                 text='HeatRate',
                                 color_discrete_sequence=vc.paleta_cores_eneva)        

            fig_hr.update_traces(marker_symbol='diamond', 
                                 marker_size=10,
                                 texttemplate='<b>%{text:.0f}</b>',
                                 textposition='top center')
            st.plotly_chart(fig_hr, 
                            use_container_width=True)
            
            hr_mean_povoacao = df_gas_povoacao['HeatRate'].mean()
            st.write(f"**Heat Rate médio:** {hr_mean_povoacao:.2f} KJ/Kg")

        with col4:
            fig_eff = px.scatter(monthly_avg, 
                                 x='Data', 
                                 y='Efficiency_%', 
                                 title='Eficiência POVOACAO - Média Mensal',
                                 labels={'Data': '', 'Efficiency_%': 'Eficiência (%)'},
                                 text='Efficiency_%',
                                 color_discrete_sequence=vc.paleta_cores_eneva[4:])
            
            fig_eff.update_traces(marker_symbol='triangle-up',
                                  marker_size=10,
                                  texttemplate='<b>%{y:.2f}</b>',
                                  textposition='top center')

            st.plotly_chart(fig_eff, 
                            use_container_width=True)

            eff_mean = hr_povoacao['Efficiency_%'].mean()
            css_style = format_change(eff_mean)
            st.markdown(f'**Eficiência média:** <span style="{css_style}">{eff_mean:.2f}%</span>', unsafe_allow_html=True)

### LORM TAB
    with tab_lorm:
        with st.expander("**_Clique para ver os dados_**"):
            st.dataframe(df_gas_lorm, hide_index=True)

        st.markdown("---")
        colum1, colum2 = st.columns([0.2,0.7])
        with colum1:
            if 'Data' in df_gas_lorm.columns:
                uniques_dates = sorted(df_gas_lorm['Data'].dropna().unique())
                selected_date = st.selectbox("Selecione a data", 
                                                options=uniques_dates, 
                                                format_func=lambda x: x.strftime("%Y-%m-%d"),
                                                key='lorm')
                selected_row = df_gas_lorm[df_gas_lorm['Data'] == selected_date].iloc[0]
            else:
                st.info("Coluna 'Data' não encontrada.")
                selected_row = df_gas_lorm.iloc[-1]

        ignore_columns = ['Data', 'MWh', 'HeatRate', 'Efficiency_%', 'm3', 'm3_Corrigido', 'IW_kJ/m3', 'PCS_kcal/m3', 'PCI_Kcal/m3', 'm3/MWh', 'PCS_KJ/M3','NM', 'MWh_med','FatorPCS','Dens_Kg/m3','Dens_Rel ']
        comp_columns = [col for col in df_gas_lorm.columns if col not in ignore_columns and 'Molar_mass_part' not in col and 'mass_frac' not in col and 'g/mol' not in col]

        col1, col2, col3, col4 = st.columns([0.25,0.15,0.25,0.25])

        with col1:
            if comp_columns:
                comp_values = selected_row[comp_columns]
                fig_lorm = px.pie(values=comp_values.values,
                            names=comp_columns,
                            hole=0.5,
                            color_discrete_sequence=vc.paleta_cores_eneva)
                st.plotly_chart(fig_lorm, use_container_width=True, key='lorm_pie')
            else:
                st.info("Colunas de composição do gás não encontradas.")

            if 'HeatRate' in df_gas_lorm.columns and pd.notnull(selected_row['HeatRate']):
                heat_rate = selected_row['HeatRate']
                st.write(f"**Heat Rate:** {heat_rate} KJ/Kg")
            
            if 'Efficiency_%' in df_gas_lorm.columns and pd.notnull(selected_row['Efficiency_%']):
                efficiency = selected_row['Efficiency_%']
                css_style = format_change(efficiency)
                st.markdown(f"**Eficiência:** <span style='{css_style}'>{efficiency:.2f}%</span>", unsafe_allow_html=True)

        with col2:
            hr_lorm = df_gas_lorm[['Data', 'HeatRate', 'Efficiency_%']].dropna()
            hr_lorm = hr_lorm[hr_lorm['Efficiency_%'] < 50]
            styled_df = hr_lorm.style.format({'HeatRate': '{:.2f}', 'Efficiency_%': '{:.2f}', 'Data': '{:%Y-%m-%d}'}).applymap(format_change, subset=['Efficiency_%'])
            st.dataframe(styled_df, hide_index=True)

        with col3:
            monthly_avg = hr_lorm.set_index('Data').resample('ME').mean().reset_index()
            fig_hr = px.scatter(monthly_avg,
                                 x='Data', 
                                 y='HeatRate', 
                                 title='Heat Rate LORM - Média Mensal',
                                 labels={'Data': '', 'HeatRate': 'Heat Rate (KJ/Kg)'},
                                 text='HeatRate',
                                 color_discrete_sequence=vc.paleta_cores_eneva)        

            fig_hr.update_traces(marker_symbol='diamond', 
                                 marker_size=10,
                                 texttemplate='<b>%{text:.0f}</b>',
                                 textposition='top center')
            st.plotly_chart(fig_hr, 
                            use_container_width=True)
            
            hr_mean_lorm = df_gas_lorm['HeatRate'].mean()
            st.write(f"**Heat Rate médio:** {hr_mean_lorm:.2f} KJ/Kg")

        with col4:
            fig_eff = px.scatter(monthly_avg, 
                                 x='Data', 
                                 y='Efficiency_%', 
                                 title='Eficiência LORM - Média Mensal',
                                 labels={'Data': '', 'Efficiency_%': 'Eficiência (%)'},
                                 text='Efficiency_%',
                                 color_discrete_sequence=vc.paleta_cores_eneva[4:])
            
            fig_eff.update_traces(marker_symbol='triangle-up',
                                  marker_size=10,
                                  texttemplate='<b>%{y:.2f}</b>',
                                  textposition='top center')

            st.plotly_chart(fig_eff, 
                            use_container_width=True)

            eff_mean = hr_lorm['Efficiency_%'].mean()
            css_style = format_change(eff_mean)
            st.markdown(f'**Eficiência média:** <span style="{css_style}">{eff_mean:.2f}%</span>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
