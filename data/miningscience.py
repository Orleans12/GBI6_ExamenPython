import Bio 
from Bio import Entrez
import re
import pandas as pd
import csv
import itertools
import numpy as np
def download_pubmed(keyword: str): 
    """Docstring download_pubmed, se realiza el minado de las IDs de los artículos
    con  una keyword que se define"""
    Entrez.email = "vicente.quezada@est.ikiam.edu.ec"
    main = Entrez.esearch(db="pubmed",
                        retmax=1000000,
                        retmode='xml',
                        term=keyword)
    data = Entrez.read(main)                    
    main.close()
    return data
    
     

def mining_pubs(tipo: str) ->pd.DataFrame:
    """Docstring mining_pubs, en este minado se utiliza otros parámetros de busqueda como "DP" "AU" "AD", se
    especifica que devuelve cada parámetro a continuación:
    DP: Devuelve un dataframe con el PMDI y DP_year.
    AU: Devuelve un dataframe con el PMDI y num_auth.
    AD: Devuelve un dataframe con el country y num_auth
    """
    Ep=download_pubmed('Ecuador genomics')
    
    ID=info['IdList']
    liste=','.join(ID)
    Entrez.email = "vicente.quezada@est.ikiam.edu.ec"
    hand = Entrez.efetch(db="pubmed",
                        rettype='medline',
                        retmode='text',
                        id=liste)
    datos = hand.read()           
    
    if (tipo == "AD"):
        
        z_codes = re.findall(r'PMID-.(.+)', datos) 
        z_codes1 = re.findall(r'DP  -.(\d+)', datos) 
        z_codes1 = [int(i) for i in zipcodes1]  
        z_alldata = list(zip(z_codes,z_codes1))
        n_colum = ['PMID','DP_year']
    else:
        if(tipo == "AU"): 
            z_codes = re.findall(r'PMID-.(.+)|(AU)  -|', datos) 
            n_colum = ['PMID','num_auth']
            
        elif(tipo == "AD"):
            z_codes = re.findall(r'PL  -.(.+)|(AU)  -|', datos)
            n_colum = ['country','num_auth']
            
        z_alldata = list()
        for x in z_codes:
            if(x[0]!=''):
                z_alldata.append((x[0],''))
            elif(x[1]!=''):
                z_alldata.append(('',x[1]))

        z_codes = z_alldata       
        lista1 = list()
        lista2 = list()
        vf = 0
        for y in z_codes:
            if(y[0] !=''):
                p_o = y[0]
                lista1.append(y[0])
                if(vf != 0):
                    lista2.append(vf)
                    vf = 0
            else:
                vf = vf+1          
        z_alldata = list(zip(lista1,lista2))
        
    hand.close()
    Ep = pd.DataFrame(z_alldata, columns=n_colum) 
    return info
     

    