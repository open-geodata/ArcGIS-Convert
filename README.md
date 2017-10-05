# ArcGIS-Convert
Elaborado para converter arquivos do geodatabase para diversos outros formatos comumente utilizados,
com a correção dos datum para WGS84, sendo esse o padrão frequentemente utilizado.

## Para que serve?
O *script* converte todos os *feature class* existentes em um dado *geodatabase* para *shapefiles*, que serão armazenados em uma pasta *../shp*.

Também ocorre a projeção de todos os *feature class* existentes no mesmo *geodatabase* para o datum WGS84, com Sistema de Projeção Geográfica (EPGS:4326), em um *geodatabase* localizado na pasta *../geo* e ainda na pasta *../shp/WGS84*. Os *feature class* poderão estar em diferentes *datum* e sistema de coordenadas, a saber:
* GCS_South_American_1969
* GCS_Corrego_Alegre
* GCS_SIRGAS_2000
* SAD_1969_UTM_Zone_21S
* SAD_1969_UTM_Zone_22S
* SAD_1969_UTM_Zone_23S
* SAD_1969_UTM_Zone_24S
* SAD_1969_UTM_Zone_25S
* Corrego_Alegre_UTM_Zone_21S
* Corrego_Alegre_UTM_Zone_22S
* Corrego_Alegre_UTM_Zone_23S
* Corrego_Alegre_UTM_Zone_24S
* Corrego_Alegre_UTM_Zone_25S
* SIRGAS_2000_UTM_Zone_21S
* SIRGAS_2000_UTM_Zone_22S
* SIRGAS_2000_UTM_Zone_23S
* SIRGAS_2000_UTM_Zone_24S
* SIRGAS_2000_UTM_Zone_25S

Os *feature class* também são exportados em formato *.kml*, localizados na pasta *../kml*, em formato *.gpx*, localizados na pasta *../gpx* e, por fim, em formato *.lyr* (para ser usado no ArcGIS), na pasta *../lyr*.

Por fim, o *script* exporta a tabela de atributos em formato *.xls*, compatível com o *software **Microsoft Excel***, possibilitando edições e análises posteriores.

## Como "instalar" e usar?
Fazer o *download* (ou cópia) do arquivo [Geodatabase2others.py](Scripts/Geodatabase2others.py) e executar.
Ajustar apenas o caminho para o *geodatabase*.

## Pré-requisitos
- ArcGIS instalado;
- *Script* [Transformation.py](https://github.com/michelmetran/ArcGIS-Transformation) aplicado;
- *Script* [FeaturesToGPX.py](Scripts/FeaturesToGPX.py) disponível originalmente no [projeto](https://github.com/arcpy/sample-gp-tools/tree/master/FeaturesToGPX);

Testado com as versões 10.5.

## Autor
* **Michel Metran**, veja [outros projetos](https://github.com/michelmetran).

Veja também a lista de [colaboradores](https://github.com/michelmetran/ArcGIS-Convert/settings/collaboration) que auxiliaram nesse projeto.

## Licença
Esse projeto é licenciado sob a 'MIT License'.
Veja o arquivo [LICENSE](LICENSE) para detalhes.