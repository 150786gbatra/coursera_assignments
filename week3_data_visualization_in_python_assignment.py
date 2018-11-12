
import csv
import pygal
import math



gdpinfo = {
        "gdpfile": "gdptable1.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 2000,
        "max_year": 2005,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

def read_csv_as_nested_dict(filename, keyfield, separator, quote):
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

    table = {}

    with open(filename, 'rt', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=separator,
                                    quotechar=quote)
        for row in csv_reader:
            # print(row)
            rowid = row[keyfield]
            table[rowid] = row
    return table


def reconcile_countries_by_name(plot_countries, gdp_countries):
    """
    Inputs:
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country names used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country names from
      gdp_countries The set contains the country codes from
      plot_countries that were not found in gdp_countries.
    """
    out_dict = {}
    non_gdp_set = set()
    for key in plot_countries:
        if plot_countries[key] in gdp_countries.keys():
            out_dict[key] = plot_countries[key]
    
        else:
            non_gdp_set.add(key)
            
    return (out_dict, non_gdp_set)

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
    if year in gdpdata.keys():
        if gdpdata[year]:
            gdpdat_v2[year] = math.log10(float(gdpdata[year]))
            return gdpdat_v2[year]
        else:
            return -1
    else:
        return -1
        
#    """
#    for k, v in gdpdata.items():
#        try:
#            gdpdat_v2[int(k)] = math.log10(float(v))
#        except ValueError:
#            pass
#    """
#    #min_max = [year for year in range(gdpinfo['min_year'], gdpinfo['max_year'] + 1)]
#
#    """
#    #for key in min_max:
#    if year in gdpdat_v2.keys():
#            #table.append((key, gdpdat_v2[key]))
#        return gdpdat_v2[year]
#    else:
#        return None
#    """

def build_map_dict_by_name(gdpinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for

    Output: 
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """

    #gdpdat_v2 = {}
    table = {}
    non_set1 = set()
    non_set2 = set()
    gdp_dat = read_csv_as_nested_dict(gdpinfo["gdpfile"], gdpinfo["country_name"], gdpinfo["separator"],gdpinfo["quote"])
    print (gdp_dat)

    
    for k, v in plot_countries.items():
        if v in gdp_dat.keys():
            value = build_plot_values(gdpinfo, gdp_dat[v], year)
            if value == -1 :
                non_set1.add(k)
            else:
                table[k] = value
        else:
            non_set2.add(k)
                
        
    return (table, non_set2, non_set1)
        

def render_world_map(gdpinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for
      map_file       - Name of output file to create

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data for the given year and
      writes it to a file named by map_file.
    """
