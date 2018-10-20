import pandas as pd
import numpy as np
import altair as alt
alt.renderers.enable('notebook')
alt.data_transformers.enable('json')
import psrqpy
from astropy.coordinates import Angle
from astropy import units as  u
from astropy.coordinates import ICRS, Galactic, FK4, FK5, SkyCoord 
catalogue = psrqpy.QueryATNF(params=['PSRJ','P0','P1', 'DM','DIST', 'F0', 'F1', 'RAJ', 'DecJ','Dist_DM','AGE','BSurf', 'Date'])
catalogue = catalogue.table
catalogue = catalogue.to_pandas()

coordinates = catalogue['RAJ'] + ' ' + catalogue['DECJ']
coordinates = coordinates.replace(to_replace='None None', value='0:00:00 0:00:00')
catalogue['log_P0'] = np.log10(catalogue['P0'].values)
catalogue['log_P1'] = np.log10(catalogue['P1'].values)
catalogue['log_F0'] = np.log10(catalogue['F0'].values)
catalogue['log_AGE'] = np.log10(catalogue['AGE'].values)
catalogue['log_DIST_DM'] = np.log10(catalogue['DIST_DM'].values)
catalogue['DIST_DM'] = catalogue['DIST_DM'].fillna(0)
catalogue['BSURF'] = catalogue['BSURF'].fillna(0)
c = SkyCoord(coordinates.values, unit=(u.hourangle, u.deg))
catalogue['ra'] = c.ra.degree
catalogue['dec']= c.dec.degree

xx = np.array([-0.51, 51.2])
yy = np.array([0.33, 51.6])
means = [xx.mean(), yy.mean()]  
stds = [xx.std() / 3, yy.std() / 3]
corr = 0.8         # correlation
covs = [[stds[0]**2          , stds[0]*stds[1]*corr], 
        [stds[0]*stds[1]*corr,           stds[1]**2]] 

m = np.random.multivariate_normal(means, covs, 1000)
ml_scores=pd.DataFrame(m, columns=['pics','peace'])
catalogue=pd.concat([catalogue,ml_scores],axis=1)
url = 'data.json'
catalogue.to_json(url, orient='records')


bkg_colour = "#18183D"
grid_colour = "darkgrey"
label_colour = "lightgrey"
highlight_colour = "#FFFFFFF"
mean_colour = "#7FCDBB"
fade_colour = "#225EA8"


# RA & Dec: Distribution of pulsars
interval = alt.selection_interval(encodings=['x'])

coordinates=alt.Chart(url).mark_point(opacity = 1).encode(
    alt.X('ra:Q', axis=alt.Axis(title='Right Ascention'),scale=alt.Scale(zero=False, domain=[0,360])),
    alt.Y('dec:Q', axis=alt.Axis(title='Declination'), scale=alt.Scale(zero=False, domain=[-90, +90])),
    color = alt.condition(interval, alt.value("black"), alt.value(highlight_colour)),
    tooltip = ['PSRJ:O', 'ra:Q', 'dec:Q', 'DM:Q','P0:Q', 'F0:Q'],
    opacity=alt.value(1.0)
).properties(
selection = interval,
height=200,
width=450
)

# P-Pdot diagram
p_pdot = alt.Chart(url).mark_circle(size=6).encode(
    x=alt.X("log_P0:Q", axis=alt.Axis(title="Spin Period")),
    y=alt.Y('log_P1:Q',  axis=alt.Axis(title='Spin Period Derivative')),
    tooltip = ['PSRJ:O', 'ra:Q', 'dec:Q', 'DM:Q','P0:Q', 'F0:Q'],
    color = alt.condition(interval, alt.value("black"), alt.value(highlight_colour)),
).properties(
selection = interval,
height=200,
width=450
)

