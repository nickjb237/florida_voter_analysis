# -*- coding: utf-8 -*-
"""
This program will take any Miami Dade county zip code and estimate each of the voters'
ethnicity.

Based on findings provided by Florida Democrats on how common each name, first
and last is, in each Hispanic ethnic group.

Created by: Nick Bauman
Advised by: Dr. Mihhail Berezovski
"""

import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# Reads the files lastnames.csv and firstnames.csv and organizes them properly.
lastnames = pd.read_csv( "lastnames.csv", 
                        dtype = { "Mexican" : str, "%" : float, "PuertoRican" : str, 
                                 "%.1" : float, "Cuban" : str, "%.2" : float, 
                                 "Dominican" : str, "%.3" : float, "CostaRican" : str, 
                                 "%.4" : float, "Guatemalan" : str, "%.5" : float, 
                                 " Honduran" : str, "%.6" : float, "Nicaraguan" : str, 
                                 "%.7" : float, "Panamanian" : str, "%.8" : float, 
                                 "Salvadoran" : str, "%.9" : float, " Argentinean" : str, 
                                 "%.10" : float, "Bolivian" : str, "%.11" : float, 
                                 "Chilean" : str, "%.12" : float, "Colombian" : str, 
                                 "%.13" : float, "Ecuadorian" : str, "%.14" : float, 
                                 "Paraguayan" : str, "%.15" : float, "Peruvian" : str, 
                                 "%.16" : float, "Uruguayan" : str, "%.17" : float, 
                                 "Venezuelan" : str, "%.18" : float },
                        delimiter="," )

firstnames = pd.read_csv( "firstnames.csv", 
                        dtype = { "Mexican" : str, "%" : float, "PuertoRican" : str, 
                                 "%.1" : float, "Cuban" : str, "%.2" : float, 
                                 "Dominican" : str, "%.3" : float, "CostaRican" : str, 
                                 "%.4" : float, "Guatemalan" : str, "%.5" : float, 
                                 " Honduran" : str, "%.6" : float, "Nicaraguan" : str, 
                                 "%.7" : float, "Panamanian" : str, "%.8" : float, 
                                 "Salvadoran" : str, "%.9" : float, " Argentinean" : str, 
                                 "%.10" : float, "Bolivian" : str, "%.11" : float, 
                                 "Chilean" : str, "%.12" : float, "Colombian" : str, 
                                 "%.13" : float, "Ecuadorian" : str, "%.14" : float, 
                                 "Paraguayan" : str, "%.15" : float, "Peruvian" : str, 
                                 "%.16" : float, "Uruguayan" : str, "%.17" : float, 
                                 "Venezuelan" : str, "%.18" : float },
                        delimiter="," )


# List of all these for iteration purposes.
d_s_eth =   {   1:"s_mex", 2:"s_prc", 3:"s_cbn", 4:"s_dom", 5:"s_csr", 6:"s_gua",
                7:"s_hon", 8:"s_nic", 9:"s_pan", 10:"s_svd", 11:"s_arg", 12:"s_bol",
                13:"s_che", 14:"s_col", 15:"s_ecu", 16:"s_par", 17:"s_per", 
                18:"s_uru", 19:"s_vez" }
d_l_eth =   {   1: "l_mex", 2:"l_prc", 3:"l_cbn", 4:"l_dom", 5:"l_csr", 6:"l_gua",
                7: "l_hon", 8:"l_nic", 9:"l_pan", 10:"l_svd", 11:"l_arg", 12:"l_bol",
                13:"l_che", 14:"l_col", 15:"l_ecu", 16:"l_par", 17:"l_per",
                18:"l_uru", 19:"l_vez" }
eths = {    1:"Mexican", 2:"PuertoRican", 3:"Cuban", 4:"Dominican", 5:"Costa Rican",
            6:"Guatemalan", 7:"Honduran", 8:"Nicaraguan", 9:"Panamanian", 10:"Salvadoran",
            11:" Argentinean", 12:"Bolivian", 13:"Chilean", 14:"Colombian", 15:"Ecuadorian",
            16:"Paraguayan", 17:"Peruvian", 18:"Uruguayan", 19:"Venezuelan" }
df_pct_cols = {    1:"%", 2:"%.1", 3:"%.2", 4:"%.3", 5:"%.4", 6:"%.5", 7:"%.6", 
                       8:"%.7", 9:"%.8", 10:"%.9", 11:"%.10", 12:"%.11", 13:"%.12", 
                       14:"%.13", 15:"%.14", 16:"%.15", 
                       17:"%.16", 18:"%.17", 19:"%.18" }

