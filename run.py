import pymysql
import argparse
import subprocess
import os
import xlsxwriter

#Variables Generales

db_name = ''
db_user = ''
db_host = ''
db_password = ''

conexion = None
cursor = None
allDatos = list()
allOperatingSystems = list()


def insertar_os(datos):

    global operatingSystems

    for val in datos:
        allOperatingSystems.append(OperatingSystems(val))

def insertar_all(datos):

    global allDatos

    for val in datos:
        allDatos.append(Datos(val))



class OperatingSystems:
    def __init__(self,datos):

        self.ip             = datos[0]
        self.os             = datos[1]
        self.critical_count = datos[2]
        self.high_count     = datos[3]
        self.medium_count   = datos[4]
        self.low_count      = datos[5]
        self.info_count     = datos[6]



class Datos:
    def __init__(self,datos):
        self.plugin_id =        datos[0]
        self.ip =               datos[1]
        self.os =               datos[2]
        self.severity =         datos[3]
        self.name =             datos[4]
        self.family =           datos[5]
        self.synopsis =         datos[6]
        self.description =      datos[7]
        self.solution =         datos[8]
        self.cvss_base_score =  datos[9]
        self.cvss3_base_score = datos[10]
        self.cvss_vector =      datos[11]
        self.cvss3_vector =     datos[12]
        self.ref =              datos[13]
        self.pub_date =         datos[14]
        self.mod_date =         datos[15]
        self.port =             datos[16]
        self.output =           datos[17]



def make_connection():
    global conexion
    try:
        conexion = pymysql.connect(host=db_host,
                             user=db_user,
                             password=db_password,
                             db=db_name)

 
    except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
        print("Ocurrió un error al conectar: ", e)


def all_folders():

    table="folder" 

    consulta = f"SELECT * FROM {db_name}.{table}"

    cursor.execute(consulta)

    informes = cursor.fetchall()

    for val in informes:
        print(val)


def create_os_xml(output_name):
    workbook = xlsxwriter.Workbook(output_name+"_os.xlsx")    
    worksheet = workbook.add_worksheet()    
        
    row = 0    
    col = 0    
        
    worksheet.write(row,col,"IP")    
    worksheet.write(row,col+1,"OS")    
    worksheet.write(row,col+2,"CRITICAL_COUNT")    
    worksheet.write(row,col+3,"HIGH_COUNT")    
    worksheet.write(row,col+4,"MEDIUM_COUNT")    
    worksheet.write(row,col+5,"LOW_COUNT")    
    worksheet.write(row,col+6,"INFO_COUNT")    
        
    row+=1    
 
    for val in allOperatingSystems:
        worksheet.write(row, col, val.ip)    
        worksheet.write(row, col+1, val.os)    
        worksheet.write(row, col+2, val.critical_count)    
        worksheet.write(row, col+3, val.high_count)    
        worksheet.write(row, col+4, val.medium_count)    
        worksheet.write(row, col+5, val.low_count)    
        worksheet.write(row, col+6, val.info_count)    
    
        row+=1    
    
        
    workbook.close()  


def all_os(output_name):

    table="temp_table" 

    consulta = f"select distinct host_ip,os,critical_count,high_count,medium_count,low_count,info_count from {db_name}.{table}"


    cursor.execute(consulta)

    informes = cursor.fetchall()

    insertar_os(informes)


    create_os_xml(output_name)

    for val in allOperatingSystems:
        print(val.ip," -- ",val.os)
    



def create_all_xml(output_name):
    workbook = xlsxwriter.Workbook(output_name+"_all.xlsx")    
    worksheet = workbook.add_worksheet()    
        
    row = 0    
    col = 0    
        
    worksheet.write(row,col,"IP")    
    worksheet.write(row,col+1,"Plugin-ID")    
    worksheet.write(row,col+2,"OS")    
    worksheet.write(row,col+3,"SEVERITY")    
    worksheet.write(row,col+4,"NAME")    
    worksheet.write(row,col+5,"FAMILY")    
    worksheet.write(row,col+6,"SYNOPSIS")    
    worksheet.write(row,col+7,"DESCRIPTION")    
    worksheet.write(row,col+8,"SOLUTION")    
    worksheet.write(row,col+9,"CVSS_BASE_SCORE")    
    worksheet.write(row,col+10,"CVSS3_BASE_SCORE")    
    worksheet.write(row,col+11,"CVSS_VECTOR")    
    worksheet.write(row,col+12,"CVSS3_VECTOR")    
    worksheet.write(row,col+13,"REF")    
    worksheet.write(row,col+14,"PUB_DATE")    
    worksheet.write(row,col+15,"MOD_DATE")    
    worksheet.write(row,col+16,"PORT")    
    worksheet.write(row,col+17,"OUTPUT")    
    

    row+=1    

    for val in allDatos:

        worksheet.write(row, col, val.ip)    
        worksheet.write(row, col+1, val.plugin_id)    
        worksheet.write(row, col+2, val.os)    
        worksheet.write(row, col+3, val.severity)    
        worksheet.write(row, col+4, val.name)    
        worksheet.write(row, col+5, val.family)    
        worksheet.write(row, col+6, val.synopsis)    
        worksheet.write(row, col+7, val.description)    
        worksheet.write(row, col+8, val.solution)    
        worksheet.write(row, col+9, val.cvss_base_score)    
        worksheet.write(row, col+10, val.cvss3_base_score)    
        worksheet.write(row, col+11, val.cvss_vector)    
        worksheet.write(row, col+12, val.cvss3_vector)    
        worksheet.write(row, col+13, val.ref)    
        worksheet.write(row, col+14, val.pub_date)    
        worksheet.write(row, col+15, val.mod_date)    
        worksheet.write(row, col+16, val.port)    
        worksheet.write(row, col+17, val.output)    
    
        row+=1    
    
        
    workbook.close()  



def return_all(output_name):

    global allDatos

    table="temp_table" 


    consulta = f"select plugin_id,host_ip,os,severity,name,family,synopsis,description,solution,cvss_base_score,cvss3_base_score,cvss_vector,cvss3_vector,ref,pub_date,mod_date,port,output from {db_name}.{table}"

    cursor.execute(consulta)

    informes = cursor.fetchall()
    

    insertar_all(informes)

    create_all_xml(output_name)
        

def make_source(actual):
    os.system(f"./ejemplo.sh {db_name} {actual} {db_password}")
    


def sql_querie(args):

    global conexion
    global cursor 
    try:
        with conexion.cursor() as cursor:
            # En este caso no necesitamos limpiar ningún dato
            if(args.folders == 1):
                all_folders()
            else:
                if(args.target == None):
                    print("You should specify the target folder id")
                    print("Use flag -fd to show all folders and then use the flag -t to specify the folder target for the queries")
                    return
                else:
                    make_source(args.target)
                    if(args.output == None):
                        print("Use flag -out to specify a name of output file")
                        return 
                    if(args.os!=None and args.os>=1):
                        all_os(args.output)
                    if(args.all!=None and args.all>=1):
                        return_all(args.output)

            
    finally:
        conexion.close()
       



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-fd', '--folders', action="count" , help="Display all folders, we need to know the id of the folder")
    parser.add_argument('-t', '--target', type=int , help="Set the folder id for the queires")
    parser.add_argument('-os', '--os', action="count" , help="Querie return all OS from table")
    parser.add_argument('-all', '--all', action="count" , help="Querie return all data from table")
    parser.add_argument('-out', '--output', help="Name of the xlsx output file")

    args = parser.parse_args()


    make_connection()
    sql_querie(args)
    

