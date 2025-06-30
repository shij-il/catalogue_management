"""
Main script for the console-based Catalogue Management System.
Allows users to interact with catalogue data via the command line.
"""
from service.catalogue_service import Catalogue_Service
from dto.catalogue import Catalogue
# Ensure correct PascalCase imports for custom exceptions
from exception.exceptions import validationerror, databaseconnectionerror
from util.validators import validate_str, validate_name_str, validate_int, validate_date, validate_status
from datetime import date # Import date for comparisons if needed

catalogue_service = Catalogue_Service()

def display_menu():
    """Prints the main menu options to the console."""
    print("\n--- CATALOGUE MANAGEMENT SYSTEM ---")
    print("1. Create Catalogue")
    print("2. View Catalogue by ID")
    print("3. View All Catalogues")
    print("4. Update Catalogue by ID")
    print("5. Delete Catalogue by ID")
    print("6. Exit")

def menu():
    """Main function to run the console menu loop."""
    while True:
        display_menu()
        choice = input("Enter a choice (1-6): ").strip()

        try:
            if choice == '1':
                print("\n--- Create New Catalogue ---")
                
                name_input = input("Enter the catalogue name: ")
                name = validate_name_str(name_input, "Catalogue Name")

                description_input = input("Enter the catalogue description: ")
                description = validate_str(description_input, "Description")

                start_date_input = input("Enter the start date (YYYY-MM-DD): ")
                start_date_obj = validate_date(start_date_input, "Start Date")

                end_date_input = input("Enter the end date (YYYY-MM-DD): ")
                end_date_obj = validate_date(end_date_input, "End Date")

                
                if start_date_obj > end_date_obj:
                    raise validationerror("Start date cannot be after end date.")

                status_input = input("Enter the status (active/inactive/upcoming/expired): ")
                status = validate_status(status_input, "Status")

                catalogue = Catalogue(name, description, start_date_obj, end_date_obj, status)
                if catalogue_service.create_catalogue(catalogue):
                    print("Catalogue created successfully!")
                else:
                    print("Failed to create catalogue due to a service error.")

            elif choice == '2':
                print("\n--- View Catalogue by ID ---")
                id_input = input("Enter the Catalogue ID to view: ")
                catalogue_id = validate_int(id_input, "Catalogue ID")

                catalogue_data = catalogue_service.get_catalogue_by_id(catalogue_id)
                if catalogue_data:
                    print("\n--- Catalogue Details ---")
                    print(f"ID: {catalogue_data.get('catalogue_id')}")
                    print(f"Name: {catalogue_data.get('catalogue_name')}")
                    print(f"Description: {catalogue_data.get('catalogue_description')}")
                    print(f"Start Date: {catalogue_data.get('start_date')}")
                    print(f"End Date: {catalogue_data.get('end_date')}")
                    print(f"Status: {catalogue_data.get('status')}")
                else:
                    print(f"Catalogue with ID {catalogue_id} not found.")

            elif choice == '3':
                print("\n--- All Catalogues ---")
                all_catalogues = catalogue_service.get_all_catalogues()
                if all_catalogues:
                    for cat in all_catalogues:
                        print("\n--------------------------")
                        print(f"ID: {cat.get('catalogue_id')}")
                        print(f"Name: {cat.get('catalogue_name')}")
                        print(f"Description: {cat.get('catalogue_description')}")
                        print(f"Start Date: {cat.get('start_date')}")
                        print(f"End Date: {cat.get('end_date')}")
                        print(f"Status: {cat.get('status')}")
                    print("\n--------------------------")
                else:
                    print("No catalogues found.")

            elif choice == '4':
                print("\n--- Update Catalogue by ID ---")
                id_input = input("Enter the Catalogue ID to update: ")
                catalogue_id = validate_int(id_input, "Catalogue ID")

                existing_catalogue = catalogue_service.get_catalogue_by_id(catalogue_id)
                if not existing_catalogue:
                    print(f"Catalogue with ID {catalogue_id} not found.")
                    continue 

                print(f"Editing Catalogue ID: {catalogue_id} (Current Name: {existing_catalogue.get('catalogue_name')})")

                name_input = input(f"Enter new name (current: {existing_catalogue.get('catalogue_name')}): ")
                name = validate_name_str(name_input, "Catalogue Name")

                description_input = input(f"Enter new description (current: {existing_catalogue.get('catalogue_description')}): ")
                description = validate_str(description_input, "Description")

                start_date_input = input(f"Enter new start date (YYYY-MM-DD, current: {existing_catalogue.get('start_date')}): ")
                start_date_obj = validate_date(start_date_input, "Start Date")

                end_date_input = input(f"Enter new end date (YYYY-MM-DD, current: {existing_catalogue.get('end_date')}): ")
                end_date_obj = validate_date(end_date_input, "End Date")

                if start_date_obj > end_date_obj:
                    raise validationerror("Start date cannot be after end date.")

                status_input = input(f"Enter new status (active/inactive/upcoming/expired, current: {existing_catalogue.get('status')}): ")
                status = validate_status(status_input, "Status")

                updated_catalogue = Catalogue(name, description, start_date_obj, end_date_obj, status)
                if catalogue_service.update_catalogue_by_id(catalogue_id, updated_catalogue):
                    print(f"Catalogue with ID {catalogue_id} updated successfully!")
                else:
                    print(f"Failed to update catalogue with ID {catalogue_id} or no changes were made.")

            elif choice == '5':
                print("\n--- Delete Catalogue by ID ---")
                id_input = input("Enter the Catalogue ID to delete: ")
                catalogue_id = validate_int(id_input, "Catalogue ID")

                confirm = input(f"Are you sure you want to delete catalogue with ID {catalogue_id}? (yes/no): ").lower()
                if confirm == 'yes':
                    if catalogue_service.delete_catalogue_by_id(catalogue_id):
                        print(f"Catalogue with ID {catalogue_id} deleted successfully!")
                    else:
                        print(f"Catalogue with ID {catalogue_id} not found or failed to delete.")
                else:
                    print("Deletion cancelled.")

            elif choice == '6':
                print("Exiting Catalogue Management System. Goodbye!")
                break 
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")

        except validationerror as e:
            print(f"Input Error: {e}")
        except databaseconnectionerror as e:
            print(f"Database Error: {e}. Please check your database connection and configuration.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Please try again.")

if __name__ == '__main__':
    menu()