# Convert Lastnames, Firstnames, and Middle names to lowercase.
for i in eths.values():
    lastnames[ i ] = lastnames[ i ].str.lower()
    firstnames[ i ] = firstnames[ i ].str.lower()

del i


# column names.
vf_cols = [ "County ID", "Voter ID", "Lastname", "Ignored", "Firstname", "Middle Name",
            "N?", "Street Address", "APT", "City", "Ignored 2", "Zip", "1", "2", "3", "4",
            "5", "6", "7", "Sex", "Ethnicity", "Birthdate", "Something", "Party Aff", 
            "Some other number", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17",
            "18", "19", "20", "21" ]

"""
    # load the voter data file
voterfile = pd.read_table( "dadecounty.txt", engine="python", skiprows=1400000, names=vf_cols, dtype=str )
    # debug: make a nonexistent middle name "x"
voterfile["Middle Name"] = voterfile["Middle Name"].fillna("x")
"""

def find( column, name, df ):
    # Search any voterfile dataframe, for any column, and any string.
    res = df[ df[ column ] == name ]
    return res

# Organize the data based on input.

def load_county( county, string ):
    # Loads a county's voter registration file so this process doesn't repeat itself.
    # Of course, now we have to manually add these files but in the end it saves time.
        # Voter file organization
    filepath = "20200107_VoterDetail/"
    ext = "_20200107.txt"
    
    filename = filepath+county+ext
    
    # column names.
    vf_cols = [ "County ID", "Voter ID", "Lastname", "Ignored", "Firstname", "Middle Name",
            "N?", "Street Address", "APT", "City", "Ignored 2", "Zip", "1", "2", "3", "4",
            "5", "6", "7", "Sex", "Ethnicity", "Birthdate", "Something", "Party Aff", 
            "Some other number", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17",
            "18", "19", "20", "21" ]

    # load the voter data file
    voterfile = pd.read_table( filename, engine="python", names=vf_cols, dtype=str, error_bad_lines = False )
    # debug: make a nonexistent middle name "x"
    voterfile["Middle Name"] = voterfile["Middle Name"].fillna("x")
    voterfile["Ethnicity"] = voterfile["Ethnicity"].fillna("0")
    
    # All zips in a county:
    zips_by_county = pd.read_csv( "zip_by_county.csv" )
    zips_in_county = zips_by_county[ zips_by_county.County == string ]
    zips_in_county = zips_in_county[ zips_in_county.Type == "Non-Unique" ]
    l_zipcodes = list( zips_in_county['Code'] )
    return voterfile, l_zipcodes

print("WARNING: Don't forget to load a county's datafile first!")

def retrieve_nonhispanic( in_zip, voterfile ): 
    # convert zipcode to a string.
    y = int( in_zip )
    z = str( y )
    
    # Returns a df of just the voters in a specified zip code.
    z_voters = voterfile[ voterfile['Zip'].str.startswith( z, na = False )]
    #z_voters = voterfile[ re.findall( str(in_zip), voterfile["Zip"] )]
    # Of that zip code, which ones are Hispanic?
    # OMMITTED
    
    # Convert all strings to lowercase only format.
    z_voters[ 'Lastname' ] = z_voters[ 'Lastname' ].str.lower()
    z_voters[ 'Firstname' ] = z_voters[ 'Firstname' ].str.lower()
    
    delete_cols = [ "Voter ID", "Ignored",
            "N?", "Street Address", "APT", "City", "Ignored 2", "Zip", "1", "2", "3", "4",
            "5", "6", "7", "Sex", "Ethnicity", "Something", "Birthdate",
            "Some other number", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17",
            "18", "19", "20", "21" ]
    
    # Clean up the voters table:
    z_voters = z_voters.drop( delete_cols, axis = 1 )
    return z_voters

