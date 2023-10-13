import settings
from cashdeskapp.models import *
from bankapp.models import *
from accounts.models import *
from enterprise.models import *
import datetime

# status code
# 200 succes
# 201
# 300 success but some operation didn't run successfully
# 400 all operations failed successfully

code = {
    200: "succes",  
    201: "",  
    300: "success but some operation didn't run successfully",  
    400: "all operations failed successfully"
        }

def create_year():
    year = datetime.datetime.now().year
    model = Exercise.objects.create(year=year)
    model.save()
    if model.id != None:
        yr = model.year
        id = model.id
        status_code = 200
    else:
        yr = None 
        id = None 
        status_code = 400

    return {'year': yr, 'id': id, 'status_code': status_code, 'message': code[status_code]}
    
def create_month():
    x = {'Janvier': 1, 
         'Fevrier': 2, 
         'Mars': 3, 
         'Avril': 4, 
         'Mai': 5, 
         'Juin': 6, 
         'Juillet': 7, 
         'Aout': 8, 
         'Septembre': 9, 
         'Octobre': 10, 
         'Novembre': 11, 
         'Decembre': 12
         }
    
    created = []
    failed = []
    
    for k, v in x.items():
        m = Month.objects.create(number=v, name=k)
        m.save()
        if m.id != None:
            created.append[m.name]
        else:
            failed.append[m.name]
    
    if len(x) == len(created):
        status_code = 200
    elif 0 < len(x) < len(created):
        status_code = 300
    else:
        status_code = 400
    
    return {'id_list': created, 'status_code': status_code, 'message': code[status_code]}

def init_enterprise(name):
    ent = Enterprise.objects.create(name=name)
    ent.save()
    if ent.id != None:
        cd = CashDesk.objects.create(reference="caisse 001", enterprise=ent)
        cd.save()
        bk = BankAccount.objects.create(name="Bank 1", Enterprise=ent)
        bk.save()

        if bk.id and cd.id != None:
            status_code = 200
        if bk.id or cd.id == None:
            status_code = 300
        elif bk.id and cd.id == None:
            status_code = 400
        
        return {'status_code': status_code, 'message': code[status_code]}
    
    else:
        status_code = 400
        return {'status_code': status_code, "message": code[status_code], 'reason': 'Enterprise creation failed'}
        