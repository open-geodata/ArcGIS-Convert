# ArcGIS-Convert

<br>

Elaborado para converter arquivos do geodatabase para diversos outros formatos comumente utilizados,
com a correção dos datum para WGS84, sendo esse o padrão frequentemente utilizado.

<br>

---

## Para que serve?

O _script_ converte todos os _feature class_ existentes em um dado _geodatabase_ para _shapefiles_, que serão armazenados em uma pasta _../shp_.

Também ocorre a projeção de todos os _feature class_ existentes no mesmo _geodatabase_ para o datum WGS84, com Sistema de Projeção Geográfica (EPGS:4326), em um _geodatabase_ localizado na pasta _../geo_ e ainda na pasta _../shp/WGS84_. Os _feature class_ poderão estar em diferentes _datum_ e sistema de coordenadas, a saber:

- GCS_South_American_1969
- GCS_Corrego_Alegre
- GCS_SIRGAS_2000
- SAD_1969_UTM_Zone_21S
- SAD_1969_UTM_Zone_22S
- SAD_1969_UTM_Zone_23S
- SAD_1969_UTM_Zone_24S
- SAD_1969_UTM_Zone_25S
- Corrego_Alegre_UTM_Zone_21S
- Corrego_Alegre_UTM_Zone_22S
- Corrego_Alegre_UTM_Zone_23S
- Corrego_Alegre_UTM_Zone_24S
- Corrego_Alegre_UTM_Zone_25S
- SIRGAS_2000_UTM_Zone_21S
- SIRGAS_2000_UTM_Zone_22S
- SIRGAS_2000_UTM_Zone_23S
- SIRGAS_2000_UTM_Zone_24S
- SIRGAS_2000_UTM_Zone_25S

<br>

Os _feature class_ também são exportados em formato _.kml_, localizados na pasta _../kml_, em formato _.gpx_, localizados na pasta _../gpx_ e, por fim, em formato _.lyr_ (para ser usado no ArcGIS), na pasta _../lyr_.

Por fim, o _script_ exporta a tabela de atributos em formato _.xls_, compatível com o \*software **Microsoft Excel\***, possibilitando edições e análises posteriores.

<br>

---

## Como "instalar" e usar?

Fazer o _download_ (ou cópia) do arquivo [Geodatabase2others.py](Scripts/Geodatabase2others.py) e executar.
Ajustar apenas o caminho para o _geodatabase_.

<br>

---

## Pré-requisitos

- ArcGIS instalado;
- _Script_ [Transformation.py](https://github.com/michelmetran/ArcGIS-Transformation) aplicado;
- _Script_ [FeaturesToGPX.py](Scripts/FeaturesToGPX.py) disponível originalmente no [projeto](https://github.com/arcpy/sample-gp-tools/tree/master/FeaturesToGPX);

Testado com as versões 10.5.

<br>

---

## Autor

- **Michel Metran**, veja [outros projetos](https://github.com/michelmetran).

Veja também a lista de [colaboradores](https://github.com/michelmetran/ArcGIS-Convert/settings/collaboration) que auxiliaram nesse projeto.

<br>

---

## Licença

Esse projeto é licenciado sob a 'MIT License'.
Veja o arquivo [LICENSE](LICENSE) para detalhes.