def retrieve_zipcode_voters( in_zip, voterfile ):
    # convert zipcode to a string.
    y = int( in_zip )
    z = str( y )
    
    # Returns a df of just the voters in a specified zip code.
    z_voters = voterfile[ voterfile['Zip'].str.startswith( z, na = False )]
    #z_voters = voterfile[ re.findall( str(in_zip), voterfile["Zip"] )]
    # Of that zip code, which ones are Hispanic?
    hispanic_voters_zip = z_voters[ z_voters['Ethnicity'].str.startswith('4')]
    
    # Convert all strings to lowercase only format.
    hispanic_voters_zip[ 'Lastname' ] = hispanic_voters_zip[ 'Lastname' ].str.lower()
    hispanic_voters_zip[ 'Firstname' ] = hispanic_voters_zip[ 'Firstname' ].str.lower()
    
    delete_cols = [ "Voter ID", "Ignored",
            "N?", "Street Address", "APT", "City", "Ignored 2", "Zip", "1", "2", "3", "4",
            "5", "6", "7", "Sex", "Ethnicity", "Birthdate", "Something",
            "Some other number", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17",
            "18", "19", "20", "21" ]
    
    # Clean up the voters table:
    hispanic_voters_zip = hispanic_voters_zip.drop( delete_cols, axis = 1 )
    return hispanic_voters_zip

def retrieve_zipdata( in_zip ):
    # Get the population proportions for any zip code.
    zips = pd.read_csv( "flzips.csv", engine="python", index_col="ZIP" )
    df_pct_cols = {    1:"%", 2:"%.1", 3:"%.2", 4:"%.3", 5:"%.4", 6:"%.5", 7:"%.6", 
                   8:"%.7", 9:"%.8", 10:"%.9", 11:"%.10", 12:"%.11", 13:"%.12", 
                   14:"%.13", 15:"%.14", 16:"%.15", 
                   17:"%.16", 18:"%.17", 19:"%.18" }

    # Consults the zip datafile for the needed zip code.
    selected_zip_data = zips.loc[ in_zip ]
    hispanic_proportions = np.array([])
    for i in range(1,20):
        # Append each Hispanic subgroup to a numpy array.
        hispanic_proportions = np.append( hispanic_proportions, selected_zip_data.loc[ df_pct_cols[i]] )
    
    return hispanic_proportions

# The next few functions will consult the names databases and determine the proportion
# that fits the inputted name.
def lastname_proportions( in_lastname ):
    """
    lastname_proportions

    Consults the lastnames.csv and database and returns how common a name is
    in each Hispanic ethnic group.
    """

  # The file lastnames.csv is the model that represent
  # how popular each first and last name are in each Hispanic ethnic group.

  # Iteration constant.
    num_eths = list( range( 1, 20 ))

    l = []
    p_last = np.array( l )

  # The loop separates each of the ethnicities into lists and series' that can be used
  # for further analysis. Pandas strongly encourages against the use of querying multiple
  # columns within a dataframe for some reason..
    
    for i in num_eths:
        d_l_eth[ i ] = list( lastnames[ df_pct_cols[ i ]])
        d_s_eth[ i ] = pd.Series(   data = d_l_eth[ i ], 
                                    index = lastnames[ eths[ i ]],
                                    dtype = float )
        temp_s = pd.Series(     data = d_l_eth[ i ],
                                index = lastnames[ eths[ i ]],
                                dtype = float)
        
      # Return proportion of given name for each ethnic group.
      # First, check to see if it exists in the group.
        if in_lastname in d_s_eth[ i ]:
          # If so, find that proportion and append it to name_proportions
          # Also considers duplicates by using the sum function.
            p = temp_s.loc[ in_lastname ].sum()
            p_last = np.append( p_last, p )
        else:
          # If not, append a 1. Appending 1 prevents every other factor being cancelled
          # by rule of multiplying by zero.
            p_last = np.append( p_last, float(1) )
    return p_last


def firstname_proportions( in_firstname ):
    """
    firstname_proportions

    Consults the firstnames.csv database and returns how common a name is
    in each Hispanic ethnic group.
    """
  # Iteration constant.
    num_eths = list( range( 1, 20 ))

    l = []
    p_first = np.array( l )

  # The loop separates each of the ethnicities into lists and series' that can be used
  # for further analysis. Pandas strongly encourages against the use of querying multiple
  # columns within a dataframe for some reason..
    
    for i in num_eths:
        d_l_eth[ i ] = list( firstnames[ df_pct_cols[ i ]])
        d_s_eth[ i ] = pd.Series(   data = d_l_eth[ i ], 
                                    index = firstnames[ eths[ i ]],
                                    dtype = float )
        temp_s = pd.Series(     data = d_l_eth[ i ],
                                index = firstnames[ eths[ i ]],
                                dtype = float)
        
      # Return proportion of given name for each ethnic group.
      # First, check to see if it exists in the group.
        if in_firstname in d_s_eth[ i ]:
          # If so, find that proportion and append it to name_proportions
          # Also considers duplicates by using the sum function.
            p = temp_s.loc[ in_firstname ].sum()
            p_first = np.append( p_first, p )
        else:
          # If not, append a 1. Appending 1 prevents every other factor being cancelled
          # by rule of multiplying by zero.
            p_first = np.append( p_first, float(1) )
            
    return p_first

