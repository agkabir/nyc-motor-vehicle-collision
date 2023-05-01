import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from os.path import dirname, join
import utills;
st.set_page_config(layout="wide")

data_raw = pd.read_csv(join(dirname(__file__),'data','Motor_Vehicle_Collisions_Crashes.csv'), sep=',', error_bad_lines=False, index_col=False, dtype='unicode',low_memory = False)
injured_killed = list(['NUMBER OF PERSONS INJURED','NUMBER OF PERSONS KILLED', 'NUMBER OF PEDESTRIANS INJURED','NUMBER OF PEDESTRIANS KILLED',
                       'NUMBER OF CYCLIST INJURED','NUMBER OF CYCLIST KILLED', 'NUMBER OF MOTORIST INJURED','NUMBER OF MOTORIST KILLED'])
cont_factor = list(['CONTRIBUTING FACTOR VEHICLE 1','CONTRIBUTING FACTOR VEHICLE 2', 'CONTRIBUTING FACTOR VEHICLE 3',
       'CONTRIBUTING FACTOR VEHICLE 4', 'CONTRIBUTING FACTOR VEHICLE 5'])

data_raw[injured_killed] = data_raw[injured_killed].fillna(0)
# Casting columns into integer type
data_raw['NUMBER OF PERSONS INJURED'] = data_raw["NUMBER OF PERSONS INJURED"].astype(float).astype(int)
data_raw['NUMBER OF PERSONS KILLED'] = data_raw["NUMBER OF PERSONS KILLED"].astype(float).astype(int)
data_raw['NUMBER OF PEDESTRIANS INJURED'] = data_raw["NUMBER OF PEDESTRIANS INJURED"].astype(float).astype(int)
data_raw['NUMBER OF PEDESTRIANS KILLED'] = data_raw["NUMBER OF PEDESTRIANS KILLED"].astype(float).astype(int)

data_raw['NUMBER OF CYCLIST INJURED'] = data_raw["NUMBER OF CYCLIST INJURED"].astype(float).astype(int)
data_raw['NUMBER OF CYCLIST KILLED'] = data_raw["NUMBER OF CYCLIST KILLED"].astype(float).astype(int)

data_raw['NUMBER OF MOTORIST INJURED'] = data_raw["NUMBER OF MOTORIST INJURED"].astype(float).astype(int)
data_raw['NUMBER OF MOTORIST KILLED'] = data_raw["NUMBER OF MOTORIST KILLED"].astype(float).astype(int)

# Creation of datetime columns
data_raw['CRASH_DATE_TIME'] = pd.to_datetime(data_raw['CRASH DATE'].str[0:10]+' '+data_raw['CRASH TIME'], format = '%m/%d/%Y %H:%M',infer_datetime_format=True)
data_raw['Year'] = data_raw['CRASH_DATE_TIME'].dt.year
data_raw['Hour'] = data_raw['CRASH_DATE_TIME'].dt.hour
data_raw['Weekday'] = data_raw['CRASH_DATE_TIME'].dt.weekday
data_raw['Weekhour'] = data_raw['Hour'] + data_raw['Weekday']*24
# Remove extra spaces at the end of each row
data_raw['ON STREET NAME'] = data_raw['ON STREET NAME'].str.strip()
data_raw['OFF STREET NAME'] = data_raw['OFF STREET NAME'].str.strip()
# Creation of the Intersection column
def intersection(df):
    inter = str(str(df['ON STREET NAME'])+', '+str(df['CROSS STREET NAME']))
    return inter
data_raw['Intersection'] = data_raw.apply(intersection, axis = 1)

# Creation of a filtered dataset which doesn't have categories that have no information, ie. Unknown, Other and Unspecified
# We also removed Passenger Vehicle because it is such a general category that doesn't offer much information
data_raw_filtered = data_raw[(data_raw['VEHICLE TYPE CODE 1'] != 'PASSENGER VEHICLE') & (data_raw['VEHICLE TYPE CODE 2'] != 'PASSENGER VEHICLE')
            & (data_raw['VEHICLE TYPE CODE 3'] != 'PASSENGER VEHICLE') & (data_raw['VEHICLE TYPE CODE 4'] != 'PASSENGER VEHICLE') & 
           (data_raw['VEHICLE TYPE CODE 5'] != 'PASSENGER VEHICLE')]

