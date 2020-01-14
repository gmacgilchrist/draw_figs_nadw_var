import xarray as xr
def ariane_year(final_t,time,dim='nfile',yrst=0,secondsperyear=31536000):
    final_year = yrst + time.interp({dim:final_t})/secondsperyear
    final_year.name = 'final_year'
    return final_year