def retrieve_name_proportions( last, first, middle ):
    """
    First, middle, last and 2nd last name proportions.
    If 2 last names given, uses functionality for both last names independently
    This is where the inconsistencies of the original datafile are solved.
    """
    # First name methodology is the only easy one :(
    p_first = firstname_proportions( first )
    
    p_last = []
    # Last name methodology.
    if "-" in last:
        delimiter = "-"
        list_last = last.split( delimiter, 1 )
        p_last = ( lastname_proportions( list_last[0] )*0.5 )+( lastname_proportions( list_last[1] )*0.5 )
                
        #else:
        # If it's just a space, make sure it only exists one time. Some last names have
        # multiple words within (such as De La, which should be counted as 2 last names
        # and not 4.) Some last names have a space delimiter rather than a hyphen in this
        # particular datafile.
    elif " " in last:
        # To add: Splitting a last name with one and only one space into two.
        p_last = lastname_proportions( last )
    # Else, just use the 1 last name individually
    else:
        p_last = lastname_proportions( last )
    
    # Middle name proportions are calculated, but whether or not they are used
    # just depends on if it exists. If the initial is given, or anything else, it's
    # just ignored.
    p_middle = firstname_proportions( middle )
    return p_first, p_last, p_middle


def retrieve_name_proportion_in_group( last, first, middle, ethnic_group ):
    """
    An evolved version of retrieve_name_proportions, but the second argument
    specifies a particular Hispanic ethnic group.
    """
    t = retrieve_name_proportions( last, first, middle )
    name_prop_in_group = t.loc[ ethnic_group ]
    return name_prop_in_group

###################################################################################        
def standardize( proportion, all_proportions ):
    """
    General function that standardizes any given ratio.
    Notably used to standardize the probability of a last name being of each
    ethnic group.

    all_proportions has to be a list of floats that contains a list of ratios.
    """
    sum_all = sum( all_proportions )
    if sum_all == 0:
        standard_probability = 0
    else:
        standard_probability = proportion / sum_all
    return standard_probability

def standardize_list( a ):
    """
    An adapted version of standardize that will standardize all values in a list.
    
    Also turns the list into a numpy array even if it isn't one already.
    """
    l = []
    a_strd = np.array( l )
    
    # Determine how long a is.
    length = len( a )
    iterate = list( range( 0, length ))
    for i in iterate:
        temp = standardize( a[ i ], a )
        a_strd = np.append( a_strd, [temp] )
        
    return a_strd

def subscores( in_lastname, in_firstname, in_middle, in_zip ):
    """
    An implementation of Bayes Theorem to calculate the probability that the voter
    is of each sub-ethnicity.
    """
    zipcode = retrieve_zipdata( in_zip )
    
    test_last, test_first, test_middle = retrieve_name_proportions( in_lastname, in_firstname, in_middle )

    # Standardize all hispanic ethnicity proportions for zip.
    strd_zipcode = standardize_list( zipcode )

    # Standardize all probabilities for ethnicities for names.
    lastname_probability = standardize_list( test_last )
    firstname_probability = standardize_list( test_first )
    middlename_probability = standardize_list( test_middle )

    #candidate = [ lastname_probability, firstname_probability, middlename_probability ]
    # Which names are the most predictive? Multi-step process.
    # Which probability is above 75?
    # If multiple, which is higher?
    # If none, which is the highest?
    

    #products = lastname_probability*firstname_probability*middlename_probability*strd_zipcode
    products = lastname_probability*firstname_probability*strd_zipcode

    subscores = standardize_list( products )
    return subscores

def estimate_ethnicity( sub ):
    # Determines the voters' ethnicity by taking the maximum subscore calculated.
    eths_full = [ "Mexican", "PuertoRican", "Cuban", "Dominican", "Costa Rican",
            "Guatemalan", "Honduran", "Nicaraguan", "Panamanian", "Salvadoran",
            "Argentinean", "Bolivian", "Chilean", "Colombian", "Ecuadorian",
            "Paraguayan", "Peruvian", "Uruguayan", "Venezuelan" ]
    result = np.where( sub == np.amax( sub ))
    array_result = result[0]
    int_result = array_result[0]
    ethnicity = eths_full[ int_result ]
    print( ethnicity )
    return ethnicity
    

