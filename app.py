import sys

from duck_donuts_nutrition import DuckDonutsNutrition


def show_usage():
    print('usage: python app.py [-c=custom_donut] [-f, --formatted]')


def start_duck_donuts_nutrition(args):
    if len(args) > 3:
        show_usage()
        return
    ddn = DuckDonutsNutrition()
    if len(args) == 3 and ('-f' in args or '--formatted' in args):
        if '-f' in args[1]:
            print(ddn.get_custom_donut_nutrition(args[2][3:], True))
        elif '-f' in args[2]:
            print(ddn.get_custom_donut_nutrition(args[1][3:], True))
        else:
            show_usage()
            return
    elif len(args) == 2 and '-c=' in args[1]:
        print(ddn.get_custom_donut_nutrition(args[1][3:], False))
    elif len(args) == 1:
        ddn.save_collection_nutritions_to_file(
            'data/generated/collection_nutritions.csv'
        )
    else:
        show_usage()


if __name__ == '__main__':
    start_duck_donuts_nutrition(sys.argv)
