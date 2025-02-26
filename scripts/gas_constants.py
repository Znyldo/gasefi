Bar_to_pascal = 100000
Ref_perf_gas = 8.31441
Celcius_to_kelvin = 273.15
Nist_temperature = 20
Nist_pressure = 1.01325
Kcal_Kj = 4.184

comp_list = ('Methane', 'Ethane', 'Propane', 'nButane', 'iButane', 'nPentane','iPentane', 'nHexane','N2','CO2')

molar_mass = {'Methane':16.04246,
               'Ethane':30.06904, 
               'Propane':44.09562, 
               'nButane':58.1222, 
               'iButane':58.1222, 
               'nPentane':72.14878, 
               'iPentane':72.14878, 
               'nHexane':86.17536, 
               'Hydrogen Sulfide':34.08088, 
               'N2':28.0134, 
               'CO2':44.0095, 
               'Water':18.01528
               }

temperature_crit = {'Methane':190.564, 
                    'Ethane':305.32, 
                    'Propane':369.83, 
                    'nButane':425.12, 
                    'iButane':408.14, 
                    'nPentane':469.7, 
                    'iPentane':460.43, 
                    'nHexane':507.6, 
                    'Hydrogen Sulfide':373.53, 
                    'N2':126.2, 
                    'CO2':304.21, 
                    'Water':647.13
                    }

pressure_crit = {'Methane':45.99, 
                 'Ethane':48.5, 
                 'Propane':42.1, 
                 'nButane':37.7, 
                 'iButane':36.2, 
                 'nPentane':33.6, 
                 'iPentane':33.7, 
                 'nHexane':30.4, 
                 'Hydrogen Sulfide':90, 
                 'N2':33.9, 
                 'CO2':73.9, 
                 'Water':219.4}

lhv = {'Methane':50048, 
        'Ethane':47511, 
        'Propane':46330, 
        'nButane':45725, 
        'iButane':45577, 
        'nPentane':45343, 
        'iPentane':45249, 
        'nHexane':44733.86, 
        'Hydrogen Sulfide':15191.988, 
        'N2':0, 
        'CO2':0
        }

hhv = {'Methane':55540.1, 
       'Ethane':51910, 
       'Propane':50322, 
       'nButane':49511, 
       'iButane':49363, 
       'nPentane':49003, 
       'iPentane':48909, 
       'nHexane':48309.19, 
       'Hydrogen Sulfide':16493.428, 
       'N2':0, 
       'CO2':0
       }

columns_esgas = ['Data',
                 'Kg/h',
                 'MWh',
                 'CH4%_molar',
                 'Etano%_molar',
                 'Propano%_molar',
                 'Iso_Butano%_molar',
                 'n_Butano%_molar',
                 'I_Pentano%_molar',
                 'n_Pentano%_molar',
                 'C6+%_molar',
                 'N2+CO2%_molar',
                 'CO2%_molar',
                 'O2%_molar']

columns_comp_gn = [
                 'CH4%_molar',
                 'Etano%_molar',
                 'Propano%_molar',
                 'Iso_Butano%_molar',
                 'n_Butano%_molar',
                 'I_Pentano%_molar',
                 'n_Pentano%_molar',
                 'C6+%_molar',
                 'N2+CO2%_molar',
                 'CO2%_molar',
                 'O2%_molar']

mol_prop_gn = ['Methane_g/mol',
               'Ethane_g/mol',
               'Propane_g/mol',
               'nButane_g/mol',
               'iButane_g/mol',
               'nPentane_g/mol',
               'iPentane_g/mol',
               'nHexane_g/mol',
               'N2_g/mol',
               'CO2_g/mol']
