import csv
import pygal
import math


"""
codeinfo = {
      "codefile": "code1.csv", # Name of the country code CSV file
      "separator": ",",                    # Separator character in CSV file
      "quote": '"',                        # Quote character in CSV file
      "plot_codes": "ISO3166-1-Alpha-2",   # Plot code field name
      "data_codes": "ISO3166-1-Alpha-3"    # GDP data code field name
}

"""
codeinfo = {
      "codefile": "code1_1.csv", # Name of the country code CSV file
      "separator": ",",                    # Separator character in CSV file
      "quote": '"',                        # Quote character in CSV file
      "plot_codes": "Code4",   # Plot code field name
      "data_codes": "Code3"    # GDP data code field name
}
"""
codeinfo = {
      "codefile": "isp_country_codes.csv", # Name of the country code CSV file
      "separator": ",",                    # Separator character in CSV file
      "quote": '"',                        # Quote character in CSV file
      "plot_codes": "ISO3166-1-Alpha-2",   # Plot code field name
      "data_codes": "ISO3166-1-Alpha-3"    # GDP data code field name
}
"""

gdpinfo = {
      "gdpfile": "gdptable3.csv",
      "separator": ";",
      "quote": "'",
      "min_year": 20010,
      "max_year": 20017,
      "country_name": "ID",
      "country_code": "CC"
}


def read_csv_as_nested_dict(filename, plot_codes, data_codes, separator, quote):
  """
  Inputs:
    filename  - Name of CSV file
    plot_codes  - Field to use as key for rows
    data_codes -  Field to use as values for rows
    separator - Character that separates fields
    quote     - Character used to optionally quote fields
  Output:
    Returns a dictionary of dictionaries where the outer dictionary
    maps the value in the key_field to the corresponding row in the
    CSV file.  The inner dictionaries map the field names to the
    field values for that row.
  """

  table = {}

  with open(filename, 'rt', newline='') as csv_file:
      csv_reader = csv.DictReader(csv_file, delimiter=separator,
                                  quotechar=quote)
      for row in csv_reader:
          # print(row)
          x= row[plot_codes]
          #y=x.lower()
          table[x] = row[data_codes]
          #rowid = row[keyfield]
          #table[rowid] = row
  return table


def build_country_code_converter(codeinfo):
  """
  Inputs:
    codeinfo      - A country code information dictionary

  Output:
    A dictionary whose keys are plot country codes and values
    are world bank country codes, where the code fields in the
    code file are specified in codeinfo.
  """
  code_dat = read_csv_as_nested_dict(codeinfo["codefile"], codeinfo["plot_codes"], codeinfo['data_codes'], codeinfo["separator"],codeinfo["quote"])
  return code_dat


def reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries):
  """
  Inputs:
    codeinfo       - A country code information dictionary
    plot_countries - Dictionary whose keys are plot library country codes
                     and values are the corresponding country name
    gdp_countries  - Dictionary whose keys are country codes used in GDP data

  Output:
    A tuple containing a dictionary and a set.  The dictionary maps
    country codes from plot_countries to country codes from
    gdp_countries.  The set contains the country codes from
    plot_countries that did not have a country with a corresponding
    code in gdp_countries.

    Note that all codes should be compared in a case-insensitive
    way.  However, the returned dictionary and set should include
    the codes with the exact same case as they have in
    plot_countries and gdp_countries.
  """
  dict_codes = {}
  dict_codes3 = {}
  set_no_countries_gdp_data = set()
  dict_codes = build_country_code_converter(codeinfo)
  
      
      
  for key in plot_countries:
      key_gdp = dict_codes[key.upper()]
      #plot_country = plot_countries[key]
       
      #if plot_country.lower() != gdp_country.lower():
      
      #code_gdp = dict_codes[key]
      #if plot_countries[key] != gdp_countries[code_gdp]['Country Name']:
      #tmp_plot = plot_countries[key.lower()]
      #tmp_gdp = gdp_countries[key.lower()]['Country Name']
      #Need to check the below code again
      #if tmp_plot.lower() != tmp_gdp.lower():
      #    set_no_countries_gdp_data.add(key)
      #else:
      #    if gdp_countries[key_gdp]:
      #        dict_codes3[key] = key_gdp
      #if gdp_countries[key_gdp]:
      if key_gdp in gdp_countries:
          #gdp_country = gdp_countries[key_gdp]['Country Name']

          dict_codes3[key] = key_gdp
      else:
          set_no_countries_gdp_data.add(key)
  return (dict_codes3, set_no_countries_gdp_data)