data_raw_filtered = data_raw[(data_raw['VEHICLE TYPE CODE 1'] != 'UNKNOWN') & (data_raw['VEHICLE TYPE CODE 2'] != 'UNKNOWN')
            & (data_raw['VEHICLE TYPE CODE 3'] != 'UNKNOWN') & (data_raw['VEHICLE TYPE CODE 4'] != 'UNKNOWN') & 
           (data_raw['VEHICLE TYPE CODE 5'] != 'UNKNOWN')]

data_raw_filtered = data_raw[(data_raw['VEHICLE TYPE CODE 1'] != 'OTHER') & (data_raw['VEHICLE TYPE CODE 2'] != 'OTHER')
            & (data_raw['VEHICLE TYPE CODE 3'] != 'OTHER') & (data_raw['VEHICLE TYPE CODE 4'] != 'OTHER') & 
           (data_raw['VEHICLE TYPE CODE 5'] != 'OTHER')]

data_raw_filtered = data_raw[(data_raw['CONTRIBUTING FACTOR VEHICLE 1'] != 'Unspecified') & (data_raw['CONTRIBUTING FACTOR VEHICLE 2'] != 'Unspecified')
           & (data_raw['CONTRIBUTING FACTOR VEHICLE 3'] != 'Unspecified') & (data_raw['CONTRIBUTING FACTOR VEHICLE 4'] != 'Unspecified') &
            (data_raw['CONTRIBUTING FACTOR VEHICLE 5'] != 'Unspecified')]

data_filtered = data_raw_filtered[['NUMBER OF PERSONS INJURED',
       'NUMBER OF PERSONS KILLED', 'NUMBER OF PEDESTRIANS INJURED',
       'NUMBER OF PEDESTRIANS KILLED', 'NUMBER OF CYCLIST INJURED',
       'NUMBER OF CYCLIST KILLED', 'NUMBER OF MOTORIST INJURED',
       'NUMBER OF MOTORIST KILLED', 'CONTRIBUTING FACTOR VEHICLE 1',
       'CONTRIBUTING FACTOR VEHICLE 2', 'CONTRIBUTING FACTOR VEHICLE 3',
       'CONTRIBUTING FACTOR VEHICLE 4', 'CONTRIBUTING FACTOR VEHICLE 5']]

# Remove unnecessary columns for this part
data_filtered_for_intersection_plot = data_raw_filtered[['CRASH DATE', 'Intersection','Hour','ON STREET NAME','CROSS STREET NAME',
                      'CONTRIBUTING FACTOR VEHICLE 1', 'CONTRIBUTING FACTOR VEHICLE 2','CONTRIBUTING FACTOR VEHICLE 3','CONTRIBUTING FACTOR VEHICLE 4', 'CONTRIBUTING FACTOR VEHICLE 5',
                      'VEHICLE TYPE CODE 1','VEHICLE TYPE CODE 2','VEHICLE TYPE CODE 3','VEHICLE TYPE CODE 4','VEHICLE TYPE CODE 5']]

# Lists containing the top 10 most popular categories in each column which are the ones to appear in the visualisation
top_ten_vec_type_1 = data_filtered_for_intersection_plot['VEHICLE TYPE CODE 1'].value_counts()[:10].index.tolist()
top_ten_vec_type_2 = data_filtered_for_intersection_plot['VEHICLE TYPE CODE 2'].value_counts()[:10].index.tolist()
top_ten_vec_type_3 = data_filtered_for_intersection_plot['VEHICLE TYPE CODE 3'].value_counts()[:10].index.tolist()
top_ten_vec_type_4 = data_filtered_for_intersection_plot['VEHICLE TYPE CODE 4'].value_counts()[:10].index.tolist()
top_ten_vec_type_5 = data_filtered_for_intersection_plot['VEHICLE TYPE CODE 5'].value_counts()[:10].index.tolist()
# Some interection values were partly NaN, so it had to be filtered using the original columns
data_inter = data_filtered_for_intersection_plot[~data_filtered_for_intersection_plot['ON STREET NAME'].isna() & ~data_filtered_for_intersection_plot['CROSS STREET NAME'].isna()]
top_ten_inter = data_inter['Intersection'].value_counts()[:10].index.tolist()