def plotting( props, labels, title ):
    """
    Plots results of proportions for categorical variables
    Inputs:
        - Proportions
        - Labels
        - Title string
    Adapted from pandas_datetime_demo.py by Dr. Dan Halperin
    """

    fig = plt.figure( figsize = ( 20,8 ))
    ax  = fig.add_axes([ 0.1, 0.1, 0.8, 0.8 ])

    # Temp and Dewpoint can be plotted from the same axis since they are a measure 
    # in the same units.
    #
    # Plotted as a function of time.
    ax.plot( labels, props, color="b", label = "Ethnicity Distribution for inputted zip" )

    # Defines the labels.
    ax.set_xlabel( "Ethnicities", fontsize=14 )
    ax.set_ylabel( "Proportion", fontsize=14 )

    # Axes ranges.
    ax.set_ylim( 0, 1 )

    # Set the fontsize for the tick labels and
    # display a grid at the tick labels
    ax.tick_params( axis= "both", labelsize = 8 )
    ax.grid()

    # Define the title.
    ax.set_title( title, fontsize = 12 ) 

    # Finish the plot by displaying and closing.
    plt.show()
    plt.close()

def subscores_fullzip( voterfile ):
    delete_cols = [ "County ID", "Voter ID", "Ignored",
            "N?", "Street Address", "APT", "City", "Ignored 2", "Zip", "1", "2", "3", "4",
            "5", "6", "7", "Sex", "Ethnicity", "Birthdate", "Something",
            "Some other number", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17",
            "18", "19", "20", "21" ]
    in_zipcode = float( input( "Zipcode: "))
    in_countycode = str( input( "County Code: "))
    voters = retrieve_zipcode_voters( in_zipcode, in_countycode, voterfile )
    print( voters )
    
    iter_c = list( voters.index.values )
    
    # List of ethnicities to be added to the end of the df 'voters'
    all_eths = []
    for i in iter_c:
        if i in list( voters.index.values ):
            sub = subscores( voters["Lastname"][i], 
                         voters["Firstname"][i], 
                         voters["Middle Name"][i], 
                         in_zipcode )
            eth = estimate_ethnicity( sub )
            all_eths.append( eth )
            
    voters["Sub Ethnicity"] = all_eths   
    #sub = subscores( in_lastname, in_firstname, in_middlename, in_zipcode )
    #eth = estimate_ethnicity( sub )
    #print( "Ethnicity: ", eth )
    voters = voters.drop( delete_cols, axis = 1 )
    #plotting( sub )
    
    # COMPARE RESULTS:
    # This is how the zip results SHOULD be.
    stat_num_voters_per_eth = stat_num_voters_per_eth = np.round( standardize_list( retrieve_zipdata( 33139 ))*len( voters ))
    
    # This is how the model predicts it to be.
    # eths_f is eths with names and not dicts
    eths_f = list( eths.values() )
    
    l = []
    counts = np.array( l )
    
    for i in eths_f:
        counts = np.append( counts, voters['Sub Ethnicity'].str.count( i ).sum())
    
    difference = stat_num_voters_per_eth - counts
    
    return voters, difference

#x, y = main()

"""
ZIP CODE EDA
"""

