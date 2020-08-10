import yfinance as yf
import pandas as pd
from datetime import timedelta

start = 		"2000-01-02"
start_minus_1 = "2000-01-01"
end = 			"2020-03-02"  # Does not get data for the end day
end_dt = 		pd.to_datetime(end)


def main():


    
	final_list = []
	final_list.append(
	    "volume,value_move_on_day,percent_move_on_day,percent_from_ten_day_ma,next_day_binary\n"
	)

	data = yf.download("SPY", start=start, end=end, group_by="ticker")
	pd_to_dict = data.to_dict("index")

	for key, value in pd_to_dict.items():

		#
		# Debug stuff
	    # print(key.date().strftime("%m/%d/%Y"))
	    # Value = {	
	    # 	'Open': 323.1400146484375, 'High': 333.55999755859375, 'Low': 321.239990234375,
	    # 	'Close': 322.4200134277344, 'Adj Close': 320.5351867675781, 'Volume': 161088400
	    # }
	    # 

		volume = value["Volume"]
		value_move_on_day = value["Close"] - value["Open"]
		percent_move_on_day = (value_move_on_day / value["Open"]) * 100
		percent_from_ten_day_ma = get_10_day_ma(key.date(), pd_to_dict)
		next_day_binary = next_day_green(key.date(), pd_to_dict)

		data_string = "{},{},{},{},{}\n".format(
		    volume,
		    value_move_on_day,
		    percent_move_on_day,
		    percent_from_ten_day_ma,
		    next_day_binary,
		)

		final_list.append(data_string)

	new_csv = open('output.csv','w')
	for x in final_list:
		new_csv.write(x)

	new_csv.close()

def next_day_green(current_day, pd_to_dict):

	next_day = current_day + timedelta(days=1)
	binary_return = 0

	while True:
		if not next_day >= end_dt:
			try:
			    pd_to_dict[pd.to_datetime(next_day)]
			    break

			except:
			    next_day = next_day + timedelta(days=1)

		else:
			return 0

	next_day_value = pd_to_dict[pd.to_datetime(next_day)]
	value_move_on_day = next_day_value["Close"] - next_day_value["Open"]

	if value_move_on_day > 0:
	    binary_return = 1

	return binary_return


def get_10_day_ma(current_day, pd_to_dict):

	#
	# 10 simple moving average
	# Get last 10 days closing price
    # Add them together and divide by 10
    # take current day and get percent away from 10 day ma
    #
	list_of_none = []
    
	current_day_value = pd_to_dict[pd.to_datetime(current_day)]
	ten_day_total = current_day_value["Close"]
	list_of_none.append(current_day_value["Close"])
	
	previous_day = current_day

	x = 1
	while x != 10:
		previous_day = previous_day + timedelta(days=-1)
		
		while True:
			if previous_day.strftime("%Y-%m-%d") != start_minus_1:
				try:
					previous_day_value = pd_to_dict[pd.to_datetime(previous_day)]
					ten_day_total = ten_day_total + previous_day_value["Close"]
					list_of_none.append(previous_day_value["Close"])
					break
				
				except:
					previous_day = previous_day + timedelta(days=-1)
			else:
				amount_off = current_day_value["Close"] - (ten_day_total / len(list_of_none))
				return ( amount_off / (ten_day_total / len(list_of_none)) ) * 100

		x+=1
	
	amount_off = current_day_value["Close"] - (ten_day_total / 10)
	return ( amount_off / (ten_day_total / 10) ) * 100


if __name__ == "__main__":
    main()
