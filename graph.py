import matplotlib.pyplot as plt
names = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
values = [1, 3, 7, 4, 0, 2, 0, 0, 2, 1, 12, 4]

plt.bar(names, values)
plt.suptitle('Cant. multas por mes')
plt.show()