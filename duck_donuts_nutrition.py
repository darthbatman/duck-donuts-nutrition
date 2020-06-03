'''
Duck Donuts Nutrition
Author: Rishi Masand
Year: 2020
'''

import numpy as np

from donuts.collections import *
from donuts.components import *
from donuts.replacements import *
from utils import *


class DuckDonutsNutrition():
    '''
    Duck Donuts Nutrition

    Calculates nutrition facts for Duck Donuts donuts and donut collections
    '''

    def __init__(self):
        self._nutrition_data_file = 'data/obtained/nutrition_info.txt'

    def _add_nutrition_values(self, n1, n2):
        '''
        Adds nutrition dictionaries n1 and n2 by key-wise values
            and stores sum in n1
        '''
        for key in n1:
            if key in n2:
                n1_val = float(n1[key][:first_non_num_idx(n1[key])])
                n2_val = float(n2[key][:first_non_num_idx(n2[key])])
                unit = n1[key][first_non_num_idx(n1[key]):]
                n1[key] = str(n1_val + n2_val) + unit
        return n1

    def _get_sanitized_line(self, line):
        '''
        Sanitizes data file line
        '''
        return line.replace('<', '').replace('**', '0')

    def _get_item_from_line(self, line):
        '''
        Gets item from data file line
        '''
        idx = first_num_idx(line)
        return line[:idx].replace(' - ', ' ').strip()

    def _get_units_from_line(self, line):
        '''
        Gets units from data file line
        '''
        idx = first_num_idx(line)
        values = line[idx:].split()
        units = [v[first_non_num_idx(v):] for v in values]
        return units

    def _get_values_from_line(self, line):
        '''
        Gets values from data file line
        '''
        idx = first_num_idx(line)
        values = line[idx:].split()
        values = [float(v[:first_non_num_idx(v)]) for v in values]
        return values

    def _get_item_nutritions(self):
        '''
        Gets item nutrition facts from nutrition data file
        '''
        with open(self._nutrition_data_file, 'r') as f:
            item_nutritions = {}
            fields = f.readline()[:-1].split()[1:]
            units = None
            line = f.readline()[:-1]
            while line:
                if len(line) > 100:
                    line = f.readline()[:-1]
                    continue
                line = self._get_sanitized_line(line)
                item = self._get_item_from_line(line)
                if not units:
                    units = self._get_units_from_line(line)
                values = self._get_values_from_line(line)
                item_nutritions[item.lower()] = values
                line = f.readline()[:-1]
            f.close()
        return item_nutritions, fields, units

    def _get_well_formatted_donut_nutrition(self, donut, item_nutritions,
                                            fields, units):
        '''
        Gets nutrition facts from donut that is in order summary format
            order summary format: "A, B, C", where
                A = bare/glazed/icing selection
                B = topping selection
                C = drizzle selection
        '''
        nutrition = item_nutritions['donut (bare)']
        components = donut.lower().split(', ')
        for component in components:
            if component == 'glazed':
                nutrition = item_nutritions['donut glazed']
                continue
            elif component == 'bare':
                continue
            elif component in item_nutritions:
                nutrition += np.array(item_nutritions[component])
                continue
            elif component == components[-1]:
                component = component + ' drizzle'
            if component in item_nutritions:
                nutrition += np.array(item_nutritions[component])
            elif component in REPLACEMENTS and \
                    REPLACEMENTS[component] in item_nutritions:
                nutrition += np.array(item_nutritions[REPLACEMENTS[component]])
        return {fields[i]: str(v) + units[i] for i, v in enumerate(nutrition)}

    def _sanitize_ill_formatted_donut(self, donut):
        '''
        Sanitizes ill-formatted donut
        '''
        if ' - ' in donut:
            donut = donut.split(' - ')[1]
        if ': ' in donut:
            donut = donut.split(': ')[1]
        donut = donut.replace(' w/ ', ' with ').replace(', and ', ' with ') \
            .replace(', ', ' with ').replace(' and ', ' with ') \
            .replace(' & ', ' with ')
        return donut

    def _get_ill_formatted_donut_components(self, donut):
        '''
        Gets components from ill-formatted donut
        '''
        return donut.lower().split(' with ')

    def _get_base_nutrition(self, fields):
        '''
        Gets base (zeroed) nutrition facts
        '''
        return np.array([0 for _ in fields]).astype(float)

    def _get_ill_formatted_donut_nutrition(self, donut, item_nutritions,
                                           fields, units):
        '''
        Gets nutrition facts from donuts in arbitrary format
        '''
        donut = self._sanitize_ill_formatted_donut(donut)
        components = self._get_ill_formatted_donut_components(donut)
        nutrition = self._get_base_nutrition(fields)
        found_donut_type = False
        while components:
            component = components[0]
            if component in item_nutritions:
                if 'donut' in component:
                    found_donut_type = True
                nutrition += np.array(item_nutritions[component])
            elif component in REPLACEMENTS:
                replacement = REPLACEMENTS[component]
                if 'donut' in replacement:
                    found_donut_type = True
                nutrition += np.array(item_nutritions[replacement])
            elif ' '.join(component.split()[1:]) in item_nutritions:
                reformatted = ' '.join(component.split()[1:])
                nutrition += np.array(item_nutritions[reformatted])
            elif component.split()[0] in item_nutritions:
                nutrition += np.array(item_nutritions[component.split()[0]])
            elif component == components[-1]:
                component = component + ' drizzle'
                if component in item_nutritions:
                    nutrition += np.array(item_nutritions[component])
                elif component in REPLACEMENTS:
                    replacement = REPLACEMENTS[component]
                    nutrition += np.array(item_nutritions[replacement])
            components = components[1:]
        if not found_donut_type:
            nutrition += np.array(item_nutritions['donut (bare)'])
        return {fields[i]: str(v) + units[i] for i, v in enumerate(nutrition)}

    def _get_collection_nutrition(self, collection, item_nutritions,
                                  fields, units):
        '''
        Gets nutrition facts for collection of donuts
        '''
        collection_nutrition = {}
        for donut in collection:
            nutrition = self._get_ill_formatted_donut_nutrition(
                donut, item_nutritions, fields, units
            )
            collection_nutrition[donut] = nutrition
            if 'Total' in collection_nutrition:
                collection_nutrition['Total'] = \
                    self._add_nutrition_values(
                        collection_nutrition['Total'], nutrition
                    )
            else:
                collection_nutrition['Total'] = dict(nutrition)

        return collection_nutrition

    def _format_collection_nutrition(self, collection, collection_nutrition):
        '''
        Format nutrition facts for collection of donuts for writing to file
        '''
        formatted_str = COLLECTION_NAMES[tuple(collection)] + ','
        for n_key in collection_nutrition['Total']:
            formatted_str += collection_nutrition['Total'][n_key] + ','
        formatted_str = formatted_str[:-1]
        formatted_str += '\n'
        del collection_nutrition['Total']
        for donut in collection_nutrition:
            formatted_str += donut.replace(',', '') + ','
            for n_key in collection_nutrition[donut]:
                formatted_str += collection_nutrition[donut][n_key] + ','
            formatted_str = formatted_str[:-1]
            formatted_str += '\n'
        return formatted_str

    def save_collection_nutritions_to_file(self, file):
        '''
        Saves nutrition facts for collection of donuts to file
        '''
        item_nutritions, fields, units = self._get_item_nutritions()
        data = 'Item,' + ','.join(fields) + '\n'
        for collection in FEATURED_COLLECTIONS:
            collection_nutrition = self._get_collection_nutrition(
                collection, item_nutritions, fields, units)
            data += self._format_collection_nutrition(
                collection, collection_nutrition)
        with open(file, 'w') as f:
            f.write(data)
            f.close()

    def get_custom_donut_nutrition(self, donut, well_formatted=False):
        '''
        Gets nutrition facts for custom donuts
        '''
        item_nutritions, fields, units = self._get_item_nutritions()
        if well_formatted:
            return self._get_well_formatted_donut_nutrition(
                donut, item_nutritions, fields, units)
        return self._get_ill_formatted_donut_nutrition(
            donut, item_nutritions, fields, units)
