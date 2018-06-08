####### Multi-Linear Regression W/ Packet Loss & Qualfun Version (A)

xi2_a = df[['delay_sum','a_maxjitter', 'qualfun_a']].values
x2_a = np.zeros((xi2_a.shape[0], xi2_a.shape[1]+1))
x2_a[:,:-1] = xi2_a
x2_a[:,-1] = np.ones(xi2_a.shape[0])

fig4 = plt.figure(4)
y2 = sum_pkt_loss_a.values
m2 = np.linalg.lstsq(x2_a,y2)
yfit2 = x2_a.dot(m2[0])
print (yfit2.shape, y2.shape, m2[0].shape, x2_a.shape)
i = range(len(y2))
print(m2[0])
plt.plot(i,y2,'ro')
plt.plot(i,yfit2,':')
plt.xlabel('Data Points Numbers')
plt.ylabel('Regression')
plt.title('Multi-Linear Regression w/ packet loss & Qualfun Version (A)')
fig4.show()
plt.show()

####### Multi-Linear Regression W/ Packet Loss & Qualfun Version (A)

xi2_b = df[['delay_sum','b_maxjitter', 'qualfun_b']].values
x2_b = np.zeros((xi2_b.shape[0], xi2_b.shape[1]+1))
x2_b[:,:-1] = xi2_b
x2_b[:,-1] = np.ones(xi2_b.shape[0])


fig5 = plt.figure(5)
y3 = sum_pkt_loss_b.values
m3 = np.linalg.lstsq(x2_b,y3)
yfit3 = x2_b.dot(m3[0])
print (yfit3.shape, y3.shape, m3[0].shape, x2_b.shape)
i0 = range(len(y3))
print(m3[0])
plt.plot(i, y3, 'ro')
plt.plot(i,yfit3,':')
plt.title('Multi-Linear Regression w/ packet loss & Qualfun Version (B)')
plt.xlabel('Data Points Numbers')
plt.ylabel('Regression')
fig5.show()
plt.show()


###### Histogram part A
fig5 = plt.figure(5)

qual_a = [ df['qualfun_a'], df['qualfun_b'] ]
qualbins_hist_a = np.arange(df['qualfun_b'].idmin(),df['qualfun_a'].idmax())

hist_labels_a = ['qualfun_a', 'qualfun_b']
plt.hist(qual_a, bins = qualbins_hist_a, alpha=1, label= hist_labels)
plt.legend(loc='upper left')
plt.grid(True)
plt.axis([0, 45, 0, 1200000],'scaled')
plt.xlabel('MOS Scores')
plt.ylabel('Frequency')
plt.title('Histogram w/ Qualfun A & B')
fig5.show()
plt.show()

