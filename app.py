import numpy as np


# Featured Dozens


SPRING_ASSORTMENT = [
    'Maple Icing with Chopped Bacon',
    'Blueberry Pancake - Blueberry Icing with Maple Drizzle & Powdered Sugar',
    'Vanilla Icing with Oreo Cookie Pieces',
    'Strawberry Cheesecake - Strawberry Icing with Cream Cheese Drizzle',
    'Cinnamon Bun - Cinnamon Sugar with Vanilla Drizzle',
    'Sunrise - Lemon Icing with Rasberry Drizzle',
    'Candied Lime - Cinnamon Sugar with Key Lime Drizzle',
    'Key Lime Pie - Key Lime Icing with Graham Cracker Crumbs & Cream Cheese Drizzle',
    'Coconut Key Lime - Key Lime Icing with Shredded Coconut',
    'Glazed',
    'Chocolate Icing with Rainbow Sprinkles',
    'Powdered Sugar'
]

SIGNATURE_ASSORTMENT = [
    'Bacon in the Sun: Maple Icing with Chopped Bacon and Caramel Drizzle',
    'Beach Ball: Vanilla Icing with Chocolate Drizzle and Rainbow Sprinkles',
    'Peanut Butter Paradise: Peanut Butter Icing with Chocolate Drizzle',
    'Blueberry Pancake: Blueberry Icing with Maple Drizzle and Powdered Sugar',
    'The Boardwalk: Glazed with Oreo crumbles, Powdered Sugar, and Vanilla Drizzle',
    'Sunrise: Lemon Icing with Raspberry Drizzle',
    'French Toast: Maple Icing with Cinnamon Sugar and Powdered Sugar',
    'Smore\'s: Chocolate Icing with Marshmallow Drizzle and Graham Cracker Crumbs',
    'Sand Dollar: Vanilla Icing with Shredded Coconut and Powdered Sugar',
    'The Beach: Vanilla Icing and Cinnamon Sugar',
    'The Flip-Flop: Chocolate Icing and Vanilla Drizzle',
    'Coconut Island Bliss: Chocolate Icing with Peanuts and Shredded Coconut'
]

OBX_ORIGINALS = [
    'Glazed w/ Chocolate Sprinkles',
    'Strawberry Icing',
    'Bare',
    'Vanilla Icing',
    'Glazed',
    'Chocolate Icing w/ Rainbow Sprinkles',
    'Powdered Sugar',
    'Chocolate Icing w/ Peanuts',
    'Cinnamon Sugar',
    'Vanilla Icing w/ Shredded Coconut',
    'Chocolate Icing',
    'Strawberry Icing w/ Rainbow Sprinkles'
]

DUCK_DOZEN = [
    'Blueberry w/ Powdered Sugar',
    'Lemon Icing w/ Raspberry Drizzle',
    'Peanut Butter Icing w/ Chocolate Drizzle',
    'Chocolate icing w/ Vanilla Drizzle',
    'Maple Icing w/ Chopped Bacon',
    'Chocolate Icing w/ Rainbow Sprinkles',
    'Powdered Sugar',
    'Strawberry Icing w/ Powdered Sugar',
    'Cinnamon Sugar w/ Vanilla Icing',
    'Vanilla Icing w/ Oreo Crumbles',
    'Chocolate Icing w/ Graham Cracker Crumbs & Marshmallow Drizzle',
    'Vanilla Icing w/ Hot Fudge Drizzle'
]

CLASSIC_ASSORTMENT = [
    'Maple Icing with Chopped Bacon',
    'Vanilla Icing with Rainbow Sprinkles',
    'Chocolate Icing with Vanilla Drizzle',
    'Blueberry Icing with Powdered Sugar',
    'Peanut Butter Icing with Raspberry Drizzle',
    'Glazed with Peanuts',
    'Cinnamon Sugar',
    'Vanilla Icing with Oreo crumbles',
    'Powdered Sugar',
    'Chocolate Icing with Rainbow Sprinkles',
    'Chocolate Icing with Peanuts',
    'Strawberry Icing with Blackberry Drizzle'
]


FEATURED_ASSORTMENTS = [SPRING_ASSORTMENT, SIGNATURE_ASSORTMENT, OBX_ORIGINALS,
                        DUCK_DOZEN, CLASSIC_ASSORTMENT]


# Helpers


def first_num_idx(s):
    for i in range(len(s)):
        if s[i].isdigit():
            return i
    return -1


def first_non_num_idx(s):
    for i in range(len(s)):
        if not s[i].isdigit() and not s[i] == '.':
            return i
    return len(s)


# Methods


