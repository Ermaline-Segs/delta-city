"""Room plans for the Delta City homes. Rects are wall centre lines (x0, y0, x1, y1), metres, front at small y.
door tuple: (room_a, room_b | 'out', width, 'door'|'arch', position 0..1 along the shared wall, side for 'out', main?)"""
import copy


def R(name, kind, x0, y0, x1, y1, **kw):
    return dict(name=name, kind=kind, rect=(x0, y0, x1, y1), **kw)


# ---------------------------------------------------------------- self-contained room (one unit)
def room_unit(i=None):
    s = '' if i is None else f'_{i}'
    return dict(rooms=[R('veranda' + s, 'open', 0, 0, 4.2, 2.0), R('room' + s, 'bed', 0, 2.0, 4.2, 6.0),
                       R('kitchenette' + s, 'kitchen', 0, 6.0, 2.1, 7.8), R('shower' + s, 'bath', 2.1, 6.0, 4.2, 7.8)],
                doors=[('room' + s, 'veranda' + s, 0.9, 'door', 0.2, None, True), ('room' + s, 'kitchenette' + s, 1.0, 'arch'),
                       ('room' + s, 'shower' + s, 0.75)])


def shift(unit, dx=0.0, dy=0.0):
    u = copy.deepcopy(unit)
    for r in u['rooms']:
        x0, y0, x1, y1 = r['rect']; r['rect'] = (x0 + dx, y0 + dy, x1 + dx, y1 + dy)
    return u


ROOM_INTERIOR = dict(name='self_contained_room', floors=[dict(z=0, **room_unit())], party=[('v', 0.0), ('v', 4.2)])


def room_row():
    rooms, doors = [], []
    for i in range(6):
        u = shift(room_unit(i + 1), dx=4.2 * i); rooms += u['rooms']; doors += u['doors']
    return dict(name='room_row', floors=[dict(z=0, rooms=rooms, doors=doors)], steps=[(0, 25.2, 0, '-y')])


# ---------------------------------------------------------------- 2-bedroom flat (one unit, gallery in front)
def flat_unit(i=None, z=0):
    s = '' if i is None else f'_{i}'
    rooms = [R('living' + s, 'living', 0, 1.5, 5.4, 6.3), R('kitchen' + s, 'kitchen', 5.4, 1.5, 8.4, 4.5), R('store' + s, 'store', 8.4, 1.5, 10.2, 4.5),
             R('hall' + s, 'corridor', 5.4, 4.5, 10.2, 6.3), R('bedroom2' + s, 'bed', 0, 6.3, 3.6, 10.2), R('bathroom' + s, 'bath', 3.6, 6.3, 5.4, 8.4),
             R('linen' + s, 'store', 3.6, 8.4, 5.4, 10.2), R('master' + s, 'bed', 5.4, 6.3, 8.7, 10.2), R('ensuite' + s, 'bath', 8.7, 6.3, 10.2, 8.7),
             R('wardrobe' + s, 'store', 8.7, 8.7, 10.2, 10.2)]
    doors = [('living' + s, 'gallery', 1.0, 'door', 0.75, None, True), ('living' + s, 'hall' + s, 1.2, 'arch'), ('hall' + s, 'kitchen' + s, 0.9),
             ('kitchen' + s, 'store' + s, 0.8), ('living' + s, 'bathroom' + s, 0.75), ('living' + s, 'bedroom2' + s, 0.9, 'door', 0.8),
             ('bedroom2' + s, 'linen' + s, 0.75), ('hall' + s, 'master' + s, 0.9), ('master' + s, 'ensuite' + s, 0.75), ('master' + s, 'wardrobe' + s, 0.75)]
    return rooms, doors


def flat_interior():
    rooms, doors = flat_unit()
    rooms.append(R('gallery', 'open', 0, 0, 10.2, 1.5, no_columns=True))
    return dict(name='two_bedroom_flat', floors=[dict(z=0, rooms=rooms, doors=doors, rail_open=True)], party=[('v', 0.0), ('v', 10.2)])


