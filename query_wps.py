#! /usr/bin/env python
#   Gter Copyleft 2020
#   Roberto Marzocchi
#   script  perlanciare query wps
# es. python3 query_wps.py localhost:8080 'for $c in (fwi) return encode($c[X(1515230),Y(5037450),ansi("2020-08-01":"2020-08-31")], "application/json")'


# library added by GTER
import os, sys, shutil, re, glob
import time
import urllib.request
import urllib.parse


print("This is the name of the script: ", sys.argv[0])

host=sys.argv[1]


url_WCPS='http://{}/rasdaman/ows?service=WCS&version=2.0.1&REQUEST=ProcessCoverage&QUERY='.format(host)

#query='for $c in (fwi) return encode($c[X(1515230),Y(5037450),ansi("2020-08-01":"2020-08-31")], "application/json")'
query=sys.argv[2]

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