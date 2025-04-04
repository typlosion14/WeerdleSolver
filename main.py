import json
import tkinter as tk
from tkinter import ttk

import pandas
import math

root = tk.Tk()

df = pandas.read_csv('pokemon.csv')
df = df.loc[:, df.columns.intersection(['name', 'height_m', 'pokedex_number', 'type1', 'type2', 'weight_kg'])]
seismitoad = df['name'].isin(['Seismitoad'])
pokemonIndex = [df[seismitoad]]
informationIndex = []
greaterSymbol = ['v']  # , 'g', 'h'
lowerSymbol = ['∧']  # , 'l', 'b'
equalSymbol = ['=']  # , 'e'
acceptedSymbol = greaterSymbol + lowerSymbol + equalSymbol
type1 = ['height_m', 'pokedex_number', 'weight_kg']
type2 = ['type1', 'type2']
okSymbol = ['=']  # , 'k', 'ok', 'e'
noSymbol = ['≠']  # , 'k', 'ok', 'e'
elseWhere = ['↹']  # , 'or'
typeSymbol = okSymbol + noSymbol + elseWhere


def showHelp():
    print('Pour signifier plus elevé, vous pouvez utiliser:' + str(greaterSymbol))
    print('Pour signifier moins elevé, vous pouvez utiliser:' + str(lowerSymbol))
    print('Pour signifier equal, vous pouvez utiliser:' + str(equalSymbol))
    print('Pour signifier ok pour les types, vous pouvez utiliser:' + str(okSymbol))
    print('Pour signifier non pour les types, vous pouvez utiliser:' + str(noSymbol))
    print('Pour signifier autre part pour les types, vous pouvez utiliser:' + str(elseWhere))


def waitingInput(error=False, typeRq='pokedex_number'):
    if type1.count(typeRq):
        if error:
            answer = input('Vous ne pouvez utilisez que:' + str(acceptedSymbol))
        else:
            answer = input()
        if acceptedSymbol.count(answer) != 1:
            return waitingInput(True, typeRq)
    else:
        if error:
            answer = input('Vous ne pouvez utilisez que:' + str(typeSymbol))
        else:
            answer = input()
        if typeSymbol.count(answer) != 1:
            return waitingInput(True, typeRq)
    return answer


def checkIfValueIsPossible():
    return "TODO"


def getBestStat(typeRQ, greater=True):
    equalInformation = list(filter(lambda x: x[typeRQ] in equalSymbol, informationIndex))
    if len(equalInformation) != 0:
        return pokemonIndex[equalInformation[0]['dataID']].iloc[0][typeRQ].item()

    reseachedSymbol = greaterSymbol if greater else lowerSymbol
    filteredInformation = list(filter(lambda x: x[typeRQ] in reseachedSymbol, informationIndex))
    pokemonArray = []
    for data in filteredInformation:
        pokemonArray.append(pokemonIndex[data['dataID']].iloc[0][typeRQ])
    if len(pokemonArray) != 0:
        sortedInformation = sorted(pokemonArray, key=lambda x: x, reverse=not greater)
        return sortedInformation[0].item()
    else:
        greaterData = {
            'pokedex_number': 1026,
            'weight_kg': 1000,
            'height_m': 21,
        }
        lowerData = {
            'pokedex_number': 0,
            'weight_kg': 0,
            'height_m': 0,
        }
        return greaterData[typeRQ] if greater else lowerData[typeRQ]


def getType(typeRQ='type1'):
    otherTypeNB = 'type1' if typeRQ == 'type2' else 'type2'

    equalInformation = list(filter(lambda x: x[typeRQ] in okSymbol, informationIndex))
    if len(equalInformation) != 0:
        return pokemonIndex[equalInformation[0]['dataID']].iloc[0][typeRQ]

    elseWhereInformation = list(
        filter(lambda x: x[otherTypeNB] in elseWhere, informationIndex))

    if len(elseWhereInformation) != 0:
        return pokemonIndex[elseWhereInformation[0]['dataID']].iloc[0][otherTypeNB]

    return ''


def getNotType():
    typeList = []
    noInformation1 = list(filter(lambda x: x['type1'] in noSymbol, informationIndex))
    if len(noInformation1) != 0:
        for data in noInformation1:
            typeList.append(pokemonIndex[data['dataID']].iloc[0]['type1'])

    noInformation2 = list(filter(lambda x: x['type2'] in noSymbol, informationIndex))
    if len(noInformation2) != 0:
        for data in noInformation2:
            typeList.append(pokemonIndex[data['dataID']].iloc[0]['type2'])

    return list(set(typeList))


