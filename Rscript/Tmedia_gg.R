#Script per l'elaborazione della temperatura media giornaliera a partire da dati orari "scaricati" da Rasdaman #
#Esecutore script: MZ                                                                                          #
#La procedura è¨ pensata per "girare" ogni gg con elaborazione del giorno precedente,                          #
#Nel caso l'utente voglia scegliere il giorno è necessario scommentare le prime righe dopo la definizione      #
#delle librerie.                                                                                               #         
################################################################################################################
library(raster)
library(tmap)
library(RColorBrewer)
library(rgdal)
library(lubridate)
library(anytime)
library(RCurl)

#Scommentare se si vuole scegliere autonomamente il giorno
#start_date <- "20201026" 
#start_date <- ymd(start_date) + hours(1)

#Stringa di base per la composizione del link da elaborare
base_string <- "http://10.10.0.28:8081/rasdaman/ows?&SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage&COVERAGEID=t2m_ana&SUBSET=ansi(%22"

#Definizione temporale del periodo da elaborare (procedura in automatico), da commentare nel caso di scelta giorno dell'utente
start_date <- today("UTC") - days(1) + hours(1)
end_date <- start_date + hours(23)

#Sequenza di date da elaborare
vec_date <- seq(start_date,end_date, by = '1 hour')
print(paste(vec_date))

#Isolo il tempo e il giorno dalla stringa data e ora
time <- strftime(vec_date,format="%H:%M:%S",tz = "UTC")
day <- strftime(vec_date[1], format="%d-%m")

#Assengno il primo raster alla mia variabile che poi andrà a sommare gli altri nel ciclo - controllo di esistenza del raster
r_link <- paste(base_string,date(vec_date[1]),"T",time[1],".000Z%22)&FORMAT=image/tiff",sep = "")
print(paste("inizio:",r_link))
if (url.exists(r_link)){ 
  rstr_finale <- raster(r_link)
} else {
  print("Errore: non accedo al raster")
}

#Ciclo sommo le ore
for (i in 1:length(vec_date)){
  r_link <- paste(base_string,date(vec_date[i]),"T",time[i],".000Z%22)&FORMAT=image/tiff",sep = "")
  print(paste(r_link))
  
  if(url.exists(r_link)){ 
    rstr_finale = rstr_finale + raster(r_link)
  } else {
    print("Errore: non accedo al raster")
  }
}

#Calcolo della temperatura media
rstr_finale <- rstr_finale / 24

#L'istruzione di seguito è commentata perchè permette di scrivere il raster giornaliero per uso locale
#Scrivo il raster giornaliero
#writeRaster(rstr_finale, filename = paste("C:\\Users\\mazanetti\\Documents\\Rasdaman\\dati\\luglio_tif\\t2m_ana_",date(vec_date[1]),".tif",sep = ""), format = "GTiff", overwrite = TRUE)

###################################################  Esempio semplice di Elaborazione grafica del raster (tmap library) ######################################
#Creazione delle isolinee da aggiungere al grafico
rc <- rasterToContour(rstr_finale)

#Assegno il sistema di riferimento Gauss-Boaga Monte Mario al raster
proj4string(rstr_finale) <- CRS("+init=epsg:3003")

#Creo il grafico. La documentazione della libreria è disponibile qui: https://cran.r-project.org/web/packages/tmap/tmap.pdf
tm_shape(rstr_finale) + tm_raster(style= "cont", palette = "-RdYlBu", title = paste("Tmedia del ",day,"\n (°C)"), interpolate = TRUE) + 
   tm_shape(rc) + tm_lines(col = "black", text = "level", breaks = rc$level, labels = as.character(rc$level)) + 
      tm_text("level", col = "white", size = 1.0) + tm_legend(outside = TRUE)

#END SCRIPT
