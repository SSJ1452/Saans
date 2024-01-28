import ozon3 as ooo

o3 = ooo.Ozon3('74e1baea1897604d8abd1cb708e92c112c7d70d7')
data = o3.get_city_air('Mumbai')
print(data)