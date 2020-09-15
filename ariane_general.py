import xarray as xr
def ariane_year(final_t,time,dim='nfile',yrst=0,secondsperyear=31536000):
    '''Calculate the year of ventilation based on the time-index of ventilation
    INPUT:  final_t ; array of time-indices
            time    ; array of times (in seconds) for each index
            dim     ; dimension in [time]
            yrst    ; year of first model outut
            secondsperyear
    OUTPUT: final_year ; array (same length as final_t) of years'''
    
    final_year = yrst + time.interp({dim:final_t})/secondsperyear
    final_year.name = 'final_year'
    return final_year