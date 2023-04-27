import streamlit as st
import pandas as pd
import numpy as np
from bokeh.models import Legend, HoverTool, ColumnDataSource,HBar, FactorRange
from bokeh.plotting import figure

from os.path import dirname, join

data_raw_filtered = pd.read_csv(join(dirname(__file__),'data','Motor_collision_filtered.csv'))



injured_killed = list(['NUMBER OF PERSONS INJURED','NUMBER OF PERSONS KILLED', 'NUMBER OF PEDESTRIANS INJURED','NUMBER OF PEDESTRIANS KILLED',
                       'NUMBER OF CYCLIST INJURED','NUMBER OF CYCLIST KILLED', 'NUMBER OF MOTORIST INJURED','NUMBER OF MOTORIST KILLED'])
cont_factor = list(['CONTRIBUTING FACTOR VEHICLE 1','CONTRIBUTING FACTOR VEHICLE 2', 'CONTRIBUTING FACTOR VEHICLE 3',
       'CONTRIBUTING FACTOR VEHICLE 4', 'CONTRIBUTING FACTOR VEHICLE 5'])


data_filtered = data_raw_filtered[['NUMBER OF PERSONS INJURED',
       'NUMBER OF PERSONS KILLED', 'NUMBER OF PEDESTRIANS INJURED',
       'NUMBER OF PEDESTRIANS KILLED', 'NUMBER OF CYCLIST INJURED',
       'NUMBER OF CYCLIST KILLED', 'NUMBER OF MOTORIST INJURED',
       'NUMBER OF MOTORIST KILLED', 'CONTRIBUTING FACTOR VEHICLE 1',
       'CONTRIBUTING FACTOR VEHICLE 2', 'CONTRIBUTING FACTOR VEHICLE 3',
       'CONTRIBUTING FACTOR VEHICLE 4', 'CONTRIBUTING FACTOR VEHICLE 5']]

fig1_controls, fig1 = st.columns([1,2])
with fig1_controls:
    injury_type = st.selectbox(
        'Select type of injury:',
        injured_killed
    )
    contribution_factor = st.selectbox(
        'Contribution Factor: ',
        cont_factor
    )
    plot_scale = st.radio(
        'Choose Axis Type: ',
        ['Linear Scale', 'Log Scale']
    )
    no_vehicles = st.slider(
        'No of contributing vehicles: ',
        5,50,5
    )

# Make dataset
def make_dataset(selected_options):
        by_factor_injured = pd.DataFrame(columns=['no_factors', 'no_victims','axis_type'])
        group_by = data_filtered.groupby(selected_options[1],as_index = False)[selected_options[0]].sum()
        #print(group_by)
        by_factor_injured['no_factors'] = group_by[selected_options[1]]
        by_factor_injured['no_victims'] = group_by[selected_options[0]]
        by_factor_injured['axis_type'] = selected_options[2]
        by_factor_injured['height'] = 450 + 5 * selected_options[3]
        by_factor_injured = by_factor_injured.sort_values(['no_victims'], ascending=True)
        by_factor_range_injured = by_factor_injured.tail(selected_options[3])
        #print(by_factor_range_injured)
        
        return ColumnDataSource(by_factor_range_injured)

## initial selection
initial_selections = [injury_type, contribution_factor, plot_scale,no_vehicles]
src = make_dataset(initial_selections)

def make_plot(src, plot_scale):
        # Blank plot in linear scale
        if plot_scale=='Linear Scale':
            p = figure(y_range=FactorRange(factors=list(src.data['no_factors'])),plot_width = 700, plot_height = 450, title = 'Bar plot of number of victims injured or killed',
                  y_axis_label = 'Contributing factor', x_axis_label = 'No of victims',toolbar_location=None)
        else:
        # Blank plot in log scale
            p = figure(y_range=FactorRange(factors=list(src.data['no_factors'])),plot_width = 700, plot_height = 450, title = 'Bar plot of no of victims injured or killed',
                  y_axis_label = 'Contributing factor', x_axis_label = 'No of victims', x_axis_type = 'log',toolbar_location=None)
        
        glyph = HBar(y='no_factors', right="no_victims", left=0.00001, height=0.5,  fill_color="#460E61")
        p.add_glyph(src, glyph)
        
        # Hover tool with hline mode
        hover = HoverTool(tooltips=[('Number of victims', '@no_victims'), 
                                    ('Contributing Factor', '@no_factors')],
                          mode='hline')
        p.add_tools(hover)        
        return p
plot = make_plot(src, plot_scale)
def style(p):
        # Title 
        p.title.align = 'center'
        p.title.text_font_size = '14pt'
        p.title.text_font = 'serif'

        # Axis titles
        p.xaxis.axis_label_text_font_size = '14pt'
        p.xaxis.axis_label_text_font_style = 'bold'
        p.yaxis.axis_label_text_font_size = '14pt'
        p.yaxis.axis_label_text_font_style = 'bold'
        return p
with fig1:
    st.bokeh_chart(style(plot), use_container_width=True)