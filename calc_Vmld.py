import numpy as np
import xarray as xr

rootdir = '/home/ocean_shared_data1/DRAKKAR/ORCA025.L75-GJM189-S/'
config = 'ORCA025.L75-GJM189'
filepath = rootdir+'*/'+config+'_y*m0[234]d*_gridT.nc'
filepath_hgrid = rootdir+'GRID/'+config+'_mesh_hgr.nc'
filepath_zgrid = rootdir+'GRID/'+config+'_mesh_zgr.nc'
lonrange = [-100,30]
latrange = [45,80]

# Load grid
ds_grid = xr.merge([xr.open_dataset(filepath_hgrid),xr.open_dataset(filepath_zgrid)],compat='override').squeeze()
# Change name of depth variable and drop time_counter
ds_grid = ds_grid.rename({'z':'deptht'}).assign_coords({'deptht':ds_grid.gdept_0.values}).drop('time_counter')
ds_grid = ds_grid

# Load data files
ds_T = xr.open_mfdataset(filepath,combine='by_coords',parallel=True)
# Merge with grid
ds_T = ds_T.update(ds_grid);

# Isolate North Atlantic
NAcondition = (ds_T.nav_lon>=lonrange[0]) & (ds_T.nav_lon<=lonrange[1]) & (ds_T.nav_lat>=latrange[0]) & (ds_T.nav_lat<=latrange[1])
ds_T = ds_T.where(NAcondition,drop=True)

Vmld = (ds_T.somxl010*ds_T.e1t*ds_T.e2t).sum(['x','y'])
Vmld.name='Vmld'

Vmld.to_dataset().to_netcdf('data/processed/eulerian/orca025_NA_Vmld.nc')