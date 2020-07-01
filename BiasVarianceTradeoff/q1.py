import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import pickle as pckl
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
def resample(percent_train):
	file=open('./Q1_data/data.pkl','rb')
	data=pckl.load(file)
	file.close()
	rows=data.shape[0]
	np.random.shuffle(data)
	end_training=int((rows*percent_train)/100)
	training_set=data[:end_training]
	testing_set=data[end_training:]
	training_rows=training_set.shape[0]
	jump=int(training_rows/10)
	jump_array=np.arange(jump,training_rows,jump).tolist()
	np.random.shuffle(training_set)
	training_set=np.split(training_set,jump_array)
	return training_set,testing_set
def task(training,testing):
	fp=[]
	for x in range(1,10):
		poly=PolynomialFeatures(degree=x)
		spl1=np.hsplit(testing,2)
		xp=spl1[0]
		yp=spl1[1]
		X_test=poly.fit_transform(xp)
		m=linear_model.LinearRegression()
		ll=np.zeros(shape=(len(testing),1))
		tpl=[]
		tpl.append(x)
		for y in training:
			spl0=np.hsplit(y,2)
			xt=spl0[0]
			Y_train=spl0[1]
			X_train=poly.fit_transform(xt)
			m.fit(X_train,Y_train)
			tpp=m.predict(X_test)
			ll=np.hstack((ll,tpp))
		ll=np.hsplit(ll,[1])[1]
		sm=np.sum(ll,axis=1,keepdims=True)
		divd=np.divide(sm,10)
		subt=np.subtract(divd,yp)
		sqr=np.square(subt)
		bias=np.average(sqr,axis=0)
		vns=np.var(ll,axis=1,keepdims=True)
		variance=np.average(vns,axis=0)
		tpl.append(bias[0])
		tpl.append(variance[0])
		fp.append(tpl)
	tpp=['Degree','Bias Square','Variance']
	print("{: >3} {: >20} {: >28}".format(*tpp))
	for z in fp:
		print("{: >3} {: >28} {: >30}".format(*z))
	fp=np.asarray(fp)
	pt=np.hsplit(fp,3)
	x_axis=pt[0]
	y_axis1=pt[1]
	y_axis2=pt[2]
	plt.figure('Bias Variance Plot For Different Degree Polynomials')
	plt.plot(x_axis,y_axis1,linewidth=7.0)
	plt.plot(x_axis,y_axis2,linewidth=7.0)
	plt.show()
training,testing=resample(90)
task(training,testing)