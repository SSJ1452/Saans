from ozon3.ozon3 import Ozon3 as ooo


o3 = ooo.Ozon3('YOUR_PRIVATE_TOKEN')
data = o3.get_city_air('New Delhi')

data = o3.get_multiple_city_air(['London', 'Hong Kong', 'New York'])     # As many locations as you need


__all__ = ["Ozon3"]
