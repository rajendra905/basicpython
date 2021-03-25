import mysql.connector
import datetime
from tabulate import tabulate

db=input("Enter name of your dtabase :")
mydb=mysql.connector.connect(host="localhost", user="root",passwd="rajendra")
mycursor=mydb.cursor()

sql="CREATE DATABASE if not exists %s" %(db,)
mycursor.execute(sql)
print("DATABASE create Successfully......")
mycursor=mydb.cursor()
mycursor.execute("Use "+db)

TableName=input("Name of Table to be created:")
query="Create table if not exists "+TableName+" \
(empno int primary key,\
name varchar(15) not null,\
job varchar(15),\
BasicSalary int,\
DA float,\
HRA float,\
GrossSalary float,\
Tax float,\
NetSalary float)"
print("Table "+TableName+ " Create Successfully.....")

mycursor.execute(query)

while True:
    print("\n\n\n")
    print("*"*100)
    print("\t\t\t\tMAIN MENU")
    print("*"*100)
    print("\t\t\t\t1. Adding Employee records")
    print("\t\t\t\t2. For Displaying record all the Employee")
    print("\t\t\t\t3. For Displaying record of a particular the Employee")
    print("\t\t\t\t4. For Deleting record all the Employee")
    print("\t\t\t\t5. For Deleting record of a particular the Employee")
    print("\t\t\t\t6. For Modification in a record")
    print("\t\t\t\t7. for Displaying payroll")
    print("\t\t\t\t8. For Displaying Salary Slip for all the employee")
    print("\t\t\t\t9. For Displaying Salary Slip for a particular the employee")
    print("\t\t\t\t10.For Exit")
    print("Enter Choice ......,end=''")
    choice=int(input())
    if choice==1:
          try:
                print("Enter Employee information.......")
                mempno=int(input('enter employee no:'))
                mname=input('enter employee name:')
                mjob=input('enter employee job:')
                mbasic=float(input('enter employee salary:'))
                if mjob.upper()=='OFFICER':
                      mda=mbasic*0.5
                      mhra=mbasic*0.35
                      mtax=mbasic*0.2
                elif mjob.upper()=='MANGER':
                      mda=mbasic*0.45
                      mhra=mbasic*0.30
                      mtax=mbasic*0.15
                else:
                      mda=mbasic*0.40
                      mhra=mbasic*0.25 
                      mtax=mbasic*0.10
                mgross=mbasic+mda+mhra
                mnet=mgross-mtax
                rec=(mempno,mname,mjob,mbasic,mda,mhra,mgross,mtax,mnet)
                query="insert into "+TableName+" values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                mycursor.execute(query,rec)

                mydb.commit()
                print('Record added successfully.....')
          except:
              print('something went wrong')
    elif choice==2:
        
        try:
            query="select * from "+TableName
            mycursor.execute(query)
            print(tabulate(mycursor,headers=['Empno','Name','job','Basic Salary','DA','HRA','GS','Tax','NS'],tablefmt='psql'))
        except:
            print('something went wrong')
    elif choice==3:
        try:
            en=input('Enter employee no.of the record to be displayed...')
            query="select * from "+TableName+" where empno="+en
            mycursor.execute(query)
            myrecord=mycursor.fetchone()
            print("\n\nRecord of Employee No,:"+en)
            print(myrecord)
            c=mycursor.rowcount
            if c== -1:
                print('Nothing to display')
        except:
             print('something went wrong')
    elif choice==4:
        try:
            ch=input('Do you want to delete all the records (y/n)')
            if ch.upper()=='Y':
                mycursor.execute('delete from '+TableName)
                mydb.commit()
                print('All the records are deleted...')
        except:
            print('something went wrong')
    elif choice==5:
         try:
             en=input('Enter employee no. of the record to be deleted...')
             query='delete from '+TableName+' where empno='+en
             mycursor.execute(query)
             mydb.commit()
             c=mycursor.rowcount
             if c>0:
                 print('Deletion done')
             else:
                     print('Employee no ',en,' not found')
         except:
             print('something went wrong')
    elif choice==6:
        try:
            en=input('Enter employee no. of the record to be modified...')
            query='select * from '+TableName+' where empno='+en
            mycursor.execute(query)
            myrecord=mycursor.fetchone()
            c=mycursor.rowcount
            if c==-1:
                print('Empno '+en+' does not exist')
            else:
                mname=myrecord[1]
                mjob=myrecord[2]
                mbasic= myrecord[3]
                print('empno :',myrecord[0])
                print('name  :',myrecord[1])
                print('job   :',myrecord[2])
                print('basic :',myrecord[3])
                print('da    :',myrecord[4])
                print('hra   :',myrecord[5])
                print('gross :',myrecord[6])
                print('tax   :',myrecord[7])
                print('net   :',myrecord[8])
                print('-----------------')
                print('Type value go modify below or just press Enter for no change')
                x=input('Enter name')
                if len(x)>0:
                    mname=x
                x=input('Enter job')
                if len(x)>0:
                    mjob=x
                x=input('Enter basic salary')
                if len(x)>0:
                    mbasic= float(x)
                query='update '+TableName+' set name='+"'"+mname+"'"+','+'job='+"'"+mjob+"'"+','+'basicsalary='+str(mbasic)+' where empno='+en
                print(query)
                mycursor.execute(query)
                mydb.commit()
                print("your record is modify")
                
        except:
             print('something went wrong')
    elif choice==7:
        try:
            query="select * from "+TableName
            mycursor.execute(query)
            myrecord=mycursor.fetchall()
            print('\n\n\n')
            print('*'*100)
            print('Employee payroll'.center(90))
            print('*'*100)  
            now= datetime.datetime.now()
            print('current date and time:',end=' ')
            print(now.strftime('%Y-%m-%d %H:%M:%S'))
            """for rec in myrecord:
                print('%4d %-15s %-10s %8.2f %8.2f %8.2f %9.2f %8.2f %9.2f'%rec)"""
            print()
            print(95*'-')
            print('%-5s %-15s %-10s %-8s %-8s %-8s %-9s %-8s %-9s'%('Empno','Name','Job','Basic','DA','HRA','Gross','TAX','NeT'))
            print(95*'-')
            for rec in myrecord:
                print('%4d %-15s %-10s %8.2f %8.2f %8.2f %9.2f %8.2f %9.2f'%rec)
            print(95*'-')
        except:
            print('something went wrong')
    elif choice==8:
        try:
            query="select * from "+TableName
            mycursor.execute(query)
            myrecord=mycursor.fetchall()
            print('\n\n\n')
            print('*'*100)
            print('Salary Slip'.center(90))
            print('*'*100)  
            now= datetime.datetime.now()
            print('current date and time:',end=' ')
            print(now.strftime('%Y-%m-%d %H:%M:%S'))
            for rec in myrecord:
                print('%4d %-15s %-10s %8.2f %8.2f %8.2f %9.2f %8.2f %9.2f'%rec)
            print(95*'-')
        except:
            print('something went wrong')
    elif choice==9:
        try:
            en=input('Enter employee no. whose pay slip you wnat to retreive:')
            query='select * from '+TableName+' where empno='+en
            mycursor.execute(query)
            now= datetime.datetime.now()
            print('\n\n\n\t\t\tSALARY SLIP')
            print('current date and time:',end=' ')
            print(now.strftime('%Y-%m-%d %H:%M:%S'))
            print(tabulate(mycursor,headers=['Empno','Name','job','Basic Salary','DA','HRA','GS','Tax','NS'],tablefmt='psql'))
        except:
            print('something went wrong')
    elif choice==10:
        break
    else:
        print("Wrong Choice....")
                    
            
            
        
                 
