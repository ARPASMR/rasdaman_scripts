#! /usr/bin/env python
#   Gter Copyleft 2020
#   Roberto Marzocchi
#   script  per rimuovere i vecchi dati erroneamente caricati singolarmente in un unico coverage (uno per ogni variabile dal 18 maggio al 13 agosto)


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
date_str1='201812'
date_dt1 = datetime.strptime(date_str1, '%Y%m')
date_str2='202008'
date_dt2 = datetime.strptime(date_str2, '%Y%m')


ar =['bui', 'dc', 'dmc', 'ffmc', 'fwi', 'isi']
for variable in ar:
    #print(variable)
    date_str=date_str1
    date_dt = datetime.strptime(date_str, '%Y%m')
    #now = datetime.now()
    while date_dt <= (date_dt2) :
        try: 
            print(spazio)
            file0='{0}_32632_{1}'.format(variable,date_str)
            file='{0}.tiff'.format(file0)
            comando="curl \"http://localhost:8080/rasdaman/ows?&SERVICE=WCS&VERSION=2.0.1&REQUEST=DeleteCoverage&COVERAGEID={0}_{1}\"".format(variable,date_str)
            print(comando) 
            return0=os.system(comando)                                          
        except:
            print ('No data to remove for {0}'.format(date_str))
        date_dt = date_dt + timedelta(days=31)
        date_str = date_dt.strftime('%Y%m')
        #print(date_str)



#exit()