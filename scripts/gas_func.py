import gas_constants as gc
def calculate_molar_mass_part(comp_gn):
    """Calculate the mass fraction of"""
    comp_gn['Methane_g/mol'] = comp_gn['CH4%_molar'] * gc.molar_mass['Methane']
    comp_gn['Ethane_g/mol'] = comp_gn['Etano%_molar'] * gc.molar_mass['Ethane']
    comp_gn['Propane_g/mol'] = comp_gn['Propano%_molar'] * gc.molar_mass['Propane']
    comp_gn['nButane_g/mol'] = comp_gn['n_Butano%_molar'] * gc.molar_mass['nButane']
    comp_gn['iButane_g/mol'] = comp_gn['Iso_Butano%_molar'] * gc.molar_mass['iButane']
    comp_gn['nPentane_g/mol'] = comp_gn['n_Pentano%_molar'] * gc.molar_mass['nPentane']
    comp_gn['iPentane_g/mol'] = comp_gn['I_Pentano%_molar'] * gc.molar_mass['iPentane']
    comp_gn['nHexane_g/mol'] = comp_gn['C6+%_molar'] * gc.molar_mass['nHexane']
    comp_gn['N2_g/mol'] = (comp_gn['N2+CO2%_molar'] - comp_gn['CO2%_molar']) * gc.molar_mass['N2']
    comp_gn['CO2_g/mol'] = comp_gn['CO2%_molar'] * gc.molar_mass['CO2']
    comp_gn['Molar_mass_part'] = comp_gn[gc.mol_prop_gn].sum(axis=1)
    return comp_gn

def calculate_mass_fraction(comp_gn):
    """Calculate the mass fraction of each component."""
    comp_gn['Methane_mass_frac'] = comp_gn['Methane_g/mol'] / comp_gn['Molar_mass_part']
    comp_gn['Ethane_mass_frac'] = comp_gn['Ethane_g/mol'] / comp_gn['Molar_mass_part']
    comp_gn['Propane_mass_frac'] = comp_gn['Propane_g/mol'] / comp_gn['Molar_mass_part']
    comp_gn['nButane_mass_frac'] = comp_gn['nButane_g/mol'] / comp_gn['Molar_mass_part']
    comp_gn['iButane_mass_frac'] = comp_gn['iButane_g/mol'] / comp_gn['Molar_mass_part']
    comp_gn['nPentane_mass_frac'] = comp_gn['nPentane_g/mol'] / comp_gn['Molar_mass_part']
    comp_gn['iPentane_mass_frac'] = comp_gn['iPentane_g/mol'] / comp_gn['Molar_mass_part']
    comp_gn['nHexane_mass_frac'] = comp_gn['nHexane_g/mol'] / comp_gn['Molar_mass_part']
    comp_gn['N2_mass_frac'] = comp_gn['N2_g/mol'] / comp_gn['Molar_mass_part']
    comp_gn['CO2_mass_frac'] = comp_gn['CO2_g/mol'] / comp_gn['Molar_mass_part']
    return comp_gn

def calculate_PCI(comp_gn):
    """Calculate the PCI of the gas."""
    comp_gn['PCI_KJ/Kg'] = comp_gn['Methane_mass_frac'] * gc.lhv['Methane'] + comp_gn['Ethane_mass_frac'] * gc.lhv['Ethane'] + comp_gn['Propane_mass_frac'] * gc.lhv['Propane'] + comp_gn['nButane_mass_frac'] * gc.lhv['nButane'] + comp_gn['iButane_mass_frac'] * gc.lhv['iButane'] + comp_gn['nPentane_mass_frac'] * gc.lhv['nPentane'] + comp_gn['iPentane_mass_frac'] * gc.lhv['iPentane'] + comp_gn['nHexane_mass_frac'] * gc.lhv['nHexane'] + comp_gn['N2_mass_frac'] * gc.lhv['N2'] + comp_gn['CO2_mass_frac'] * gc.lhv['CO2']
    return comp_gn

def calculate_efficiency(comp_gn):
    """Calculate gas efficiency metrics from the data."""
    comp_gn['HeatRate'] = (comp_gn['Kg/h'] * comp_gn['PCI_KJ/Kg']) / comp_gn['MWh']
    comp_gn['Efficiency_%'] = (1 / ((comp_gn['HeatRate'] / 3600)/1000))*100
    return comp_gn
