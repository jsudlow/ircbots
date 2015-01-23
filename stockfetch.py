import ystockquote
#print ystockquote.get_price('GOOG')

stock_string = "twisty: @stock goog"
lines = stock_string.split(' ')

print ystockquote.get_price(lines[-1])