#Age of pulsar histogram
age_histogram = alt.Chart(url).mark_bar().encode(
    x=alt.X("log_AGE:Q", bin=alt.Bin(maxbins=40), axis=alt.Axis(title="Age of pulsar 10^years"), \
           scale=alt.Scale(zero=False, domain=[2,12])
           ),
    tooltip = ['PSRJ:O', 'ra:Q', 'dec:Q', 'DM:Q','P0:Q', 'F0:Q'],
    y=alt.Y('count()', axis=alt.Axis(title="Number of Pulsars")),
    #color = alt.condition(interval, alt.value("red"), alt.value(highlight_colour)),
    color = alt.value('red'),
).properties(
selection = interval,
height=200,
width=450
)
#DM Distance
dm_histogram = alt.Chart(url).mark_bar().encode(
    x=alt.X("log_DIST_DM:Q", bin=alt.Bin(maxbins=40), axis=alt.Axis(title="Calculated Distance based on Dispersion Measure (kpc)")),
    y=alt.Y('count()', axis=alt.Axis(title="Number of Pulsars")),
    #color = alt.condition(interval, alt.value("red"), alt.value(highlight_colour)),
    color = alt.value("black"),
    tooltip = ['PSRJ:O', 'ra:Q', 'dec:Q', 'DM:Q','P0:Q', 'F0:Q']
).properties(
selection = interval,
height=200,
width=450
).interactive()

#Spin Frequency vs dm
spin_frequency_dm =alt.Chart(url).mark_point().encode(
    x=alt.X('log_F0:Q', axis=alt.Axis(title='Log Spin Frequency')),
    y=alt.Y('DM:Q', axis=alt.Axis(title='Dispersion Measure')),
    tooltip = ['PSRJ:O', 'ra:Q', 'dec:Q', 'DM:Q','P0:Q', 'F0:Q'],
   color = alt.condition(interval, alt.value("black"), alt.value(highlight_colour)),
).properties(
selection = interval,
height=200,
width=450
).interactive()

#Spin Period vs dm
spin_period_dm =alt.Chart(url).mark_point().encode(
    x=alt.X('log_P0:Q', axis=alt.Axis(title='Log Spin Period')),
    y=alt.Y('DM:Q', axis=alt.Axis(title='Dispersion Measure')),
    tooltip = ['PSRJ:O', 'ra:Q', 'dec:Q', 'DM:Q','P0:Q', 'F0:Q'],
    color = alt.condition(interval, alt.value("black"), alt.value(highlight_colour)),
).properties(
selection = interval,
height=200,
width=450
).interactive()

#Discovery chart
discovery_chart = alt.Chart(url).mark_area().encode(
    x=alt.X('DATE:Q',scale= alt.Scale(zero=False, domain=[1960,2019]), axis=alt.Axis(title='Year'), ),
    y=alt.Y('count()', axis=alt.Axis(title="Number of Pulsars")),
   color =  alt.value("black"),
).properties(
    #selection = interval,
    height=200,
    width=960).interactive()

heatmap = alt.Chart(url).mark_rect().encode(
    alt.X('log_F0:Q', bin=True, axis=alt.Axis(title="Spin Frequency")),
    alt.Y('DM:Q', bin=True, axis=alt.Axis(title="Dispersion Measure")),
    alt.Color('count():Q')
).properties(
selection = interval,
height=200,
width=450
).interactive()

points = alt.Chart(url).mark_circle(
    color='black',
    size=5,
).encode(
    x='log_F0:Q',
    y='DM:Q',
)

ml_model=alt.Chart(url).mark_point(opacity = 1).encode(
    alt.X('pics:Q', axis=alt.Axis(title='Model 1')),
    alt.Y('peace:Q', axis=alt.Axis(title='Model 2')),
    color = alt.condition(interval, alt.value("black"), alt.value(highlight_colour)),
    tooltip = ['PSRJ:O', 'ra:Q', 'dec:Q', 'DM:Q','P0:Q', 'F0:Q'],
    opacity=alt.value(1.0)
).properties(
selection = interval,
height=200,
width=960
).interactive()

final_chart = ((coordinates | dm_histogram) & ml_model & (spin_frequency_dm | (points + heatmap))  & (discovery_chart)).properties(
    title='Pulsar Dashboard')
final_chart.save('dashboard.html')
final_chart