# Filtering the dataset to only contain the rows which are in the top 10 most popular. Also dropped the unnecessary columns
data_filt_vec_type_1 = data_filtered_for_intersection_plot[data_filtered_for_intersection_plot['VEHICLE TYPE CODE 1'].isin(top_ten_vec_type_1)].drop(['ON STREET NAME', 'CROSS STREET NAME'], axis = 'columns')
data_filt_vec_type_2 = data_filtered_for_intersection_plot[data_filtered_for_intersection_plot['VEHICLE TYPE CODE 2'].isin(top_ten_vec_type_2)].drop(['ON STREET NAME', 'CROSS STREET NAME'], axis = 'columns')
data_filt_vec_type_3 = data_filtered_for_intersection_plot[data_filtered_for_intersection_plot['VEHICLE TYPE CODE 3'].isin(top_ten_vec_type_3)].drop(['ON STREET NAME', 'CROSS STREET NAME'], axis = 'columns')
data_filt_vec_type_4 = data_filtered_for_intersection_plot[data_filtered_for_intersection_plot['VEHICLE TYPE CODE 4'].isin(top_ten_vec_type_4)].drop(['ON STREET NAME', 'CROSS STREET NAME'], axis = 'columns')
data_filt_vec_type_5 = data_filtered_for_intersection_plot[data_filtered_for_intersection_plot['VEHICLE TYPE CODE 5'].isin(top_ten_vec_type_5)].drop(['ON STREET NAME', 'CROSS STREET NAME'], axis = 'columns')
data_filt_inter = data_filtered_for_intersection_plot[data_filtered_for_intersection_plot['Intersection'].isin(top_ten_inter)].drop(['ON STREET NAME', 'CROSS STREET NAME'], axis = 'columns')

# Creation of the secondary filter lists, which contain the top 10 most popular categories in the other column of the filtered dataset
top_ten_con_fac1 = data_filtered_for_intersection_plot['CONTRIBUTING FACTOR VEHICLE 1'].value_counts()[:10].index.tolist()
top_ten_con_fac2 = data_filtered_for_intersection_plot['CONTRIBUTING FACTOR VEHICLE 2'].value_counts()[:10].index.tolist()
top_ten_con_fac3 = data_filtered_for_intersection_plot['CONTRIBUTING FACTOR VEHICLE 3'].value_counts()[:10].index.tolist()
top_ten_con_fac4 = data_filtered_for_intersection_plot['CONTRIBUTING FACTOR VEHICLE 4'].value_counts()[:10].index.tolist()
top_ten_con_fac5 = data_filtered_for_intersection_plot['CONTRIBUTING FACTOR VEHICLE 5'].value_counts()[:10].index.tolist()
top_ten_con_facint = data_filt_inter['CONTRIBUTING FACTOR VEHICLE 1'].value_counts()[:10].index.tolist()
# Added an 'All' option to all filters
top_ten_con_fac1.insert(0,'All')
top_ten_con_fac2.insert(0,'All')
top_ten_con_fac3.insert(0,'All')
top_ten_con_fac4.insert(0,'All')
top_ten_con_fac5.insert(0,'All')
top_ten_con_facint.insert(0,'All')
## Frontend display
st.header('Motor Vehicle Collisions - Crashes')
st.write("The [Motor Vehicle Collisions](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95) data set contain information from all police reported motor vehicle collisions in NYC. The time frame on the data is from 2012 to 2020. The dataset contains 1.69 millions of rows and 29 columns and each rows represents Motor Vehicle Collision.")
st.subheader('Basic Statistics:')
st.write(data_raw_filtered.describe())
st.subheader('Weekly pattern of collisions')
# bar plot of nubmer of vehicle colission per hour in whole week
colission_by_weekhour = data_raw_filtered.groupby(['Weekhour']).size()
colission_counts_weekhour = colission_by_weekhour.loc[colission_by_weekhour.index]
fig = plt.figure(figsize=(30,10))
plt.bar(colission_by_weekhour.index, colission_counts_weekhour)
plt.xlabel('Weekhour')
plt.ylabel('Colission Count')
plt.xticks(rotation=0)
plt.title('Number of colision on week hours')
st.pyplot(fig)