def getStats():
    data = {
        'greater_index': getBestStat('pokedex_number'),
        'lower_index': getBestStat('pokedex_number', False),
        'greater_weight': getBestStat('weight_kg'),
        'lower_weight': getBestStat('weight_kg', False),
        'greater_height': getBestStat('height_m'),
        'lower_height': getBestStat('height_m', False),
        'typeisnot': getNotType(),
        'type1': getType(),
        'type2': getType('type2')
    }
    return data


def getPokemonNameList(pokemonList):
    nameList = []
    for pkdexnb, pkm in pokemonList.iterrows():
        nameList.append(pkm['name'])
    return nameList


def getPossiblePokemonList():
    data = getStats()
    # if data['lower_index'] != data['greater_index']:
    #     pokemonPossible = df.query(
    #         "pokedex_number > " + str(data['lower_index']) + " & pokedex_number < " + str(data['greater_index'])
    #     )
    # else:
    #     pokemonPossible = df.query(
    #         "pokedex_number == " + str(data['lower_index']) + " & pokedex_number == " + str(data['greater_index'])
    #     )

    pokemonPossible = df.query(
        "pokedex_number > " + str(data['lower_index']) + " & pokedex_number < " + str(data['greater_index'])
    )
    if data['lower_height'] != data['greater_height']:
        pokemonPossible = pokemonPossible.query(
            "height_m > " + str(data['lower_height']) + " & height_m < " + str(data['greater_height'])
        )
    else:
        pokemonPossible = pokemonPossible.query(
            "height_m == " + str(data['lower_height']) + " & height_m == " + str(data['greater_height'])
        )
    if data['lower_weight'] != data['greater_weight']:
        pokemonPossible = pokemonPossible.query(
            "weight_kg > " + str(data['lower_weight']) + " & weight_kg < " + str(data['greater_weight'])
        )
    else:
        pokemonPossible = pokemonPossible.query(
            "weight_kg == " + str(data['lower_weight']) + " & weight_kg == " + str(data['greater_weight'])
        )
    if data['type1'] != '':
        pokemonPossible = pokemonPossible.loc[pokemonPossible['type1'] == data['type1']]
    else:
        pokemonPossible = pokemonPossible.loc[~pokemonPossible['type1'].isin(data['typeisnot'])]

    if data['type2'] != '':
        pokemonPossible = pokemonPossible.loc[pokemonPossible['type2'] == data['type2']]
    else:
        pokemonPossible = pokemonPossible.loc[~pokemonPossible['type2'].isin(data['typeisnot'])]
    return pokemonPossible


def askInformation():
    pokeName = pokemonIndex[len(pokemonIndex) - 1].iloc[0]['name']
    print('Comment est l\'index de ' + pokeName + ' par rapport au pokemon secret ?')
    data = {'dataID': len(informationIndex), 'pokedex_number': waitingInput(), 'height_m': None, 'weight_kg': None,
            'type1': None,
            'type2': None}
    print('Comment est la taille de ' + pokeName + ' par rapport au pokemon secret ?')
    data['height_m'] = waitingInput(typeRq='height_m')
    print('Comment est le poids de ' + pokeName + ' par rapport au pokemon secret ?')
    data['weight_kg'] = waitingInput(typeRq='weight_kg')
    print('Comment est le 1er type de ' + pokeName + ' par rapport au pokemon secret ?')
    data['type1'] = waitingInput(typeRq='type1')
    print('Comment est le 2ème type de ' + pokeName + ' par rapport au pokemon secret ?')
    data['type2'] = waitingInput(typeRq='type2')
    informationIndex.append(data)


def chooseAPokemon():
    pokemonList = scorringListPokemon(getPossiblePokemonList())
    print('Pokemon Suggéré:\n', pokemonList.sort_values(by=['score']).iloc[0])


def scorringPokemon(pkm, base_score):
    stats = getStats()
    score = base_score * 10
    if stats['lower_weight'] != stats['greater_weight']:
        score = score + abs((stats['greater_weight'] * 10 - stats['lower_weight'] * 10) - pkm['weight_kg'] * 10)
    if stats['lower_height'] != stats['greater_height']:
        score = score + abs((stats['greater_height'] * 10 - stats['lower_height'] * 10) - pkm['height_m'] * 10)
    return score


