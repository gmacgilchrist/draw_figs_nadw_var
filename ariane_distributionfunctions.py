import numpy as np
import xarray as xr
from xhistogram.xarray import histogram as hist

def ariane_D1(var1,bins,dim=None,weights=None,subset=False,conditional=None,subsetname=None,save=False):
    '''Description here.'''
    
    # Apply conditional statement
    if subset:
        var1 = var1.where(conditional,drop=True)
        weights = weights.where(conditional,drop=True)
        
    D1 = hist(
        var1,
        bins=bins,
        dim=dim,
        weights=weights
            )
    
    if save:
        if weights.name==None:
            error('Weights have no name. Must name for the purpose of saving.')
        if subset:
            filename = 'D1_weights-'+weights.name+'_bins-'+var1.name+'_subset-'+subsetname+'.nc'
        else:
            filename = 'D1_weights-'+weights.name+'_bins-'+var1.name+'.nc'
        D1.name = weights.name
        D1.to_dataset().to_netcdf('data/processed/lagrangian/'+filename)
    
    return D1

def ariane_D2(var1,var2,bins,dim=None,weights=None,subset=False,conditional=None,subsetname=None,save=False):
    '''Description here.'''
    
    # Apply conditional statement
    if subset:
        var1 = var1.where(conditional,drop=True)
        var2 = var2.where(conditional,drop=True)
        weights = weights.where(conditional,drop=True)
        
    D2 = hist(
        var1,var2,
        bins=bins,
        dim=dim,
        weights=weights
            )
    
    if save:
        if weights.name==None:
            error('Weights have no name. Must name for the purpose of saving.')
        if subset:
            filename = 'D2_weights-'+weights.name+'_bins-'+var1.name+'-'+var2.name+'_subset-'+subsetname+'.nc'
        else:
            filename = 'D2_weights-'+weights.name+'_bins-'+var1.name+'-'+var2.name+'.nc'
        D2.name = weights.name
        D2.to_dataset().to_netcdf('data/processed/lagrangian/'+filename)
    
    return D2

def ariane_D3(var1,var2,var3,bins,dim=None,weights=None,subset=False,conditional=None,subsetname=None,verbose=False,save=True):
    D3_vals = np.zeros(shape=(bins[0].size-1,bins[1].size-1,bins[2].size-1))
    
    for i in range(bins[2].size-1):
        if verbose:
            print(var3.name+' : '+str(bins[2][i])+' to '+str(bins[2][i+1]))
        if subset:
            S = conditional & (var3>bins[2][i]) & (var3<bins[2][i+1])
        else:
            S = (var3>bins[2][i]) & (var3<bins[2][i+1])
            
        D3_vals[:,:,i] = ariane_D2(
            var1,var2,
            bins=[bins[0],bins[1]],
            dim=dim,
            weights=weights,
            subset=subset,
            conditional=S
                ).values
    
    print('end')
    D3 = xr.DataArray(D3_vals,
                    dims=[var1.name+'_bin',var2.name+'_bin',var3.name+'_bin'],
                    coords={var1.name+'_bin':0.5*(bins[0][:-1]+bins[0][1:]),
                            var2.name+'_bin':0.5*(bins[1][:-1]+bins[1][1:]),
                            var3.name+'_bin':0.5*(bins[2][:-1]+bins[2][1:])})
    
    if save:
        #if weights.name==None:
        #    error('Weights have no name. Must name for the purpose of saving.')
        if subset:
            filename = 'D3_weights-'+weights.name+'_bins-'+var1.name+'-'+var2.name+'-'+var3.name+'_subset-'+subsetname+'.nc'
        else:
            filename = 'D3_weights-'+weights.name+'_bins-'+var1.name+'-'+var2.name+'-'+var3.name+'.nc'
        D3.name = weights.name
        D3.to_dataset().to_netcdf('data/processed/lagrangian/'+filename)
        
    return D3

def ariane_D4(var1,var2,var3,var4,bins,dim=None,weights=None,subset=False,conditional=None,subsetname=None,verbose=False,save=True):
    D4_vals = np.zeros(shape=(bins[0].size-1,bins[1].size-1,bins[2].size-1,bins[3].size-1))
    
    for i in range(bins[3].size-1):
        if verbose:
            print(var4.name+' : '+str(bins[3][i])+' to '+str(bins[3][i+1]))
        if subset:
            S = conditional & (var4>bins[3][i]) & (var4<bins[3][i+1])
        else:
            S = (var4>bins[3][i]) & (var4<bins[3][i+1])
            
        D4_vals[:,:,:,i] = ariane_D3(
                var1,var2,var3,
                bins=[bins[0],bins[1],bins[2]],
                dim=dim,
                weights=weights,
                subset=subset,
                conditional=S,
                verbose=False,
                save=False
                    ).values
    print('end')
        
    D4 = xr.DataArray(D4_vals,
                    dims=[var1.name+'_bin',var2.name+'_bin',var3.name+'_bin',var4.name+'_bin'],
                    coords={var1.name+'_bin':0.5*(bins[0][:-1]+bins[0][1:]),
                            var2.name+'_bin':0.5*(bins[1][:-1]+bins[1][1:]),
                            var3.name+'_bin':0.5*(bins[2][:-1]+bins[2][1:]),
                            var4.name+'_bin':0.5*(bins[3][:-1]+bins[3][1:])})
    if save:
        if subset:
            filename = 'D4_weights-'+weights.name+'_bins-'+var1.name+'-'+var2.name+'-'+var3.name+'-'+var4.name+'_subset-'+subsetname+'.nc'
        else:
            filename = 'D4_weights-'+weights.name+'_bins-'+var1.name+'-'+var2.name+'-'+var3.name+'-'+var4.name+'.nc'
        D4.name = weights.name
        D4.to_dataset().to_netcdf('data/processed/lagrangian/'+filename)

    return D4

