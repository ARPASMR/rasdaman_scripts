#! /usr/bin/env python
#   Gter Copyleft 2020
#   Roberto Marzocchi
#   script  per rimuovere i vecchi dati erroneamente caricati singolarmente in un unico coverage (uno per ogni variabile dal 18 maggio al 13 agosto)


# library added by GTER
import os, sys, shutil, re, glob
import time
import urllib.request
import urllib.parse


url_WCPS='http://localhost:8080/rasdaman/ows?service=WCS&version=2.0.1&REQUEST=ProcessCoverage&QUERY='

query='for $c in (fwi) return encode($c[X(1515230),Y(5037450),ansi("2020-08-01":"2020-08-31")], "application/json")'

query_decoded=urllib.parse.quote(query)


comando = "curl \"{}{}\"".format(url_WCPS, query_decoded)

print(comando)
return2=os.system(comando)
print('\n')
#print(return2)
if return2==0:
    print('OK')
else:
    print('ERRORE SU QUERY')