def flat_block():
    floors = []
    for z in (0, 1):
        rooms, doors = [], []
        for i in range(3):
            rr, dd = flat_unit(f'{z}{i + 1}')
            for r in rr:
                x0, y0, x1, y1 = r['rect']; r['rect'] = (x0 + 10.2 * i, y0, x1 + 10.2 * i, y1)
            rooms += rr; doors += dd
        rooms.append(R('gallery', 'open', 0, 0, 30.6, 1.5, no_columns=(z == 1)))
        fl = dict(z=z, rooms=rooms, doors=doors)
        if z == 0:
            rooms.append(R('stair', 'stair_open', 12.0, -1.4, 15.8, 0.0, dir='+x', rails=['lo']))
            rooms.append(R('stairfoot', 'open', 15.8, -1.4, 16.6, 0.0, no_columns=True))
            fl['clear_pairs'] = [('stair', 'gallery'), ('stair', 'stairfoot'), ('stairfoot', 'gallery'), ('stair', None)]
        else:
            rooms.append(R('stairwell', 'void', 12.0, -1.4, 15.8, 0.0, outdoor=True))
            rooms.append(R('landing', 'open', 15.8, -1.4, 16.6, 0.0, no_columns=True))
            fl['clear_pairs'] = [('stairwell', 'landing'), ('landing', 'gallery')]
        floors.append(fl)
    return dict(name='flat_block', floors=floors, steps=[(0, 12.0, 0, '-y'), (16.6, 30.6, 0, '-y')], overhang=0.6)


# ---------------------------------------------------------------- bungalow (3 bedrooms)
def bungalow():
    rooms = [R('bedroom3', 'bed', 0, 0, 3.6, 3.6), R('veranda', 'open', 3.6, 0, 9.6, 2.4), R('master', 'bed', 9.6, 0, 13.8, 4.2),
             R('living', 'living', 3.6, 2.4, 9.6, 7.2), R('bathroom', 'bath', 0, 3.6, 3.6, 5.4), R('ensuite', 'bath', 9.6, 4.2, 12.0, 6.0),
             R('wardrobe', 'store', 12.0, 4.2, 13.8, 6.0), R('bedroom2', 'bed', 0, 5.4, 3.6, 9.0), R('laundry', 'store', 0, 9.0, 3.6, 10.2),
             R('dining', 'dining', 3.6, 7.2, 9.6, 10.2), R('kitchen', 'kitchen', 9.6, 6.0, 13.8, 10.2)]
    doors = [('living', 'veranda', 1.0, 'door', 0.5, None, True), ('living', 'bedroom3', 0.9), ('living', 'bathroom', 0.75), ('living', 'bedroom2', 0.9),
             ('living', 'master', 0.9), ('master', 'ensuite', 0.75), ('master', 'wardrobe', 0.75), ('living', 'dining', 1.8, 'arch'),
             ('dining', 'kitchen', 0.9), ('dining', 'laundry', 0.75), ('kitchen', 'out', 0.9, 'door', 0.5, 'back')]
    return dict(name='bungalow', floors=[dict(z=0, rooms=rooms, doors=doors)], steps=[(3.6, 9.6, 0, '-y')])


