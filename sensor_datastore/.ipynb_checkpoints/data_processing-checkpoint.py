# +
import pandas as pd
import datetime
import pytz

class dataProcessing():
      def __init__(self):
          pass
      
      def fill_missing_values(self, data, column="TC"):
          """
              Inputs:
              data : dataframe with 
                    columns  : sensor   - has type temperature, pressure and humidity
                             : value    -  Relative values
                             : datetime -  Date-time of realization
               
               Outputs:
               data_tc : dataframe 
                       missing time series are filled, respected values are interpolated, drop duplicates
          
          """
          data["datetime"] = pd.to_datetime(data.datetime)
          # TO.DO : consider the  micro raise in time period and include to capture time period accurately.
          data["datetime"] = data.datetime.dt.floor('H')
          data_sc = data.loc[data.sensor == column]
          data_sc = data_sc.drop_duplicates(subset="datetime", keep='first', inplace=False)

          #
          # Missing values
          #

          # Generated dates
          generated = pd.date_range(start=datetime.datetime(2019, 1, 1, 0, 0, 0, 0), end=datetime.datetime(2019, 12, 31, 23, 0, 0, 0), freq="1H")
          all_values = pd.DatetimeIndex(data_sc.datetime.dt.floor('H')) 

          missing_values = generated.difference(all_values)
          missing_df = pd.DataFrame([[column, None, key] for key in missing_values], columns=list(data_sc.columns))
          data_sc = pd.concat([data_sc, missing_df]).sort_values(["datetime"])
          data_sc = data_sc.drop_duplicates(subset=None, keep='first', inplace=False)
          data_sc = data_sc.reset_index(drop=True)

          # filling missing values
          data_sc["value"] = data_sc.value.interpolate(method ='ffill')
          return data_sc

      # selecting based on date
      def filter_on_date(self, start, end, dataframe, datecol="datetime"):
        """
            filter based on start and end time over pased dataframe
        """
        return dataframe.loc[(dataframe[datecol] < end) & (dataframe[datecol] > start)]
# -


