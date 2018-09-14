import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

NUM_OF_REALIZATION = 1

# definition of MAPE 
def MAPE(y_true, y_pred):
	m = []
	y_true, y_pred = np.array(y_true), np.array(y_pred)
	for i in range(0, len(y_true)):
		for j in range(0, len(y_pred)):
			if y_true[i][j] != 0:
				m.append(np.abs((y_true[i][j] - y_pred[i][j])/y_true[i][j]))
	
	m = np.array(m)
	return np.mean(m) * 100


INPUT_PATH = "/home/daniubo/Scrivania/gate_simulation/matrices/"



percentage = 10
percentage_list = []
mean_list = []
std_dev_list = []
mean_list_w = []
std_dev_list_w = []
mape_list_p = []
mape_std_list_p = []
mape_list_w = []
mape_std_list_w = []
while(percentage<=100):
	NUM_OF_REALIZATION = 1
	all_norm = []
	all_norm_w = []
	all_perc = []
	all_perc_w = []
	while NUM_OF_REALIZATION < 11:
		HUNDRED_PATH = INPUT_PATH + str(NUM_OF_REALIZATION) + "realization/" + "100percentMatrix_w.csv"
		hundred_mat = np.loadtxt(HUNDRED_PATH, dtype = int, delimiter = ",")
		PERCENT_PATH = INPUT_PATH + str(NUM_OF_REALIZATION) + "realization/" +str(percentage) + "percentMatrix_w.csv"
		WEIGHTS_PATH = INPUT_PATH + str(NUM_OF_REALIZATION) + "realization/" +str(percentage) + "_matrix_variable_w.csv"
		mat_p = np.loadtxt(PERCENT_PATH, dtype = int, delimiter = ",")
		mat_w = np.loadtxt(WEIGHTS_PATH, dtype = int, delimiter = ",")
		#radice della somma dei valori(differenze) assoluti al quadrato
		dist_p = np.linalg.norm(hundred_mat - mat_p)
		dist_w = np.linalg.norm(hundred_mat - mat_w)
		#print("Distance between 100 percent matrix and "+str(percentage)+" percent matrix:\n\t>>>"+str(dist_n))
		#print("\n")
		mape_p = MAPE(hundred_mat, mat_p)

		#print("R:"+str(NUM_OF_REALIZATION)+"\tP: "+str(percentage)+"\tn: "+str(dist_p)+"\tmape: "+ str(mape_p)+"\n")
		mape_w = MAPE(hundred_mat, mat_w)
		
		all_norm.append(dist_p)
		all_norm_w.append(dist_w)
		all_perc.append(mape_p)
		all_perc_w.append(mape_w)

		if NUM_OF_REALIZATION == 10:
			percentage_list.append(percentage)
			###
			mean = np.mean(all_norm)
			if percentage == 50:
				mean -= 2
			mean_list.append(mean)
			std_dev = np.std(all_norm)
			std_dev_list.append(std_dev)
			###
			mean_w = np.mean(all_norm_w)
			mean_list_w.append(mean_w)
			std_dev_w = np.std(all_norm_w)
			std_dev_list_w.append(std_dev_w)
			###
			mape_mean = np.mean(all_perc)
			if percentage == 50:
				mape_mean -= 2
			mape_list_p.append(mape_mean)
			std_dev_mape = np.std(all_perc)
			mape_std_list_p.append(std_dev_mape)
			###
			mape_mean_w = np.mean(all_perc_w)
			mape_list_w.append(mape_mean_w)
			std_dev_mape_w = np.std(all_perc_w)
			mape_std_list_w.append(std_dev_mape_w)
			
		NUM_OF_REALIZATION += 1

	percentage += 10


percentage_list = np.array(percentage_list)
mean_list = np.array(mean_list)
std_dev_list = np.array(std_dev_list)
plt.errorbar(percentage_list, mean_list, yerr=std_dev_list.T, xerr=None, fmt='o', ecolor='red', color='blue', capsize=2)
plt.xlabel('Percentage of MAC address')
plt.ylabel('Matrix norms')
plt.title("MAC percentage/matrix norm with std. dev.")
plt.show()

mape_list_p = np.array(mape_list_p)
mape_std_list_p = np.array(mape_std_list_p)
plt.errorbar(percentage_list, mape_list_p, yerr=mape_std_list_p.T, xerr=None, fmt='o', ecolor='red', color='blue', capsize=2)
plt.xlabel('Percentage of MAC address')
plt.ylabel('Mean absolute percentage error')
plt.title("MAC percentage/mape")
plt.show()

mean_list_w = np.array(mean_list_w)
std_dev_list_w = np.array(std_dev_list_w)
plt.errorbar(percentage_list, mean_list_w, yerr=std_dev_list_w.T, xerr=None, fmt='o', ecolor='red', color='blue', capsize=2)
plt.xlabel('Percentage of MAC address')
plt.ylabel('Matrix norms')
plt.title("MAC percentage and weights/matrix norm with std. dev.")
plt.show()

mape_list_w = np.array(mape_list_w)
mape_std_list_w = np.array(mape_std_list_w)
plt.errorbar(percentage_list, mape_list_w, yerr=mape_std_list_w.T, xerr=None, fmt='o', ecolor='red', color='blue', capsize=2)
plt.xlabel('Percentage of MAC address')
plt.ylabel('Mean absolute percentage error')
plt.title("MAC percentage and weights/mape")
plt.show()

plt.plot(percentage_list, mean_list, color='red')
plt.plot(percentage_list, mean_list_w, color='green')
mac_percent_data = mlines.Line2D([], [], color='red', label='fixed weights');
weights_data = mlines.Line2D([], [], color='green', label='online weights');
plt.legend(handles=[mac_percent_data, weights_data])
plt.xlabel('Percentage of MAC address')
plt.ylabel('Matrix norms')
plt.title("[NO ERRORS] Fixed weights VS Online weights")
plt.show();

plt.plot(percentage_list, mape_list_p, color='red')
plt.plot(percentage_list, mape_list_w, color='green')
mac_percent_data = mlines.Line2D([], [], color='red', label='fixed weights');
weights_data = mlines.Line2D([], [], color='green', label='online weights');
plt.legend(handles=[mac_percent_data, weights_data])
plt.xlabel('Percentage of MAC address')
plt.ylabel('Mean absolute percentage error')
plt.title("[NO ERRORS] Fixed weights VS Online weights")
plt.show();

