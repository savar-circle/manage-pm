import datetime
def etob(values):
    values = values.replace("0", "০")
    values = values.replace("1", "১")
    values = values.replace("2", "২")
    values = values.replace("3", "৩")
    values = values.replace("4", "৪")
    values = values.replace("5", "৫")
    values = values.replace("6", "৬")
    values = values.replace("7", "৭")
    values = values.replace("8", "৮")
    values = values.replace("9", "৯")
    return values

def dateformater(value):
    value = datetime.datetime.strptime(value, '%Y-%m-%d')
    value = value.strftime("%d/%m/%Y")
    return value

def year4to2(values):
    values = values.replace("/২০", "/")
    return values