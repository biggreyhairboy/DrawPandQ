from datasource import getaDayTicksFromSQLServer, cleanTicks

dayticks = getaDayTicksFromSQLServer("csvmode")

cleanticks = cleanTicks(dayticks)
print(cleanticks)


print('hello')