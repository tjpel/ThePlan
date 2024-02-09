from datetime import datetime, timezone, timedelta
from google.cloud import firestore

today = datetime.now(tz=timezone(-timedelta(hours=6)))
yesterday = today - timedelta(days = 1)
yester2day = today - timedelta(days = 2)
monthago = today - timedelta(days = 30)

def dateToString(date: datetime) -> str:
    return date.strftime(r"%Y/%m/%d")  

def checkPreviousMH(client: firestore.Client,  level: int, max: int) -> bool:
    return len(client.collection('checkin') \
        .where('date', '<', dateToString(today)) \
        .where('date', '>=', dateToString(monthago)) \
        .where('rating', '==', level).get()) < max

def getRecentRow(client: firestore.Client, collection: str, check_today: bool = False, deleteOnToday: bool = False):
    conn = client.collection(collection)
    query = conn.order_by('date', direction=firestore.Query.DESCENDING)

    if check_today:
        data = query.limit(1).get()
    else:
        data = query.where('date', '>=', dateToString(yesterday)).limit(1).get()

    if deleteOnToday and data[0]._data["date"] == dateToString(today):
        data[0]._reference.delete()

    if len(data) == 0:
        return None
    else:
        return data[0]._data
    
def subtractExpenses(client: firestore.Client, cc, category, amount, notes):
    lastf = getRecentRow(client, 'finances', True, True)
    conn = client.collection('finances')

    if cc:
        acc = 'cc'
    elif category == 'Fun':
        acc = 'usfunsp'
    else:
        acc = 'usgensp'

    lastf[acc] -= amount
    lastf["date"] = dateToString(today)
    conn.add(lastf)

    client.collection('expenses').add({
        "date": dateToString(today),
        "category": category,
        "amount": amount,
        "account": acc,
        "notes": notes
    })

    if lastf['usfunsp'] < 0 and acc == 'usfunsp':
        return -5
    else:
        return 0
    
def pointsCalculation(client, points, gym_activity, mental_health):
    if gym_activity == "Stuck to The Plan":
        points += 3
    elif gym_activity == "Active, but not in line with The Plan":
        points += 1
    else:
        points += -2

    #check if bad mental health day
    if points < 0:
        if mental_health == 1 and checkPreviousMH(1, 1):
            points = 0
        elif mental_health == 2 and checkPreviousMH(2, 4):
            points = points // 2

    gbtYester = getRecentRow(client, 'points')
    client.collection('points').add({
        "date": dateToString(today),
        "todaysPoints": points,
        "culmPoints": gbtYester['culmPoints'] + points
        })
    return points



    