st.subheader("Interactive bar plot of Number of persons injured/killed related to Contributing Factors")
st.write("The bar plot below plots the number of victims injured/ killed by the different contributing factors.\
                The plot can be viewed in either linear or in log scale. Furthermore, the plot can also be viewed by \
                ranging the slider to get the idea about which contributing factor is more responsible for injuring/killing \
                victims. This plot may take a while to update and load, please be patient.")

## Showing interactive bar plot and controls
#fig1_controls, fig1 = st.columns([1,2])
#with fig1_controls:
control_expander = st.expander("Select the options to view interactive plots", expanded=False)
with control_expander:
    injury_type = st.selectbox(
        'Select type of injury:',
        injured_killed
    )
    contribution_factor = st.selectbox(
        'Contribution Factor vehicles: ',
        cont_factor
    )
    plot_scale = st.radio(
        'Choose Axis Type: ',
        ['Linear Scale', 'Log Scale']
    )
    no_vehicles = st.slider(
        'Contribution Factors: ',
        5,50,5
    )

## initial selection
initial_selections = [injury_type, contribution_factor, plot_scale,no_vehicles]
src = utills.make_dataset(initial_selections, data_filtered)

plot_bar = utills.make_plot(src, plot_scale)

#with fig1:
st.bokeh_chart(plot_bar, use_container_width=True)

### interactive plot section of intersection part
st.subheader('Bar plot of Collisions per hour related to Vehicle type')
st.write('''This barplot shows the proportion of accidents during the day for the most common vehicle types. 
It is also possible to filter on the contributing causes for each vehicle in the collision. The labels 
"Vehicle type code #" and "Contributing factor vehicle #" addresses the different cars involved in an accident
 with number one being the primary car in the accident. This plot may take a while to update and load, please be patient. Furthermore due to constraints in processing time in order to run the visualisation this plot contains 2/41 parts of the original dataset, this amounts 80 000 observation.''')
## Making tab and intersection plot
vec_type_list = list(['VEHICLE TYPE CODE 1','VEHICLE TYPE CODE 2','VEHICLE TYPE CODE 3','VEHICLE TYPE CODE 4',
'VEHICLE TYPE CODE 5', 'Intersection'])
tab1, tab2,tab3,tab4,tab5,tab6 = st.tabs(vec_type_list)
with tab1:
    utills.make_tab_content(data_filt_vec_type_1,vec_type_list[0],top_ten_con_fac1,top_ten_vec_type_1)
with tab2:
    utills.make_tab_content(data_filt_vec_type_2,vec_type_list[1],top_ten_con_fac2,top_ten_vec_type_2)
with tab3:
    utills.make_tab_content(data_filt_vec_type_3,vec_type_list[2],top_ten_con_fac3,top_ten_vec_type_3)
with tab4:
    utills.make_tab_content(data_filt_vec_type_4,vec_type_list[3],top_ten_con_fac4,top_ten_vec_type_4)
with tab5:
    utills.make_tab_content(data_filt_vec_type_5,vec_type_list[4],top_ten_con_fac5,top_ten_vec_type_5)
with tab6:
    utills.make_tab_content(data_filt_inter,vec_type_list[5],top_ten_con_facint,top_ten_inter)