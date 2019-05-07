import numpy as np

def ChangeDateFormat(name):
    
    months = ("Январь","Февраль","Март","Апрель","Май","Июнь","Июль","Август","Сентябрь","Октябрь","Ноябрь","Декабрь")
    day, mon, year = name.split(" ")
    if mon not in months:
        print("mon = ", mon)
    else:
        mon = months.index(mon)+1
    
    return f"{day}-0{mon}-{year}" if int(mon) < 10 else f"{day}-{mon}-{year}"

def TimeToSeconds(time):
    hours, mins, secs = map(lambda x: int(x), time.split(':'))
    return hours*3600+mins*60+secs

def TimeToCategory(time, part = (0, 30, 0), numCategories = None):
    hours, minutes, seconds = map(lambda x: int(x), time.split(':'))
    if hours >= 24 or minutes >= 60 or seconds >= 60:
        raise ValueError("Wrong time type!")
    hours -= 8
    
    seconds += hours*3600+minutes*60
    
    perCategory = (12/numCategories)*60*60 if part is None else part[0]*3600+part[1]*60+part[2]
    
    category = seconds // perCategory
    
    return category+1

def ToCategory(category, categories):
    
    if category not in categories:
        print("category = ", category)
    else:
        category = categories.index(category)
        
    return category

def Augmentation(count, year_start=2000, year_end = 2019, month_start = 1, month_end = 12, day_start = 1, day_end = 31,
                 times = 48,
                 waiting = 1800, 
                 servicing = 5400,
                 services = 5,
                 operators = 30,
                 point_services = 19,
                 events = 3):
    def checkDigit(start, end, bound_left, bound_right):
        if start < bound_left:
            start = bound_left
        elif start > bound_right:
            start = bound_right
        if end < bound_left:
            end = bound_left
        elif end < start:
            if start < bound_right: end = start + 1
            else: end = bound_right
        elif end > bound_right:
            end = bound_right
        return start, end
    
    month_start, month_end = checkDigit(month_start, month_end, 1, 12)
    day_start, day_end = checkDigit(day_start, day_end, 1, 31)
    
    newData = {"Дата": [f"{np.random.randint(year_start, year_end+1)}-{np.random.randint(month_start, month_end)}-{np.random.randint(day_start, day_end)}" for _ in range(count)],
               #"Дата": [f"{np.random.randint(2000, 2020)}-{4}-{np.random.randint(27, 32)}" for _ in range(count)],
               "Время выдачи": [np.random.randint(1, times+1) for _ in range(count)],
               "Время завершения":[],
               "Длительность ожидания":[np.random.randint(0,waiting+1) for _ in range(count)],
               "Длительность обслуживания":[np.random.randint(0, servicing+1) for _ in range(count)],
               "Длительность нахождения в очереди":[],
               "Услуга":[np.random.randint(0, services+1) for _ in range(count)],
               "Оператор":[np.random.randint(0, operators+1) for _ in range(count)],
               "Точка обслуживания":[np.random.randint(0, point_services+1) for _ in range(count)],
               "Последнее событие":[np.random.randint(0, events+1) for _ in range(count)]}
    
    for i in range(len(newData["Дата"])):
        date = newData["Дата"][i]
        year, month, day = map(lambda x: int(x), date.split("-"))
        if day == 31 and month in (2, 4, 6, 9, 11):
            day -= 1
            if month == 2:
                day -= 2
        elif day > 28 and month == 2: day -= 2
        
        newData["Дата"][i]= f"{year}-{month}-{day}"
        
    newData["Время завершения"] = [np.random.randint(i, 49) for i in newData["Время выдачи"]]
    newData["Длительность нахождения в очереди"] = [wait+service for wait,service in zip(newData["Длительность ожидания"], newData["Длительность обслуживания"])]

    return newData