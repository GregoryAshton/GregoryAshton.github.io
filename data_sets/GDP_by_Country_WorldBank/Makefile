DOWNLOAD = data.zip
OUT = ny.gdp.mktp.cd_Indicator_en_csv_v2.csv
.PHONY: download clean

download:
	rm -f ${DOWNLOAD}
	wget http://api.worldbank.org/v2/en/indicator/ny.gdp.mktp.cd?downloadformat=csv -O data.zip
	unzip $(DOWNLOAD)
	rm -f ${DOWNLOAD} Metadata*csv *xml

