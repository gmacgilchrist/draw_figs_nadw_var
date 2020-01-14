import numpy as np
import xarray as xr
from xhistogram.xarray import histogram as hist
from thermodynamics import calc_sigmantr

rootdir = '/home/ocean_shared_data1/DRAKKAR/ORCA025.L75-GJM189-S/'
config = 'ORCA025.L75-GJM189'
filepath = rootdir+'*/'+config+'_y*m0[34]d*_gridT.nc'
filepath_hgrid = rootdir+'GRID/'+config+'_mesh_hgr.nc'
filepath_zgrid = rootdir+'GRID/'+config+'_mesh_zgr.nc'
lonrange = [-100,30]
latrange = [-30,80]

# Load grid
ds_grid = xr.merge([xr.open_dataset(filepath_hgrid),xr.open_dataset(filepath_zgrid)],compat='override').squeeze()
# Change name of depth variable and drop time_counter
ds_grid = ds_grid.rename({'z':'deptht'}).assign_coords({'deptht':ds_grid.gdept_0.values}).drop('time_counter')
ds_grid = ds_grid

# Load data files
ds_T = xr.open_mfdataset(filepath,combine='by_coords',parallel=True)
# Merge with grid
ds_T = ds_T.update(ds_grid);

# Select upper 50m
ds_T = ds_T.sel(deptht=slice(0,50))
# Isolate North Atlantic
NAcondition = (ds_T.nav_lon>=lonrange[0]) & (ds_T.nav_lon<=lonrange[1]) & (ds_T.nav_lat>=latrange[0]) & (ds_T.nav_lat<=latrange[1])
ds_T = ds_T.where(NAcondition,drop=True)

# Calculate neutral density
ds_T['vosigmantr'] = xr.apply_ufunc(calc_sigmantr, ds_T.votemper, ds_T.vosaline,
                      dask='parallelized', output_dtypes=[ds_T.votemper.dtype])

densities = np.arange(27.7,28,0.01)

volume = ds_T.e1t*ds_T.e2t*ds_T.e3t
TV = hist(
    ds_T.vosigmantr,
    bins=[densities],
    dim=['x','y','deptht'],
    weights=(volume*ds_T.votemper))
V = hist(
    ds_T.vosigmantr,
    bins=[densities],
    dim=['x','y','deptht'],
    weights=volume)
T = TV/V

T.to_dataset().to_netcdf('data/processed/orca025_NA-z50_votemper-by-vosigmantr.nc', mode='w')