from sqlite3 import connect,Row

database:str = "db/skills.db"

#function to retrieving data
def getprocess(sql:str,vals:list)->list:
    conn:any = None
    cursor:any = None
    data:list = []
    try:
        conn = connect(database)
        conn.row_factory = Row
        cursor = conn.cursor()
        cursor.execute(sql,vals)
        data = cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()
    return data
    
#function for putting,updating,deleting data 
def postprocess(sql:str,vals:list)->bool:
    conn:any = None
    cursor:any = None
    try:
        conn = connect(database)
        cursor = conn.cursor()
        cursor.execute(sql,vals)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()
    return True if cursor.rowcount>0 else False
    
#function to get all data from a table
def getall(table:str)->list:
    sql:str = f"SELECT * FROM `{table}`"
    return getprocess(sql,[])
    
#function to get a specific data from a table
def getrecord(table:str,**kwargs)->list:
    keys:list = list(kwargs.keys())
    vals:list = list(kwargs.values())
    flds:list = []
    for key in keys:
        flds.append("`"+key+"`=?")
    fld:str = " AND ".join(flds)
    sql:str = f"SELECT * FROM `{table}` WHERE {fld}"
    return getprocess(sql,vals)
    
#function for deleting data 
def deleterecord(table:str,**kwargs)->bool:
    keys:list = list(kwargs.keys())
    vals:list = list(kwargs.values())
    flds:list = []
    for key in keys:
        flds.append("`"+key+"`=?")
    fld:str = " AND ".join(flds)
    sql:str = f"DELETE FROM `{table}` WHERE {fld}"
    return postprocess(sql,vals)
    
#function for adding data 
def addrecord(table:str,**kwargs)->bool:
    #insert into `students`(`idno`,`name`,`course`,`level`) values(?,?,?,?)
    keys:list = list(kwargs.keys())
    vals:list = list(kwargs.values())
    q:list = len(keys)*'?'
    qmark:str = ",".join(q)
    flds:str = "`,`".join(keys)
    sql:str = f"INSERT INTO `{table}`(`{flds}`) VALUES({qmark})"
    return postprocess(sql,vals)
    
#function for updating data 
def updaterecord(table:str,**kwargs)->bool:
    
    keys:list = list(kwargs.keys())
    vals:list = list(kwargs.values())
    flds:list = []
    newvals:list = []
    for i in range(1,len(keys)):
        flds.append("`"+keys[i]+"`=?")
        newvals.append(vals[i])
    fld:str = ",".join(flds)
    sql:str = f"UPDATE `{table}` SET {fld} where `{keys[0]}`='{vals[0]}'"
    print(sql)
    return postprocess(sql,newvals)
 



