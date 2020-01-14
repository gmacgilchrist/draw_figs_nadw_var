import numpy as np
import scipy.io as sio
from matplotlib import pyplot as plt
import xarray as xr
from xhistogram.xarray import histogram as hist
from thermodynamics import calc_sigmantr
from ariane_distributionfunctions import ariane_D1, ariane_D2, ariane_D3, ariane_D4

rootdir = '/home/ocean_personal_data/graemem/ariane/'
model = 'orca025_global_5d'
experiment = 'quant_back_seedNAn1_t*_sign27.7-28_MLrefz8delsig0.01'
filepath = rootdir+'experiments/'+model+'/'+experiment+'/ariane_positions_quantitative.nc'
filepath_initial = rootdir+'experiments/'+model+'/'+experiment+'/ariane_initial.nc'
filepath_time = rootdir+'time/time_orca025_global_5d.mat'
filepath_region = rootdir+'experiments/'+model+'/quant_back_seedNAn1_t3560-sep-4217_sign27.7-28_MLrefz8delsig0.01/region_limits'
# Universal variables
spy = 365*24*60*60
yrst = 1958
yrend = 2016
ventsec = 7
lastinit = 4217

# Ariane input
ds_initial = xr.open_mfdataset(filepath_initial,combine='nested',concat_dim='ntraj')
ds_initial.init_volume.name = 'init_volume'
# Ariane output
ds = xr.open_mfdataset(filepath,combine='nested',concat_dim='ntraj')
ds = xr.merge([ds, ds_initial.init_volume])
ds['final_age'] = ds.final_age.astype('timedelta64[s]').astype('float64')/spy
ds['final_dens'] = calc_sigmantr(ds.final_temp,ds.final_salt)
# Model times
time_vals = np.append(np.array([0]),sio.loadmat(filepath_time)['time'].squeeze())
time = xr.DataArray(time_vals,dims=['nfile'],coords={'nfile':np.arange(time_vals.size)})
# Reagion limits
region_limits = np.loadtxt(filepath_region)

# Bins
years = np.arange(yrst,yrend+1)
ages = np.arange(-3/12,yrend-yrst+9/12)
densities = np.arange(27.7,28,0.01)
init_t_unique = np.unique(ds.init_t)
inits = np.append(init_t_unique-0.5,init_t_unique[-1]+0.5)
xs = np.arange(region_limits[0,0],region_limits[0,1])
ys = np.arange(region_limits[1,0],region_limits[1,1])

var1 = ds.final_x
var2 = ds.final_y
var3 = ds.final_age
var4 = ds.init_t

bins = [xs,ys,ages,inits]
weights = ds.init_volume

S = (ds.final_section==ventsec)
subsetname = 'final_section-7'

D4 = ariane_D4(
    var1=var1,
    var2=var2,
    var3=var3,
    var4=var4,
    bins=bins,
    dim=['ntraj'],
    weights=weights,
    subset=True,
    conditional=S,
    subsetname=subsetname,
    verbose=True,
    save=True
        )