def scorringListPokemon(pokemonList):
    pokemonList['score'] = 0
    pos = 0
    for pkdexnb, pkm in pokemonList.iterrows():
        base_score = abs((math.ceil(len(pokemonList) / 2)) - pos)
        pokemonList.at[pkdexnb, 'score'] = scorringPokemon(pkm, base_score)
        pos += 1
    return pokemonList


def manualMode():
    data = {'dataID': 0, 'pokedex_number': '∧', 'height_m': '∧', 'weight_kg': 'v', 'type1': 'n', 'type2': 'n'}
    informationIndex.append(data)

    data2 = {'dataID': 1, 'pokedex_number': '<', 'height_m': '<', 'weight_kg': '>', 'type1': 'n', 'type2': 'n'}
    informationIndex.append(data2)
    pokemonIndex.append(df[df['name'] == 'Aegislash'])

    data3 = {'dataID': 2, 'pokedex_number': '<', 'height_m': '>', 'weight_kg': '>', 'type1': 'n', 'type2': 'n'}
    informationIndex.append(data3)
    pokemonIndex.append(df[df['name'] == 'Tapu Bulu'])

    # data4 = {'dataID': 3, 'pokedex_number': '<', 'height_m': '>', 'weight_kg': '>', 'type1': 'o', 'type2': 'n'}
    # informationIndex.append(data4)
    # pokemonIndex.append(df[df['name'] == 'Skuntank'])

    chooseAPokemon()


def automaticMode():
    askInformation()
    pkmList = getPossiblePokemonList()
    print('Pokemon Possibles \n', pkmList)
    pkmSuggest = pkmList.iloc[math.ceil(len(pkmList) / 2)]
    print('Pokemon Suggéré\n', pkmSuggest)
    pokemonIndex.append(df[df['name'] == pkmSuggest['name']])
    while len(getPossiblePokemonList()) > 1:
        askInformation()
        pkmList = getPossiblePokemonList()
        print('Pokemon Possibles \n', pkmList)
        pkmSuggest = pkmList.iloc[math.ceil(len(pkmList) / 2)]

        print('Pokemon Suggéré\n', pkmSuggest)
        pokemonIndex.append(df[df['name'] == pkmSuggest['name']])


# manualMode()
#automaticMode()

def reset():
    pokemonIndex.clear()
    informationIndex.clear()
    pokemonIndex.append(df[seismitoad])
    global current_data
    current_data = {'dataID': 0, 'pokedex_number': False, 'height_m': False, 'weight_kg': False, 'type1': False,
                    'type2': False}
    global root
    root.destroy()
    root = tk.Tk()
    showWindow()


bypassOBJ = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]


def showWindow():
    # Afficher un tableau avec Pokemon NumberPokedex Poids Taille Type1 Type2
    #                          DropdownPkm Dropdown1 Dropdown1 Dropdown1 Dropdown2 Dropdown2
    # AutoRefresh la liste DropdownPkm mais verrouille les anciennes dropdownPkm
    # Bouton reset qui remet Seismitoad et vide les autres lignes
    root.title('Weerdle Solver')

    pkmlb = tk.Label(root, text="Pokemon")
    pkmlb.grid(column=0, row=0)

    pkdxlb = tk.Label(root, text="Pokedex Nb")
    pkdxlb.grid(column=1, row=0)

    htlb = tk.Label(root, text="Height")
    htlb.grid(column=2, row=0)

    wtlb = tk.Label(root, text="Weight")
    wtlb.grid(column=3, row=0)

    t1lb = tk.Label(root, text="Type 1")
    t1lb.grid(column=4, row=0)

    t2lb = tk.Label(root, text="Type 2")
    t2lb.grid(column=5, row=0)

    resetButton = tk.Button(root, text="Reset", command=reset)
    resetButton.grid(column=3, row=6)

    cbpkm1 = ttk.Combobox(root, textvariable=bypassOBJ[0], state='disabled')
    cbpkm1['values'] = getPokemonNameList(df)
    cbpkm1.current(536)
    cbpkm1.grid(column=0, row=1)

    pkdxNb1 = tk.StringVar()
    cbpkdx1 = ttk.Combobox(root, textvariable=pkdxNb1, state='readonly')
    cbpkdx1['values'] = acceptedSymbol
    cbpkdx1.bind('<<ComboboxSelected>>', lambda event: statsChoice(event, cbpkdx1, "pokedex_number"))
    cbpkdx1.grid(column=1, row=1)

    height1 = tk.StringVar()
    heightcb1 = ttk.Combobox(root, textvariable=height1, state='readonly')
    heightcb1['values'] = acceptedSymbol
    heightcb1.bind('<<ComboboxSelected>>', lambda event: statsChoice(event, heightcb1, "height_m"))
    heightcb1.grid(column=2, row=1)

    weight1 = tk.StringVar()
    weightcb1 = ttk.Combobox(root, textvariable=weight1, state='readonly')
    weightcb1['values'] = acceptedSymbol
    weightcb1.bind('<<ComboboxSelected>>', lambda event: statsChoice(event, weightcb1, "weight_kg"))
    weightcb1.grid(column=3, row=1)

    type1txt1 = tk.StringVar()
    t1cb1 = ttk.Combobox(root, textvariable=type1txt1, state='readonly')
    t1cb1['values'] = typeSymbol
    t1cb1.bind('<<ComboboxSelected>>', lambda event: statsChoice(event, t1cb1, "type1"))
    t1cb1.grid(column=4, row=1)

    type2txt1 = tk.StringVar()
    t2cb1 = ttk.Combobox(root, textvariable=type2txt1, state='readonly')
    t2cb1['values'] = typeSymbol
    t2cb1.bind('<<ComboboxSelected>>', lambda event: statsChoice(event, t2cb1, "type2"))
    t2cb1.grid(column=5, row=1)

    tk.mainloop()