# ---------------------------------------------------------------- duplex (5 bedrooms incl. guest room)
def duplex():
    g = [R('porch', 'open', 4.2, -1.8, 7.8, 0), R('guest', 'bed', 0, 0, 4.2, 3.6), R('guest_bath', 'bath', 0, 3.6, 2.4, 5.4), R('wc', 'wc', 2.4, 3.6, 4.2, 5.4),
         R('hall', 'hall', 4.2, 0, 7.8, 5.4), R('living', 'living', 7.8, 0, 12.0, 5.4), R('corridor', 'corridor', 0, 5.4, 12.0, 6.6),
         R('kitchen', 'kitchen', 0, 6.6, 4.2, 10.2), R('store', 'store', 0, 10.2, 4.2, 12.0), R('stair', 'stair', 4.2, 6.6, 5.6, 11.0, dir='-y'),
         R('backhall', 'corridor', 4.2, 11.0, 5.6, 12.0), R('dining', 'dining', 5.6, 6.6, 12.0, 12.0)]
    gd = [('hall', 'porch', 1.2, 'door', 0.5, None, True), ('hall', 'guest', 0.9), ('guest', 'guest_bath', 0.75), ('hall', 'wc', 0.7),
          ('hall', 'living', 1.6, 'arch'), ('hall', 'corridor', 1.2, 'arch'), ('corridor', 'kitchen', 0.9), ('corridor', 'dining', 1.6, 'arch'),
          ('kitchen', 'store', 0.8), ('backhall', 'store', 0.8), ('backhall', 'dining', 0.8), ('backhall', 'out', 0.9, 'door', 0.5, 'back')]
    u = [R('balcony', 'open', 4.2, -1.8, 7.8, 0), R('bedroom2', 'bed', 0, 0, 4.2, 3.6), R('bath2', 'bath', 0, 3.6, 2.4, 5.4), R('linen', 'store', 2.4, 3.6, 4.2, 5.4),
         R('lounge', 'lounge', 4.2, 0, 7.8, 5.4), R('master', 'bed', 7.8, 0, 12.0, 3.6), R('master_bath', 'bath', 7.8, 3.6, 10.0, 5.4),
         R('dressing', 'store', 10.0, 3.6, 12.0, 5.4), R('corridor_up', 'corridor', 0, 5.4, 12.0, 6.6), R('bedroom3', 'bed', 0, 6.6, 4.2, 10.2),
         R('bath3', 'bath', 0, 10.2, 4.2, 12.0), R('stairwell', 'void', 4.2, 6.6, 5.6, 12.0), R('bedroom4', 'bed', 5.6, 6.6, 12.0, 10.2),
         R('bath4', 'bath', 5.6, 10.2, 8.0, 12.0), R('store4', 'store', 8.0, 10.2, 12.0, 12.0)]
    ud = [('lounge', 'balcony', 1.2), ('lounge', 'bedroom2', 0.9), ('bedroom2', 'bath2', 0.75), ('lounge', 'linen', 0.7), ('lounge', 'master', 0.9),
          ('master', 'master_bath', 0.75), ('master', 'dressing', 0.75), ('lounge', 'corridor_up', 1.2, 'arch'), ('corridor_up', 'bedroom3', 0.9),
          ('bedroom3', 'bath3', 0.75), ('corridor_up', 'bedroom4', 0.9), ('bedroom4', 'bath4', 0.75), ('bedroom4', 'store4', 0.75)]
    return dict(name='duplex', floors=[dict(z=0, rooms=g, doors=gd, open_pairs=[('backhall', 'stair')]),
                                       dict(z=1, rooms=u, doors=ud, clear_pairs=[('corridor_up', 'stairwell')])],
                stair_links=[((0, 'stair'), (1, 'corridor_up'))], steps=[(4.2, 7.8, -1.8, '-y')])


