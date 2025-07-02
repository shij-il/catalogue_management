# """
# Service layer to handle catalogue operations with the database.
# """
# from dto.catalogue import Catalogue
# from util.db_connection import get_connection
# from exception.exceptions import databaseconnectionerror 

# class Catalogue_Service:
#     """
#     Provides methods to perform CRUD operations on catalogue data.
#     """
#     def create_catalogue(self, catalogue: Catalogue) -> bool:
#         """
#         Creates a new catalogue record in the database.

#         :param catalogue: Catalogue object to insert.
#         :return: True if the operation is successful.
#         :raises DatabaseConnectionError: If a database operation fails.
#         """
#         conn = None
#         cursor = None
#         try:
#             conn = get_connection()
#             cursor = conn.cursor()
#             query = """
#                 INSERT INTO catalogue (catalogue_name, catalogue_description, start_date, end_date, status)
#                 VALUES (%s, %s, %s, %s, %s)
#             """
#             cursor.execute(query, (catalogue.name, catalogue.description, catalogue.start_date, catalogue.end_date, catalogue.status))
#             conn.commit()
#             return True
#         except databaseconnectionerror as e:
            
#             raise e
#         except Exception as e:
#             print(f"Error creating catalogue: {e}")
#             if conn:
#                 conn.rollback() 
#             return False
#         finally:
#             if cursor:
#                 cursor.close()
#             if conn:
#                 conn.close()

#     def get_catalogue_by_id(self, catalogue_id: int) -> dict:
#         """
#         Retrieves a catalogue record by ID.

#         :param catalogue_id: ID of the catalogue to fetch.
#         :return: Dictionary of the catalogue record or None.
#         :raises DatabaseConnectionError: If a database operation fails.
#         """
#         conn = None
#         cursor = None
#         try:
#             conn = get_connection()
#             cursor = conn.cursor(dictionary=True) 
#             cursor.execute("SELECT * FROM catalogue WHERE catalogue_id = %s", (catalogue_id,))
#             result = cursor.fetchone()
#             return result
#         except databaseconnectionerror as e:
#             raise e
#         except Exception as e:
#             print(f"Error getting catalogue by ID: {e}")
#             return None
#         finally:
#             if cursor:
#                 cursor.close()
#             if conn:
#                 conn.close()

#     def get_all_catalogues(self) -> list:
#         """
#         Retrieves all catalogue records.

#         :return: List of dictionaries containing all catalogue records.
#         :raises DatabaseConnectionError: If a database operation fails.
#         """
#         conn = None
#         cursor = None
#         try:
#             conn = get_connection()
#             cursor = conn.cursor(dictionary=True)
#             cursor.execute("SELECT * FROM catalogue ORDER BY catalogue_id ASC") 
#             result = cursor.fetchall()
#             return result
#         except databaseconnectionerror as e:
#             raise e
#         except Exception as e:
#             print(f"Error getting all catalogues: {e}")
#             return []
#         finally:
#             if cursor:
#                 cursor.close()
#             if conn:
#                 conn.close()

#     def update_catalogue_by_id(self, catalogue_id: int, catalogue: Catalogue) -> bool:
#         """
#         Updates a catalogue by ID.

#         :param catalogue_id: ID of the catalogue to update.
#         :param catalogue: Updated Catalogue object.
#         :return: True if any record was updated, else False.
#         :raises DatabaseConnectionError: If a database operation fails.
#         """
#         conn = None
#         cursor = None
#         try:
#             conn = get_connection()
#             cursor = conn.cursor()
#             query = """
#                 UPDATE catalogue SET catalogue_name=%s, catalogue_description=%s, start_date=%s, end_date=%s, status=%s
#                 WHERE catalogue_id = %s
#             """
#             cursor.execute(query, (catalogue.name, catalogue.description, catalogue.start_date, catalogue.end_date, catalogue.status, catalogue_id))
#             conn.commit()
#             return cursor.rowcount > 0
#         except databaseconnectionerror as e:
#             raise e
#         except Exception as e:
#             print(f"Error updating catalogue: {e}")
#             if conn:
#                 conn.rollback()
#             return False
#         finally:
#             if cursor:
#                 cursor.close()
#             if conn:
#                 conn.close()

#     def delete_catalogue_by_id(self, catalogue_id: int) -> bool:
#         """
#         Deletes a catalogue by ID.

#         :param catalogue_id: ID of the catalogue to delete.
#         :return: True if a record was deleted, else False.
#         :raises DatabaseConnectionError: If a database operation fails.
#         """
#         conn = None
#         cursor = None
#         try:
#             conn = get_connection()
#             cursor = conn.cursor()
#             cursor.execute("DELETE FROM catalogue WHERE catalogue_id = %s", (catalogue_id,))
#             conn.commit()
#             return cursor.rowcount > 0
#         except databaseconnectionerror as e:
#             raise e
#         except Exception as e:
#             print(f"Error deleting catalogue: {e}")
#             if conn:
#                 conn.rollback()
#             return False
#         finally:
#             if cursor:
#                 cursor.close()
#             if conn:
#                 conn.close()

"""
Service layer to handle catalogue operations with the database.
"""
from dto.catalogue import Catalogue
from util.db_connection import get_connection
from exception.exceptions import databaseconnectionerror 

class Catalogue_Service:
    """
    Provides methods to perform CRUD operations on catalogue data.
    """
    def create_catalogue(self, catalogue: Catalogue) -> bool:
        """
        Creates a new catalogue record in the database.

        :param catalogue: Catalogue object to insert.
        :return: True if the operation is successful.
        :raises DatabaseConnectionError: If a database operation fails.
        """
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO catalogue (catalogue_name, catalogue_description, start_date, end_date, status)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                catalogue.name,
                catalogue.description,
                str(catalogue.start_date),  # Ensure date is string if MySQL expects string format
                str(catalogue.end_date),
                catalogue.status
            ))
            conn.commit()
            return True
        except databaseconnectionerror as e:
            raise e
        except Exception as e:
            print(f"Error creating catalogue: {e}")
            if conn:
                conn.rollback() 
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_catalogue_by_id(self, catalogue_id: int) -> dict:
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True) 
            cursor.execute("SELECT * FROM catalogue WHERE catalogue_id = %s", (catalogue_id,))
            result = cursor.fetchone()
            return result
        except databaseconnectionerror as e:
            raise e
        except Exception as e:
            print(f"Error getting catalogue by ID: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_all_catalogues(self) -> list:
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM catalogue ORDER BY catalogue_id DESC")  # newest first
            result = cursor.fetchall()
            return result
        except databaseconnectionerror as e:
            raise e
        except Exception as e:
            print(f"Error getting all catalogues: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_catalogue_by_id(self, catalogue_id: int, catalogue: Catalogue) -> bool:
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = """
                UPDATE catalogue SET catalogue_name=%s, catalogue_description=%s, start_date=%s, end_date=%s, status=%s
                WHERE catalogue_id = %s
            """
            cursor.execute(query, (
                catalogue.name,
                catalogue.description,
                str(catalogue.start_date),
                str(catalogue.end_date),
                catalogue.status,
                catalogue_id
            ))
            conn.commit()
            return cursor.rowcount > 0
        except databaseconnectionerror as e:
            raise e
        except Exception as e:
            print(f"Error updating catalogue: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_catalogue_by_id(self, catalogue_id: int) -> bool:
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM catalogue WHERE catalogue_id = %s", (catalogue_id,))
            conn.commit()
            return cursor.rowcount > 0
        except databaseconnectionerror as e:
            raise e
        except Exception as e:
            print(f"Error deleting catalogue: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()