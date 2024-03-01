import internet

res = internet.Weather().get_future('Moscow')
print(res)
res = internet.Weather().get_now('Рязань')
print(res)
res = internet.Geo().get_lat_and_lon_by_name('Moscow')
print(res)
res = internet.Time().get_time('Рязань')
print(res)
res = internet.FullPlaceInfo('Москва')
print(res)