def add_nutrition_values(n1, n2):
    for key in n1:
        if key in n2:
            n1_val = float(n1[key][:first_non_num_idx(n1[key])])
            n2_val = float(n2[key][:first_non_num_idx(n2[key])])
            unit = n1[key][first_non_num_idx(n1[key]):]
            n1[key] = str(n1_val + n2_val) + unit
    return n1


def get_item_nutritions():
    file_name = 'data/obtained/nutrition_info.txt'
    with open(file_name, 'r') as f:
        item_nutritions = {}
        fields = f.readline()[:-1].split()[1:]
        units = None
        line = f.readline()[:-1]
        while line:
            if len(line) > 100:
                line = f.readline()[:-1]
                continue
            line = line.replace('<', '').replace('**', '0')
            idx = first_num_idx(line)
            item = line[:idx].replace(' - ', '').strip()
            values = line[idx:].split()
            if not units:
                units = [v[first_non_num_idx(v):] for v in values]
            values = [float(v[:first_non_num_idx(v)]) for v in values]
            if 'oreo' in item.lower():
                item = 'oreo'
            if 'glazed' in item.lower():
                item = 'glazed'
            item_nutritions[item.lower()] = values
            line = f.readline()[:-1]
        f.close()
    return item_nutritions, fields, units


def get_donut_nutrition(donut, item_nutritions, fields, units):
    if ' - ' in donut:
        donut = donut.split(' - ')[1]
    if ': ' in donut:
        donut = donut.split(': ')[1]
    donut = donut.replace(' w/ ', ' with ').replace(', ', ' with ').replace(' and ', ' with ')
    components = donut.lower().split(' with ')

    nutrition = np.array([0 for _ in fields]).astype(float)

    found_donut_type = False
    while components:
        if components[0] in item_nutritions:
            if 'donut' in components[0]:
                found_donut_type = True
            nutrition += np.array(item_nutritions[components[0]])
        elif ' '.join(components[0].split()[1:]) in item_nutritions:
            nutrition += np.array(item_nutritions[' '.join(components[0].split()[1:])])
        elif components[0].split()[0] in item_nutritions:
            nutrition += np.array(item_nutritions[components[0].split()[0]])
        components = components[1:]
    if not found_donut_type:
        nutrition += np.array(item_nutritions['donut (bare)'])

    return {fields[i]: str(v) + units[i] for i, v in enumerate(nutrition)}


def get_assortment_nutrition(assortment, item_nutritions, fields, units):
    assortment_nutrition = {}
    for donut in assortment:
        nutrition = get_donut_nutrition(donut,
                                        item_nutritions,
                                        fields, units)
        assortment_nutrition[donut] = nutrition
        if 'Total' in assortment_nutrition:
            assortment_nutrition['Total'] = add_nutrition_values(assortment_nutrition['Total'], nutrition)
        else:
            assortment_nutrition['Total'] = dict(nutrition)

    return assortment_nutrition


def format_assortment_nutrition(assortment, assortment_nutrition):
    assortment_names = {
        tuple(SPRING_ASSORTMENT): 'Spring Assortment',
        tuple(SIGNATURE_ASSORTMENT): 'Signature Assortment',
        tuple(OBX_ORIGINALS): 'OBX Originals',
        tuple(DUCK_DOZEN): 'Duck Dozen',
        tuple(CLASSIC_ASSORTMENT): 'Classic Assortment'
    }
    formatted_str = assortment_names[tuple(assortment)] + ','
    for n_key in assortment_nutrition['Total']:
        formatted_str += assortment_nutrition['Total'][n_key] + ','
    formatted_str = formatted_str[:-1]
    formatted_str += '\n'
    del assortment_nutrition['Total']
    for donut in assortment_nutrition:
        formatted_str += donut.replace(',', '') + ','
        for n_key in assortment_nutrition[donut]:
            formatted_str += assortment_nutrition[donut][n_key] + ','
        formatted_str = formatted_str[:-1]
        formatted_str += '\n'
    return formatted_str


def save_assortment_nutritions_to_file(file_name):
    item_nutritions, fields, units = get_item_nutritions()
    file_str = 'Item,' + ','.join(fields) + '\n'
    for assortment in FEATURED_ASSORTMENTS:
        assortment_nutrition = get_assortment_nutrition(assortment, item_nutritions, fields, units)
        file_str += format_assortment_nutrition(assortment, assortment_nutrition)
    with open(file_name, 'w') as f:
        f.write(file_str)
        f.close()


if __name__ == '__main__':
    save_assortment_nutritions_to_file('data/generated/assortment_nutritions.csv')
