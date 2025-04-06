
import pymorphy3
morph = pymorphy3.MorphAnalyzer()

INVERTED_INDEX_PATH = 'D:/Study/info-search/hw3/inverted_index.txt'

class Commands:
    AND = 'and'
    OR = 'or'
    NOT = 'not'
    R_BR = ')'
    L_BR = '('

def get_inverted_index():
    inverted_index = dict()
    with open(INVERTED_INDEX_PATH, 'r', encoding='utf-8') as file:
        lines = file.read().splitlines()
        for l in lines:
            inverted_index[l.split(" ", 1)[0]] = set(eval(l.split(" ", 1)[1]))
    return inverted_index


def search(query):
    expr = query.strip().split()
    inverted_index = get_inverted_index()
    result = Commands.L_BR
    for i, e in enumerate(expr):
        match e:
            case Commands.AND:
                result += ").intersection("
            case Commands.OR:
                result += ").union("
            case Commands.NOT:
                result += ").difference("
            case Commands.L_BR | Commands.R_BR:
                result += e
            case _:
                lemma = morph.parse(e)[0].normal_form
                if lemma in inverted_index.keys():
                    result += str(inverted_index[lemma])
                else:
                    result += "set()"
    return eval(result + Commands.R_BR)


if __name__ == "__main__":
    while True:
        print("Доступные операторы: " + Commands.AND + ", " + Commands.OR + ", " + Commands.NOT)
        query = input("Введите запрос: ").lower()
        if query == 'exit':
            exit()
        try:
            result = search(query)
            print(f'Найдено в {len(result)} файлах: {result}')
        except:
            print('Ошибка. Попробуйте снова')