def EDA_zipcode( in_zip, voterfile ):
    zipvoters = retrieve_zipcode_voters( in_zip, voterfile )
    p_zip = retrieve_zipdata( in_zip )

    # Zipcode Analysis
      # Population (pop)
    
      # Hispanic Population (h_pop)
      
      # Percent Hispanic (p_h_pop)
    
    # Voting
      # Total Hispanic Voters (t)
    t = len( zipvoters )
      # Republicans, Democrats, and NPAs (counts[0:2])
    counts = np.array(   [zipvoters[ "Party Aff" ].str.count( "REP" ).sum(),
                          zipvoters[ "Party Aff" ].str.count( "DEM" ).sum(),
                          zipvoters[ "Party Aff" ].str.count( "NPA" ).sum() ])

      # Find the percentages (p)
    p = counts / t
    
    # Top 3 most common Hispanic subgroups.
    top3index = p_zip.argsort()[-3:][::-1]
    l = []
    top3 = np.array( l )
    for i in top3index:
        top3 = np.append( top3, eths[ i+1 ])
        
    dom = False    
    # Is one Hispanic group significantly common??
    if p_zip[ top3index[ 0 ]] > 0.65:
        suffix = "*"
        dom = True
    else:
        suffix = ""
        
    # Add asterisk to significantly common ethnicity.
    top3[ 0 ] = top3[ 0 ]+suffix    

    print( "--------------------------------------------------\nZip Code information for", in_zip )
    print( "# of total Hispanic voters: ", t, end = "\n\n" )


    print( "Voting Info:" )
    print( "Republicans: ",     counts[0], "(", p[0], ")" )
    print( "Democrats: ",       counts[1], "(", p[1], ")" )
    print( "NPAs: ",            counts[2], "(", p[2], ")" , end ="\n\n" )

    print( "Population Top Ethnicities:",     top3[0], "(", p_zip[ top3index[0] ], ")",
                                              top3[1], "(", p_zip[ top3index[1] ], ")",
                                              top3[2], "(", p_zip[ top3index[2] ], ")" )
    
    if dom == True:
        print( "* Denotes significantly common hispanic group.")
        print( "-----------------------------------------------------")
    else:
        print( "-----------------------------------------------------")
    # Plots the Hispanic population proportions of the zipcode.
    int_zip = int( in_zip )
    in_zip = str( int_zip )
    
    plotting_eths = np.array(list( eths.values() ))
    plotting( p_zip, plotting_eths, in_zip )
    
    # Using the plotting functionality again, we can plot democrats vs. republicans
    # vs NPAs.
    parties = [ "Republican", "Democrat", "NPA" ]
    plotting( p, parties, "Party Distribution" )
    
    top3p = np.array([ p_zip[top3index[0]], p_zip[top3index[1]], p_zip[top3index[2]] ])
    return p, top3, top3p

def EDA_nonhispanic( in_zip, voterfile ):
    voters = retrieve_nonhispanic( in_zip, voterfile )
    t = len( voters )
    # Republicans, Democrats, and NPAs (counts[0:2])
    counts = np.array(   [voters[ "Party Aff" ].str.count( "REP" ).sum(),
                          voters[ "Party Aff" ].str.count( "DEM" ).sum(),
                          voters[ "Party Aff" ].str.count( "NPA" ).sum() ])
    
    p = counts / t
    
    print( "--------------------------------------------------\nZip Code information for", in_zip )
    print( "# of total voters: ", t, end = "\n\n" )
    
    print( "Voting Info:" )
    print( "Republicans: ",     counts[0], "(", p[0], ")" )
    print( "Democrats: ",       counts[1], "(", p[1], ")" )
    print( "NPAs: ",            counts[2], "(", p[2], ")" , end ="\n\n" )
    

def county_zip_table( county_code, county_string ):
    # Returns a data frame with the top3 most common hispanic sub groups in each zip 
    # code in the provided county, as well as the voter party affiliation of that zip code.
    voterfile, zips = load_county( county_code, county_string )

    cols = [ "% Republican", "% Democrat", "% NPA", "Top 1", "% Top 1", "Top 2", "% Top 2",
        "Top 3", "% Top 3" ]

    l = []
    e = {0:np.array(l)}

    l_rep = e[0]
    l_dem = e[0]
    l_npa = e[0]
    l_top1 = e[0]
    l_p_top1 = e[0]
    l_top2 = e[0]
    l_p_top2 = e[0]
    l_top3 = e[0]
    l_p_top3 = e[0]

    for i in zips:
        p, top3, top3p = EDA_zipcode( i, voterfile )
        l_rep = np.append( l_rep, p[0] )
        l_dem = np.append( l_dem, p[1] )
        l_npa = np.append( l_npa, p[2] )
        l_top1 = np.append( l_top1, top3[0] )
        l_p_top1 = np.append( l_p_top1, top3p[0])
        l_top2 = np.append( l_top2, top3[1] )
        l_p_top2 = np.append( l_p_top2, top3p[1])
        l_top3 = np.append( l_top3, top3[2] )
        l_p_top3 = np.append( l_p_top3, top3p[2])
    
    col_data = [ l_rep, l_dem, l_npa, l_top1, l_p_top1, l_top2, l_p_top2, l_top3, l_p_top3 ]
    
    res = pd.DataFrame( index = zips, columns = cols )
    
    for i, j in zip( cols, col_data ):
        res[ i ] = j
    
    print( county_string, "loaded" )
    return res

def whatcity( in_zip ):
    # Give the name of a city of a zip code, for context.
    zips_by_name = pd.read_csv( "zip_by_county.csv" )
    
    res = find( "Code", in_zip, zips_by_name )
    city = res["Name"]
    return city
    
            
