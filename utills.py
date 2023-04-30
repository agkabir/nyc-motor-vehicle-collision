import streamlit as st
import pandas as pd
import numpy as np
from bokeh.models import Legend, HoverTool, ColumnDataSource,HBar, FactorRange
from bokeh.plotting import figure
import bokeh.palettes as c


hour_range =[str(x) for x in np.arange(1,25,1)]
color=c.viridis(10)
vec_type_list = list(['VEHICLE TYPE CODE 1','VEHICLE TYPE CODE 2','VEHICLE TYPE CODE 3','VEHICLE TYPE CODE 4',
'VEHICLE TYPE CODE 5', 'Intersection'])

# Make dataset
def make_dataset(selected_options, data_filtered):
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

def make_dataset_intersection(selected_con_factor, data_frame,vec_type, n):
        if selected_con_factor != 'All':
            data_filt_vec_type_con_factor = data_frame[data_frame['CONTRIBUTING FACTOR VEHICLE '+ n] == selected_con_factor]
        else:
            data_filt_vec_type_con_factor = data_frame
            
        count_by_hour_and_vec_type = data_filt_vec_type_con_factor.groupby(['Hour',vec_type]).count()['CRASH DATE'].unstack()
        count_by_hour_and_vec_type = count_by_hour_and_vec_type.div(count_by_hour_and_vec_type.sum(axis =0), axis =1)
        count_by_hour_and_vec_type = count_by_hour_and_vec_type.reset_index()
        count_by_hour_and_vec_type['Hour'] = count_by_hour_and_vec_type['Hour'] + 0.5
        #print('i am here')
        return ColumnDataSource(count_by_hour_and_vec_type)
def style(p):
        # Title 
        p.title.align = 'center'
        p.title.text_font_size = '20pt'
        p.title.text_font = 'serif'

        # Axis titles
        p.xaxis.axis_label_text_font_size = '14pt'
        p.xaxis.axis_label_text_font_style = 'bold'
        p.yaxis.axis_label_text_font_size = '14pt'
        p.yaxis.axis_label_text_font_style = 'bold'

        # Tick labels
        p.xaxis.major_label_text_font_size = '12pt'
        p.yaxis.major_label_text_font_size = '12pt'

        return p

def make_plot(src, plot_scale):
    if len(src.data['no_factors'])>20:
        plot_height =700
    else:
        plot_height = 450
    # Blank plot in linear scale
    if plot_scale=='Linear Scale':
        p = figure(y_range=FactorRange(factors=list(src.data['no_factors'])),plot_width = 700, plot_height = plot_height, title = 'Bar plot of number of victims injured or killed',
                y_axis_label = 'Contributing factors', x_axis_label = 'No of victims',toolbar_location=None)
    else:
    # Blank plot in log scale
        p = figure(y_range=FactorRange(factors=list(src.data['no_factors'])),plot_width = 700, plot_height = plot_height, title = 'Bar plot of no of victims injured or killed',
                y_axis_label = 'Contributing factors', x_axis_label = 'No of victims (in log scale)', x_axis_type = 'log',toolbar_location=None)
    
    glyph = HBar(y='no_factors', right="no_victims", left=0.00001, height=0.5,  fill_color="#460E61")
    p.add_glyph(src, glyph)
    
    # Hover tool with hline mode
    hover = HoverTool(tooltips=[('Number of victims', '@no_victims'), 
                                ('Contributing Factor', '@no_factors')],
                        mode='hline')
    p.add_tools(hover)        
    return style(p)

def make_plot_intersection(src, top_ten_vec_type):
        # Blank plot with correct labels
        p = figure(x_range = FactorRange(factors=hour_range),plot_width = 950, plot_height = 500,
                   title = 'Collision per hour on Day',toolbar_location=None, x_axis_label = 'Time (Hour)', y_axis_label = 'Proportion')
        
        items = [] 
        bar ={} # to store vbars
        ### here we will do a for loop:
        for indx,i in enumerate(top_ten_vec_type):
            if indx==0:
                bar[i] = p.vbar(x='Hour',  top=i, source= src, color=color[indx], muted_color=None, muted_alpha=0.1,fill_alpha=0.5, muted = False, width=1) 
            else:
                bar[i] = p.vbar(x='Hour',  top=i, source= src, color=color[indx], muted_color=None, muted_alpha=0.1,fill_alpha=0.5, muted = True, width=1) 
            items.append((i, [bar[i]]))
            #print(items)
        legend = Legend(items=items, location=(20,40))
        p.add_layout(legend, 'right') 
        p.legend.click_policy="mute"
        
        # Styling
        p = style(p)

        return p



def make_tab_content(data_frame,vec_type,top_ten_con_fac,top_ten_vec_type):
    if vec_type!='Intersection':
        n = vec_type[-1]
    else:
        n = str(1)
    selected_con_factor = st.selectbox(
        "Contributing factor vehicle "+ n,
        top_ten_con_fac
    )
    src = make_dataset_intersection(selected_con_factor, data_frame,vec_type,n)
    plot = make_plot_intersection(src, top_ten_vec_type)
    st.bokeh_chart(plot, use_container_width=True)
