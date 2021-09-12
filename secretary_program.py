documents = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
]
directories = {
    '1': ['2207 876234', '11-2'],
    '2': ['10006'],
    '3': []
}


def main(documents, directories):
    """
        ap - (all people) - команда, которая выводит список всех владельцев документов
        p – (people) – команда, которая спросит номер документа и выведет имя человека, которому он принадлежит;
        l – (list) – команда, которая выведет список всех документов в формате passport "2207 876234" "Василий Гупкин";
        s – (shelf) – команда, которая спросит номер документа и выведет номер полки, на которой он находится;
        a – (add) – команда, которая добавит новый документ в каталог и в перечень полок, спросив его номер, тип,
        имя владельца и номер полки, на котором он будет храниться.
        d – (delete) – команда, которая спросит номер документа и удалит его из каталога и из перечня полок;
        m – (move) – команда, которая спросит номер документа и целевую полку и переместит его с текущей полки на целевую;
        as – (add shelf) – команда, которая спросит номер новой полки и добавит ее в перечень;
        q - (quit) - команда, которая завершает выполнение программы
        """
    print(
        'Вас приветствует программа помошник!\n',
        '(Введите help, для просмотра списка поддерживаемых команд)\n'
    )
    while True:
        user_input = input()

        if user_input == 'p':
            document_number = input('Введите номер документа ')
            people = search_document(documents, document_number)
            if people is not None:
                print(people['name'])
            else:
                print('Документ не найден')
        elif user_input == 'ap':
            print(get_owner_list(documents))
        elif user_input == 's':
            document_number = input('Введите номер документа ')
            directory_number = search_shelf_document(directories, document_number)
            if directory_number is not None:
                print(directory_number)
            else:
                print('Документ не найден')
        elif user_input == 'l':
            print_document_list(documents)
        elif user_input == 'a':
            new_document = input_document()
            add_document(directories, new_document, documents)
            print(documents)
            print(directories)
        elif user_input == 'd':
            delete_document(documents, directories)
            print(documents)
            print(directories)
        elif user_input == 'm':
            move(documents, directories)
            print(documents)
            print(directories)
        elif user_input == 'as':
            add_shelf(directories)
            print(documents)
            print(directories)
        elif user_input == 'help':
            print(main.__doc__)
        elif user_input == 'q':
            break


def get_owner_list(documents):
    owner_list = []
    for document in documents:
        try:
            owner = document.get('name')
            owner_list.append(owner)
        except KeyError:
            pass
    return owner_list


def search_document(documents, document_number):
    for document in documents:
        if document['number'] == document_number:
            return document


def search_shelf_document(directories, document_number):
    for directory, documents in directories.items():
        if document_number in documents:
            return directory


def print_document(document):
    print(f'{document["type"]} "{document["number"]}"  "{document["name"]}" ')


def input_document():
    new_document = {'type': '', 'number': '', 'name': ''}

    new_document['type'] = input('Введите тип документа ')
    new_document['number'] = input('Введите номер документа ')
    new_document['name'] = input('Введите имя владельца ')
    return new_document


def print_document_list(documents):
    for document in documents:
        print_document(document)


def add_document(directories, new_document, documents=None):
    while True:
        directory_number = input('Введите номер полки ')
        if directories.get(directory_number) is not None:
            directories[directory_number].append(new_document['number'])
            if documents is not None: documents.append(new_document)
            return True
        else:
            user_choose = input(
                'Введенная полка не сущетсвует. Если хотите создатm новую полку и добавить на нее документ, '
                'введите 1, чтобы изменить номер полки, введите другое, чтобы отменить добавление документа введите q ')
            if user_choose == '1':
                directories[directory_number] = [new_document['number']]
                if documents is not None: documents.append(new_document)
                return True
            elif user_choose == 'q':
                break


def delete_document(documents, directories):
    while True:
        document_number = input('Введите номер документа для удаления ')
        shelf_number = search_shelf_document(directories, document_number)
        if shelf_number is not None and document_number != 'stop':
            directories[shelf_number].remove(document_number)
            documents.remove(search_document(documents, document_number))
            break
        elif document_number == 'stop':
            break
        else:
            print('Документ с указанным номер не найден. Попробуйте еще раз')
            print('Для выхода введите "stop"')


def delete_document_from_shelf(directories, document_number):
    shelf_number = search_shelf_document(directories, document_number)
    if shelf_number is not None:
        directories[shelf_number].remove(document_number)


def move(documents, directories):
    document_number = input('Введите номер документа ')
    document = search_document(documents, document_number)
    if document is not None:
        if add_document(directories, document):
            delete_document_from_shelf(directories, document_number)


def add_shelf(directories):
    while True:
        new_shelf_number = input("Введите номер новой полки ")
        if new_shelf_number not in directories.keys():
            directories[new_shelf_number] = []
            break
        else:
            print("Полка с таким номером уже существует")
            print("если хотите ввести другой номер полки, введите 1")
            print("если хотите выйти в главное меню, введите 0")
            user_input = input()
            if user_input == '1':
                continue
            elif user_input == '0':
                break


if __name__ == '__main__':
    main(documents, directories)