# ---------------------------------------------------------------- mansion (5 bedrooms upstairs)
def mansion():
    g = [R('portico', 'open', 6, -2.4, 12, 0), R('study', 'study', 0, 0, 4.2, 5.4), R('wc', 'wc', 4.2, 0, 6, 2.4), R('cloak', 'store', 4.2, 2.4, 6, 5.4),
         R('foyer', 'hall', 6, 0, 12, 5.4, floor='f_granite'), R('living', 'living', 12, 0, 18, 5.4, floor='f_granite'),
         R('corridor', 'corridor', 0, 5.4, 18, 6.9, floor='f_granite'), R('kitchen', 'kitchen', 0, 6.9, 6, 11.4), R('pantry', 'store', 0, 11.4, 3, 13.8),
         R('laundry', 'store', 3, 11.4, 6, 13.8), R('stair', 'stair', 6, 6.9, 7.5, 11.4, dir='-y'), R('backhall', 'corridor', 6, 11.4, 7.5, 13.8),
         R('dining', 'dining', 7.5, 6.9, 12, 13.8, floor='f_granite'), R('family', 'family', 12, 6.9, 18, 13.8)]
    gd = [('foyer', 'portico', 1.6, 'door', 0.5, None, True), ('foyer', 'living', 2.0, 'arch'), ('foyer', 'wc', 0.75), ('corridor', 'cloak', 0.7),
          ('corridor', 'study', 0.9), ('foyer', 'corridor', 2.0, 'arch'), ('corridor', 'kitchen', 0.9), ('corridor', 'dining', 1.8, 'arch'),
          ('corridor', 'family', 1.2, 'arch'), ('corridor', 'living', 0.9), ('kitchen', 'pantry', 0.8), ('kitchen', 'laundry', 0.8),
          ('backhall', 'laundry', 0.8), ('backhall', 'dining', 0.8), ('backhall', 'out', 0.9, 'door', 0.5, 'back')]
    u = [R('balcony', 'open', 6, -2.4, 12, 0), R('bedroom2', 'bed', 0, 0, 4.2, 5.4), R('bath2', 'bath', 4.2, 0, 6, 2.7), R('wardrobe2', 'store', 4.2, 2.7, 6, 5.4),
         R('lounge', 'lounge', 6, 0, 12, 5.4), R('bedroom5', 'bed', 12, 0, 16.2, 5.4), R('bath5', 'bath', 16.2, 0, 18, 2.7),
         R('wardrobe5', 'store', 16.2, 2.7, 18, 5.4), R('corridor_up', 'corridor', 0, 5.4, 18, 6.9), R('bedroom3', 'bed', 0, 6.9, 6, 11.4),
         R('bath3', 'bath', 0, 11.4, 6, 13.8), R('stairwell', 'void', 6, 6.9, 7.5, 13.8), R('bedroom4', 'bed', 7.5, 6.9, 12, 11.4),
         R('bath4', 'bath', 7.5, 11.4, 12, 13.8), R('dressing', 'store', 12, 6.9, 15, 9.0), R('master_bath', 'bath', 15, 6.9, 18, 9.0),
         R('master', 'bed', 12, 9.0, 18, 13.8, floor='f_wood')]
    ud = [('lounge', 'balcony', 1.6), ('bedroom2', 'bath2', 0.75), ('bedroom2', 'wardrobe2', 0.75), ('corridor_up', 'bedroom2', 0.9),
          ('lounge', 'corridor_up', 2.0, 'arch'), ('corridor_up', 'bedroom5', 0.9), ('bedroom5', 'bath5', 0.75), ('bedroom5', 'wardrobe5', 0.75),
          ('corridor_up', 'bedroom3', 0.9), ('bedroom3', 'bath3', 0.75), ('corridor_up', 'bedroom4', 0.9), ('bedroom4', 'bath4', 0.75),
          ('corridor_up', 'dressing', 0.9), ('dressing', 'master', 0.9), ('master', 'master_bath', 0.75)]
    return dict(name='mansion', floors=[dict(z=0, rooms=g, doors=gd, open_pairs=[('backhall', 'stair')]),
                                        dict(z=1, rooms=u, doors=ud, clear_pairs=[('corridor_up', 'stairwell')])],
                stair_links=[((0, 'stair'), (1, 'corridor_up'))], steps=[(6, 12, -2.4, '-y')])


def boys_quarters():
    rooms = [R('bq_veranda', 'open', 0, 0, 8.4, 1.8), R('bq_room1', 'bed', 0, 1.8, 3.3, 5.4), R('bq_room2', 'bed', 3.3, 1.8, 6.6, 5.4),
             R('bq_bath', 'bath', 6.6, 1.8, 8.4, 5.4)]
    doors = [('bq_room1', 'bq_veranda', 0.9, 'door', 0.3, None, True), ('bq_room2', 'bq_veranda', 0.9, 'door', 0.3), ('bq_bath', 'bq_veranda', 0.75)]
    return dict(name='boys_quarters', prefix='bq_', floors=[dict(z=0, rooms=rooms, doors=doors)], steps=[(0, 8.4, 0, '-y')])


def gatehouse():
    return dict(name='gatehouse', prefix='gh_', floors=[dict(z=0, rooms=[R('gatehouse', 'study', 0, 0, 3.0, 3.0)],
                                                             doors=[('gatehouse', 'out', 0.9, 'door', 0.5, 'back', True)])])
