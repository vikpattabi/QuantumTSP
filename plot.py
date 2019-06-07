import matplotlib.pyplot as plt

plt.bar(0, 2)
plt.bar(1, 0)
plt.bar(2, 4)
plt.bar(3, 5)
plt.title('Performance of QPE approach to TSP on 4 sample graphs')
plt.xlabel('Test graph index')
plt.ylabel('# correct solutions out of 5 trials')
plt.show()
