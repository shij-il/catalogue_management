"""
Main module for Catalogue Management System.

Provides a text-based interface to perform CRUD operations on catalogues.
"""
from dto.catalogue import Catalogue
from service.catalogue_service import Catalogue_Service
from util.validators import validate_date,validate_int,validate_str,validate_status,validate_name_str
from exception.exceptions import databaseconnectionerror

def menu():
    """
    Displays the main menu and performs actions based on user input.
    Uses Catalogue_Service to handle operations on the catalogue database.
    """
    service=Catalogue_Service()
    while True:
        print("---CATALOGUE MANAGEMENT SYSTEM---")
        print("1.Create Catalogue")
        print("2.View catalogue by id")
        print("3.View all catelogues")
        print("4.Update catelogue by id")
        print("5.Delete catelogue by id")
        print("6.Exit")

        choice = input("Enter a choice(1-6) : ")

        if choice=="1":
            name = validate_name_str("enter the catalogue name :","Catalogue Name")
            description=validate_str("enter the catalogue description : ","Description")
            start_date = validate_date("enter the start date (YYYY-MM-DD) : ")
            end_date = validate_date("enter the end date (YYYY-MM-DD) : ")
            status = validate_status("enter the status (active/inactive/upcoming/expired): ")

            catalogue = Catalogue(name,description,start_date,end_date,status)
            success = service.create_catalogue(catalogue)
            try:
                if success:
                 print("catalogue created succesfully")
                else:
                    print("failed creating database")
            except databaseconnectionerror as e:
                print(f"failed creating database : {e}")    

        elif choice=="2":
            catalogue_id = validate_int("enter the catalogue id : ")
            result = service.get_catalogue_by_id(catalogue_id)
            if result:
                print("catalogue found")
                for k,v in result.items():
                    print(f"{k} : {v}")
            else:
                print("no catalogue found with this id")

        elif choice=="3":
            catalogues = service.get_all_catalogues()
            if catalogues:
                print("all catalogues : ")
                for row in catalogues:
                    print("-"*30)
                    for k,v in row.items():
                        print(f"{k} : {v}")
            else:
                print("catalogues not found")

        elif choice=="4":
            catalogue_id=validate_int("enter the catalogue id  tp update : ")
            name=validate_name_str("enter the new name : ","Catalogue Name")
            description=validate_str("enter te new description : ","description")
            start_date=validate_date("enter the new start date : ")
            end_date=validate_date("enter the new end date : ")
            status=validate_status("enter the new status (active/inactive/upcoming/expired) : ")
            update = Catalogue(name,description,start_date,end_date,status)
            if service.update_catalogue_by_id(catalogue_id,update):
                print("catalogue updated succesfully")
            else:
                print("failed updating catalogue") 

        elif choice=="5":
            catalogue_id=validate_int("enter the catalogue id to delete : ")
            if service.delete_catalogue_by_id(catalogue_id):
                print("catalogue deleted succesfully")
            else:
                print("failed in deleting catalogue")

        elif choice=="6":
            print("Exiting...GoodBye")
            break
        else:
            print("Invalid choice!! Enter a number from 1 - 6")

if __name__=="__main__":
    menu()                