current_data = {'dataID': 0, 'pokedex_number': False, 'height_m': False, 'weight_kg': False, 'type1': False,
                'type2': False}


def pkmChoice(event, combobox: ttk.Combobox):
    if current_data['dataID'] != 0:
        pokemonIndex.append(df[df['name'] == combobox.get()])


def checkStats():
    global current_data
    if current_data['pokedex_number'] and current_data['height_m'] and current_data['weight_kg'] and current_data[
        'type1'] and current_data['type2']:
        informationIndex.append(current_data)
        current_data = {'dataID': current_data['dataID'] + 1, 'pokedex_number': False, 'height_m': False,
                        'weight_kg': False, 'type1': False,
                        'type2': False}
        newLine(current_data['dataID'] + 1)


def statsChoice(event, combobox: ttk.Combobox, data_type):
    current_data[data_type] = combobox.get()
    checkStats()


def newLine(row):
    cbpkm2 = ttk.Combobox(root, textvariable=bypassOBJ[row - 1], state='disabled')
    cbpkm2['values'] = getPokemonNameList(scorringListPokemon(getPossiblePokemonList()).sort_values(by=['score']))
    cbpkm2.current(0)
    pkmChoice(None, cbpkm2)
    cbpkm2.grid(column=0, row=row)

    pkdxNb1 = tk.StringVar()
    cbpkdx1 = ttk.Combobox(root, textvariable=pkdxNb1, state='readonly')
    cbpkdx1['values'] = acceptedSymbol
    cbpkdx1.bind('<<ComboboxSelected>>', lambda event: statsChoice(event, cbpkdx1, "pokedex_number"))
    cbpkdx1.grid(column=1, row=row)

    height1 = tk.StringVar()
    heightcb1 = ttk.Combobox(root, textvariable=height1, state='readonly')
    heightcb1['values'] = acceptedSymbol
    heightcb1.bind('<<ComboboxSelected>>', lambda event: statsChoice(event, heightcb1, "height_m"))
    heightcb1.grid(column=2, row=row)

    weight1 = tk.StringVar()
    weightcb1 = ttk.Combobox(root, textvariable=weight1, state='readonly')
    weightcb1['values'] = acceptedSymbol
    weightcb1.bind('<<ComboboxSelected>>', lambda event: statsChoice(event, weightcb1, "weight_kg"))
    weightcb1.grid(column=3, row=row)

    type1txt1 = tk.StringVar()
    t1cb1 = ttk.Combobox(root, textvariable=type1txt1, state='readonly')
    t1cb1['values'] = typeSymbol
    t1cb1.bind('<<ComboboxSelected>>', lambda event: statsChoice(event, t1cb1, "type1"))
    t1cb1.grid(column=4, row=row)

    type2txt1 = tk.StringVar()
    t2cb1 = ttk.Combobox(root, textvariable=type2txt1, state='readonly')
    t2cb1['values'] = typeSymbol
    t2cb1.bind('<<ComboboxSelected>>', lambda event: statsChoice(event, t2cb1, "type2"))
    t2cb1.grid(column=5, row=row)


showWindow()
