from datetime import date

print(date.today())

if date.today() > date(2026, 5, 1):
    print('LA FECHA ES MAYOR')
elif date.today() < date(2026, 5, 1):
    print('LA FECHA ES MENOR')
else:
    print('LAS FECHAS SON IGUALES')

if date.today() > date(2026, 9, 1):
    print('LA FECHA ES MAYOR')
elif date.today() < date(2026, 9, 1):
    print('LA FECHA ES MENOR')
else:
    print('LAS FECHAS SON IGUALES')

if date.today() > date(2026, 5, 31):
    print('LA FECHA ES MAYOR')
elif date.today() < date(2026, 5, 31):
    print('LA FECHA ES MENOR')
else:
    print('LAS FECHAS SON IGUALES')