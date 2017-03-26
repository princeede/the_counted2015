# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 14:19:52 2017

@author: OLAGUNJU
"""
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.style.use('ggplot')

#load the csv...
path = r'C:\Users\OLAGUNJU\Desktop\exc_file\kaggle\the_counted\images'

counted_15 = r'C:\Users\OLAGUNJU\Desktop\exc_file\kaggle\the_counted\2015.csv'

#Convert to a pandas dataframe
count_15 = pd.read_csv(counted_15, encoding = 'ISO-8859-1')

#Remove some columns that are not needed for the exploratory analysis
count_15 = count_15.drop([ 'latitude', 'longitude','streetaddress','city','year','uid','day'], axis = 1)
count_15.age = count_15.age.apply(pd.to_numeric, args=('coerce',))

#create a list of months...
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October','November', 'December']

#save the value_counts of months in list_months
#Note that the elemnets of list_months will not be arranged properly...
#And value_counts return a list and not a Series
list_months = count_15.month.value_counts(normalize = False, sort=False)

#Convert list_months to an pandas DataFrame(a Series to would give same result) 
df_months = pd.DataFrame({'month':list_months.index, 'value':list_months})

#create a dict **mapping**
mapping = {month: i for i, month in enumerate(months)}
#map the the element of the new DataFrame **df_months** to elements of the list **months** created above
key = df_months['month'].map(mapping)

#sort elements of **df_months** acording to key
df_months = df_months.iloc[key.argsort()]

#get the number of victims based on race and type of arm/weapon
race_armed = count_15.groupby('raceethnicity').armed.value_counts().unstack('armed')
race_armed = race_armed.div(race_armed.sum(1), axis=0)

#get the number of victims based on race and class of death
race_class = count_15.groupby('raceethnicity').classification.value_counts().unstack('classification')
race_class = race_class.div(race_class.sum(1), axis=0)

#plotting begins here---
gender = count_15.gender.value_counts(normalize = True, sort=False)
ax1 = gender.plot(kind='pie',title = 'Police Killing Based on Gender', autopct='%1.1f%%', use_index=False)
ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig(path+'\\gender.png', bbox_inches='tight')
plt.show()

armed = count_15.armed.value_counts(normalize = True, sort=False)
ax2 = armed.plot(kind='barh')
ax2.set(title='Suspect Armed?', ylabel='Type of arm', xlabel='Percentage (x100)')
plt.savefig(path+'\\armed.png', bbox_inches='tight')
plt.show()

ax3 = df_months.plot(kind='bar')
ax3.set(title='Months', xlabel = 'Month', ylabel= 'Number of killings')
plt.savefig(path+'\\month.png', bbox_inches='tight')
plt.show()

raceethnicity = count_15.raceethnicity.value_counts(normalize = True, sort=False)
ax4 = raceethnicity.plot(kind='barh')
ax4.set(title='Killing Based on Race/Ethnicity', xlabel='Rate of Killings (x100%)', ylabel='Race/Ethnicity')
plt.savefig(path+'\\race_ethnicity.png', bbox_inches='tight')
plt.show()

state = count_15.state.value_counts(normalize = False)
ax5 = state[:10].plot(kind='bar')
ax5.set(title='Top 10 States with the highest police killing record', xlabel='State', ylabel='Number of Killings')
plt.savefig(path+'\\state.png', bbox_inches = 'tight')
plt.show()

classify = count_15.classification.value_counts(normalize = True, sort=False)
ax6 = classify.plot(kind='bar')
ax6.set(title='Nature of killing', xlabel='Nature', ylabel='Rate (x100%)')
plt.savefig(path+'\\classification.png', bbox_inches = 'tight')
plt.show()

ax7 = race_armed.plot(kind='barh', stacked=True, figsize=(10,5))
ax7.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax7.set(ylabel = 'Race/Ethnicity')
plt.savefig(path+'\\race_armed.png', bbox_inches = 'tight')
plt.show()

ax8 = race_class.plot(kind='barh', stacked=True)
ax8.legend(loc='center left', bbox_to_anchor=(1,0.5))
ax8.set(ylabel = 'Race/Ethnicity')
plt.savefig(path+'\\race_class.png', bbox_inches = 'tight')
plt.show()

ax9 = count_15.age.hist(bins=20)
ax9.set(xlabel='Age', ylabel='Frequency', title='Age Distribution')
plt.savefig(path+'\\age.png', bbox_inches = 'tight')
plt.show()

count_15.loc[count_15.age <= 10, ['name','classification','raceethnicity', 'armed','lawenforcementagency']]
