text = '''65,000 km
·
Diesel
·
Manual
·
3rd Owner'''

p_text = text.replace('\n·\n',' ').split(' ')
km_driven = (' ').join(p_text[:2])
owner = (' ').join(p_text[-2:])
