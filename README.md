# duck-donuts-nutrition

![python (scoped)](https://img.shields.io/badge/python-%3E%3D3.7.6-brightgreen.svg)

## Description
`duck-donuts-nutrition` calculates nutrition data for Duck Donuts donuts and donut collections. `duck-donuts-nutrition` parses publicly available nutrition data provided by Duck Donuts to determine nutrition data for individual menu items.

Each donut is made up of a combination of menu items (e.g. glazes, toppings, etc.). Each donut's nutritional data is calculated by adding up each nutritional component for all of the donut's menu items. Each collection's nutritional data is calculated by adding up each nutritional component for all all of the collection's donuts.

The assortments currently reflected in the generated nutrition data are the Spring Assortment, Signature Assortment, OBX Originals, Duck Dozen, and the Classic Assortment.

## Usage

### Installation

Install the dependencies with the following command.

`pip install -r requirements.txt`

### Execution

To run `duck-donuts-nutrition`, use the following command.

`python app.py [-c=custom_donut] [-f, --formatted]`

where

`-c=custom_donut` specifies the text of the custom donut (optional, nutrition facts for all present collections written to CSV by default)

`-f, --formatted` specifies that the custom donut text is formatted in the format "bare/glazed/icing selection, topping selection, drizzle selection" (optional, only to be used with `-c`, assumes donut text is not in this form by default)

## Authors

* Rishi Masand

## Resources

[Duck Donuts Nutritional Data](https://www.duckdonuts.com/wp-content/uploads/2019/12/Duck-Donuts-Nutrition-Data.pdf?x80093) from Duck Donuts website
