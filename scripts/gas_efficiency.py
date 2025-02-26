import pandas as pd
import gas_constants as gc
import gas_func as gf

def convert_string_to_numeric(data):
    for col in data.columns:
        if data[col].dtype == 'object':
            data[col] = pd.to_numeric(data[col],errors='coerce')
    return data

def load_data_viana1(filepath):
    ### Read sheet VIANA 1 from the excel file.
    data = pd.read_excel(filepath,sheet_name='VIANA 1')
    data = convert_string_to_numeric(data)
    return data 

def load_data_lorm1(filepath):
    ### Read sheet LORM 1 from the excel file.
    data = pd.read_excel(filepath,sheet_name='LORM 1')
    data = convert_string_to_numeric(data)
    return data

def load_data_povoacao(filepath):
    ### Read sheet POVOACAO from the excel file.
    data = pd.read_excel(filepath,sheet_name='POVOAÇÃO')
    data = convert_string_to_numeric(data)
    return data

def load_data_lorm(filepath):
    ### Read sheet LORM from the excel file.
    data = pd.read_excel(filepath,sheet_name='LORM')
    data = convert_string_to_numeric(data)
    return data

def main():
    """Main function to execute the gas efficiency analysis."""
    filepath = '/Users/uzieljunior/Library/CloudStorage/OneDrive-EnevaS.A/EFICIÊNCIA/data/USINAS - Geração e Consumo.xlsx'

    ### Read all sheets from the excel file.
    data_viana1 = load_data_viana1(filepath)
    data_lorm1 = load_data_lorm1(filepath)
    data_pov = load_data_povoacao(filepath)
    data_lorm = load_data_lorm(filepath)

    ### read only the columns of interest for the PCS power plants.
    comp_gn_viana1 = data_viana1[gc.columns_esgas]
    ### transform to percentage
    comp_gn_viana1[gc.columns_comp_gn] /= 100
    ### calculate the efficiency of the gas in the power plant VIANA 1.
    comp_gn_viana1 = gf.calculate_efficiency(gf.calculate_PCI(gf.calculate_mass_fraction(gf.calculate_molar_mass_part(comp_gn_viana1))))

    comp_gn_lorm1 = data_lorm1[gc.columns_esgas]
    comp_gn_lorm1[gc.columns_comp_gn] /= 100
    ### calculate the efficiency of the gas in the power plant LORM 1.
    comp_gn_lorm1 = gf.calculate_efficiency(gf.calculate_PCI(gf.calculate_mass_fraction(gf.calculate_molar_mass_part(comp_gn_lorm1))))

    comp_gn_pov = data_pov[gc.columns_esgas]
    comp_gn_pov[gc.columns_comp_gn] /= 100
    ### calculate the efficiency of the gas in the power plant POVOACAO.
    comp_gn_pov = gf.calculate_efficiency(gf.calculate_PCI(gf.calculate_mass_fraction(gf.calculate_molar_mass_part(comp_gn_pov))))

    data_lorm['HeatRate'] = (data_lorm['m3'] * (data_lorm['PCI_Kcal/m3'] * gc.Kcal_Kj)) / data_lorm['MWh']
    data_lorm['Efficiency_%'] = (1 / ((data_lorm['HeatRate'] / 3600)/1000))*100

    filepath_output = '/Users/uzieljunior/Library/CloudStorage/OneDrive-EnevaS.A/EFICIÊNCIA/data/USINAS - Geração e Consumo_output.xlsx'
    with pd.ExcelWriter(filepath_output) as writer:
        comp_gn_viana1.to_excel(writer,sheet_name='VIANA 1',index=False)
        comp_gn_lorm1.to_excel(writer,sheet_name='LORM 1',index=False)
        comp_gn_pov.to_excel(writer,sheet_name='POVOACAO',index=False)
        data_lorm.to_excel(writer,sheet_name='LORM',index=False)

if __name__ == '__main__':
    main()
