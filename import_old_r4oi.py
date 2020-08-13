#! /usr/bin/env python
#   Gter Copyleft 2020
#   Roberto Marzocchi
#   script  per importare i vecchi dati erroneamente caricati singolarmente in un unico coverage (uno per ogni variabile)


# library added by GTER
import os, sys, shutil, re, glob
import time
import urllib.request
import urllib.parse

from datetime import datetime, timedelta

epsg='32632'
spazio = "\n**************************************"
path= os.path.dirname(os.path.realpath(__file__))
print('Path is ',path)

#print('sys.argv[0] =', sys.argv[0])             
#path = os.path.dirname(sys.argv[0])        
#print('path =', path)
#print('full path =', os.path.abspath(path)) 

#exit()
#start from 2020-05-18 
date_str1='2020051812'
date_dt1 = datetime.strptime(date_str1, '%Y%m%d%H')
date_str2='2020081307'
date_dt2 = datetime.strptime(date_str2, '%Y%m%d%H')


ar = ['pdry_idi', 'prec_ana', 'pwet_idi', 'rh_ana', 'rh_hdx', 'rh_idi', 't2m_ana', 't2m_bkg', 't2m_idi']
for variable in ar:
    #print(variable)
    date_str=date_str1
    date_dt = datetime.strptime(date_str, '%Y%m%d%H')
    #now = datetime.now()
    while date_dt <= (date_dt2) :
        try: 
            print(spazio)
            file='{0}_32632_{1}.tiff'.format(variable,date_str)
            comando="curl \"http://localhost:8080/rasdaman/ows?&SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage&COVERAGEID={0}_{1}&FORMAT=image/tiff\" > {2}".format(variable,date_str, file)
            #print(comando) 
            return0=os.system(comando)
            #print(return0)  
            print('Creo il json per importare il file')
            text = '{{"config": {{ "service_url": "http://localhost:8080/rasdaman/ows", ' \
                '"tmp_directory": "/tmp/", "crs_resolver": "http://localhost:8080/def/", ' \
                '"default_crs": "http://localhost:8080/def/crs/EPSG/0/{2}",  ' \
                '"mock": false, "automated": true, "retry": true, "retries": 5, ' \
                '"track_files": true }},  ' \
                '"input": {{ "coverage_id": "{0}", "paths": [ "{1}/{4}" ] }}, ' \
                '"recipe": {{ "name": "time_series_irregular", "options": {{ "wms_import": false, ' \
                '"time_parameter": {{ "filename": {{ "regex": "(.*)_(.*)_(.*)", "group": "3" }}, '\
                '"datetime_format": "YYYYMMDDHH"}}, "time_crs": "http://localhost:8080/def/crs/OGC/0/AnsiDate", '\
                '"tiling": "ALIGNED [0:1023, 0:1023] TILE SIZE 4194304" }}  }} }}'.format(variable, path, epsg, date_str, file)
            #print(text)
            print(spazio)
            #print('Importo il file')
            nomefile = "{}.json".format(variable)
            out_file = open(nomefile, "w")
            out_file.write(text)
            out_file.close()
            comando_import = '/opt/rasdaman/bin/wcst_import.sh %s' % nomefile
            return1=os.system(comando_import)
            print(return1)                                              
        except:
            print ('No data to download for {0}'.format(date_str))
        date_dt = date_dt + timedelta(hours=1)
        date_str = date_dt.strftime('%Y%m%d%H')
        #print(date_str)



#exit()