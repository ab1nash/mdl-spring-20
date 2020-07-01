import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import pickle as pk
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
file = open('./Q2_data/X_train.pkl','rb')
xt = pk.load(file)
file.close()
file = open('./Q2_data/Y_train.pkl','rb')
yt = pk.load(file)
file.close()
file = open('./Q2_data/X_test.pkl','rb')
Xtt = pk.load(file)
Xtest = Xtt.reshape(-1,1)
file.close()
file = open('./Q2_data/Fx_test.pkl','rb')
fxtest = pk.load(file)
fxtest=fxtest.reshape(-1,1)
file.close()
fp=[]
for x in range(1,10):
    poly=PolynomialFeatures(degree=x)
    X_test=poly.fit_transform(Xtest)
    m=linear_model.LinearRegression()
    ll=np.zeros(shape=(len(Xtest),1))
    tpl=[]
    tpl.append(x)
    for y in range(len(xt)):
        x_ttrain=xt[y]
        y_train=yt[y]
        x_ttrain=x_ttrain.reshape(-1,1)
        X_train=poly.fit_transform(x_ttrain)
        m.fit(X_train,y_train)
        tpp=m.predict(X_test)
        tpp=tpp.reshape(-1,1)
        ll=np.hstack((ll,tpp))
    ll=np.hsplit(ll,[1])[1]
    sm=np.sum(ll,axis=1,keepdims=True)
    divd=np.divide(sm,20)
    subt=np.subtract(divd,fxtest)
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