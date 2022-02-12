import pandas as pd
import numpy as np
import math, random

# Show full width and height of dataframe
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)

# Converting csv to data frame. Total weight = 2621
data = pd.read_csv("knapsack.csv")

# Add another column for v/w 