def read_csv_as_nested_dict_gdp(filename, keyfield, separator, quote):
  """
  Inputs:
    filename  - Name of CSV file
    keyfield  - Field to use as key for rows
    separator - Character that separates fields
    quote     - Character used to optionally quote fields
  Output:
    Returns a dictionary of dictionaries where the outer dictionary
    maps the value in the key_field to the corresponding row in the
    CSV file.  The inner dictionaries map the field names to the
    field values for that row.
  """

  table1 = {}

  with open(filename, 'rt', newline='') as csv_file:
      csv_reader = csv.DictReader(csv_file, delimiter=separator,
                                  quotechar=quote)
      for row in csv_reader:
          # print(row)
          rowid = row[keyfield]
          #print (rowid)
          rowid_low = rowid.lower()
          #print (rowid, rowid_low)
          table1[rowid_low] = row
          #print (table1)
  return table1


def build_plot_values(gdpinfo, gdpdata, year):
  """
  Inputs:
    gdpinfo - GDP data information dictionary
    gdpdata - A single country's GDP stored in a dictionary whose
              keys are strings indicating a year and whose values
              are strings indicating the country's corresponding GDP
              for that year.
  Output:
    Returns a list of tuples of the form (year, GDP) for the years
    between "min_year" and "max_year", inclusive, from gdpinfo that
    exist in gdpdata.  The year will be an integer and the GDP will
    be a float.
  """
  #table = []
  gdpdat_v2 = {}
  gdpdata_1 = {}
  gdpdata_1 = dict(gdpdata)
  #print ("gbatra2")
  #print (gdpdata)
  #print 
  #print (gdpdata_1)
  #for k,v in gdpdata_1.items():
  #    print (k,v)
  if year in gdpdata_1.keys():
      #print ("gbatra3")
      if gdpdata_1[year]:
          gdpdat_v2[year] = math.log10(float(gdpdata_1[year]))
          
          return gdpdat_v2[year]
      else:
          return -1
  else:
      return -1
  

def build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year):
  """
  Inputs:
    gdpinfo        - A GDP information dictionary
    codeinfo       - A country code information dictionary
    plot_countries - Dictionary mapping plot library country codes to country names
    year           - String year for which to create GDP mapping

  Output:
    A tuple containing a dictionary and two sets.  The dictionary
    maps country codes from plot_countries to the log (base 10) of
    the GDP value for that country in the specified year.  The first
    set contains the country codes from plot_countries that were not
    found in the GDP data file.  The second set contains the country
    codes from plot_countries that were found in the GDP data file, but
    have no GDP data for the specified year.
  """
  """
  build_map_dict_by_code({'country_name': 'Country Name', 'gdpfile': 'gdptable1.csv', 'separator': ',', 'min_year': 2000, 'quote': '"', 'max_year': 2005, 'country_code': 'Code'},
                     {'data_codes': 'Cd3', 'codefile': 'code2.csv', 'quote': "'", 'plot_codes': 'Cd2', 'separator': ','},
                     {'C3': 'c3', 'C1': 'c1', 'C5': 'c5', 'C4': 'c4', 'C2': 'c2'},
                     '2001') expected ({'C3': 1.041392685158225, 'C1': 0.30102999566398114}, {'C4', 'C2', 'C5'}, set()) but received ({}, {'C3', 'C1', 'C4', 'C2', 'C5'}, set()) (Exception: Invalid Keys) Expected dictionary {'C3': 1.041392685158225, 'C1': 0.30102999566398114} has a different number of keys than received dictionary {}
  """
  table = {}
  non_set1 = set()
  non_set2 = set()
  
  gdp_dat = read_csv_as_nested_dict_gdp(gdpinfo["gdpfile"], gdpinfo["country_code"], gdpinfo["separator"],gdpinfo["quote"])
  code_dat = build_country_code_converter(codeinfo)
  #print (code_dat)
  #print (gdp_dat)
  
  for k, v in plot_countries.items():
      code_plot = plot_countries[k]
      if code_plot in code_dat.keys():
          key_codeinfo = code_dat[code_plot]
          #print (code_plot, key_codeinfo)
          #print (gdp_dat.keys())
          #print (k,v, key_codeinfo)
          #Case3
          if key_codeinfo.lower() in gdp_dat.keys():
              #print ("gbatra4")
              key_tmp = key_codeinfo.lower()
          #Case2
          #if key_codeinfo.upper() in gdp_dat.keys():
          #Case1
          #if key_codeinfo in gdp_dat.keys():
              #print (gdp_dat.keys())
              value = build_plot_values(gdpinfo, gdp_dat[key_tmp], year)
              #Case2
              #value = build_plot_values(gdpinfo, gdp_dat[key_codeinfo.upper()], year)
              #Case1
              #value = build_plot_values(gdpinfo, gdp_dat[key_codeinfo], year)
              #print (value)
          
              
              if value == -1 :
                  non_set1.add(k)
              else:
                  table[k] = value
          else:
              non_set2.add(k)
      else:
          non_set2.add(k)
  #print (table, non_set2, non_set1)      
  return (table, non_set2, non_set1)
"""
plot_countries = {'C3': 'c3', 'C1': 'c1', 'C5': 'c5', 'C4': 'c4', 'C2': 'c2'}
build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, '20012')
"""
  
