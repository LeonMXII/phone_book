import csv
import re

def open_file(file):
    with open(file, encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts = list(rows)
    return contacts

def sorted_name(contacts):
    full_contacts = []
    for name in contacts:
        pattern = r'[\s,]'
        fio = (re.split(pattern, ' '.join(name[:3])))[:3]
        info = name[3:]
        name = fio + info
        full_contacts.append(name)
    return full_contacts

def sorted_phone(contacts):
    full_contacts = []
    for phone in contacts:
        pattern = r'(\+7|8)?\s*\(?(\d{3})\)?\-?\s*(\d{3})\-?'\
                r'(\d{2})\-?(\d+)(\s*)\(*([доб.]*)?\s*(\d{4})?\)*'
        phones = re.search(pattern, phone[-2])
        if phones is not None:
            result = re.sub(pattern, r'+7(\2)\3-\4-\5\6\7\8', phone[-2])
            phone[-2] = result
        full_contacts.append(phone)
    return full_contacts

def double_contacts(contacts):
    contacts_d = []
    for i in contacts:
        pattern = ', '.join([i[0], (i[1])])
        index = contacts.index(i) + 1
        for e in contacts[index:]:
            final_name = ', '.join([e[0], (e[1])])
            result = re.search(pattern, final_name)
            if result is not None:
                if i[2] == '':
                    i[2] = e[2]
                if i[3] == '':
                    i[3] = e[3]
                if i[4] == '':
                    i[4] = e[4]
                if i[5] == '':
                    i[5] = e[5]
                if i[6] == '':
                    i[6] = e[6]
                contacts_d.append(e)
    full_contacts = [i for i in contacts if i not in contacts_d]
    return full_contacts


def save_file(contacts):
    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts)


if __name__ == "__main__":
    phonebook = open_file("phonebook_raw.csv")
    phonebook = sorted_name(phonebook)
    phonebook = sorted_phone(phonebook)
    phonebook = double_contacts(phonebook)
    save_file(phonebook)


