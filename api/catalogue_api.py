from flask import Blueprint, request, jsonify
from service.catalogue_service import Catalogue_Service
from dto.catalogue import Catalogue
from util.validators import validate_str, validate_name_str, validate_int, validate_date, validate_status
from exception.exceptions import validationerror, databaseconnectionerror
from datetime import date

catalogue_api = Blueprint('catalogue_api', __name__)
catalogue_service = Catalogue_Service()

# Helper function to convert DB-style keys to DTO-style keys for consistent frontend display
def format_catalogue_data(db_data):
    if not db_data:
        return None
    return {
        "catalogue_id": db_data.get('catalogue_id'),
        "name": db_data.get('catalogue_name'),       
        "description": db_data.get('catalogue_description'),
        "start_date": str(db_data.get('start_date')), 
        "end_date": str(db_data.get('end_date')), 
        "status": db_data.get('status')
    }

@catalogue_api.route('/catalogues', methods=['POST'])
def create_catalogue():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    try:
        
        name = validate_name_str(data.get('name'), "Catalogue Name")
        description = validate_str(data.get('description'), "Description")
        start_date_obj = validate_date(data.get('start_date'), "Start Date")
        end_date_obj = validate_date(data.get('end_date'), "End Date")
        status = validate_status(data.get('status'), "Status")

        if start_date_obj > end_date_obj:
            raise validationerror("Start date cannot be after end date.")

        catalogue = Catalogue(name, description, start_date_obj, end_date_obj, status)
        if catalogue_service.create_catalogue(catalogue):
            return jsonify({"message": "Catalogue created successfully"}), 201
        else:
            return jsonify({"error": "Failed to create catalogue due to a server issue"}), 500
    except validationerror as e:
        return jsonify({"error": str(e)}), 400
    except databaseconnectionerror as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"Unhandled error in create_catalogue: {e}")
        return jsonify({"error": f"An unexpected server error occurred: {e}"}), 500

@catalogue_api.route('/catalogues/<int:catalogue_id>', methods=['GET'])
def get_catalogue_by_id(catalogue_id):
    try:
        validated_id = validate_int(catalogue_id, "Catalogue ID")
        db_catalogue_data = catalogue_service.get_catalogue_by_id(validated_id)

        if db_catalogue_data:
            
            formatted_data = format_catalogue_data(db_catalogue_data)
            return jsonify(formatted_data), 200
        else:
            return jsonify({"message": "Catalogue not found"}), 404
    except validationerror as e:
        return jsonify({"error": str(e)}), 400
    except databaseconnectionerror as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"Unhandled error in get_catalogue_by_id: {e}")
        return jsonify({"error": f"An unexpected server error occurred: {e}"}), 500

@catalogue_api.route('/catalogues', methods=['GET'])
def get_all_catalogues():
    try:
        db_catalogues_data = catalogue_service.get_all_catalogues()
        if db_catalogues_data:
            
            formatted_catalogues = [format_catalogue_data(c) for c in db_catalogues_data]
            return jsonify(formatted_catalogues), 200
        else:
            return jsonify([]), 200
    except databaseconnectionerror as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"Unhandled error in get_all_catalogues: {e}")
        return jsonify({"error": f"An unexpected server error occurred: {e}"}), 500

@catalogue_api.route('/catalogues/<int:catalogue_id>', methods=['PUT'])
def update_catalogue_by_id(catalogue_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    try:
        validated_id = validate_int(catalogue_id, "Catalogue ID")

        
        name = validate_name_str(data.get('name'), "Catalogue Name")
        description = validate_str(data.get('description'), "Description")
        start_date_obj = validate_date(data.get('start_date'), "Start Date")
        end_date_obj = validate_date(data.get('end_date'), "End Date")
        status = validate_status(data.get('status'), "Status")

        if start_date_obj > end_date_obj:
            raise validationerror("Start date cannot be after end date.")

        catalogue = Catalogue(name, description, start_date_obj, end_date_obj, status)
        if catalogue_service.update_catalogue_by_id(validated_id, catalogue):
            return jsonify({"message": "Catalogue updated successfully"}), 200
        else:
            return jsonify({"message": "Catalogue not found or no changes made"}), 404
    except validationerror as e:
        return jsonify({"error": str(e)}), 400
    except databaseconnectionerror as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"Unhandled error in update_catalogue_by_id: {e}")
        return jsonify({"error": f"An unexpected server error occurred: {e}"}), 500

@catalogue_api.route('/catalogues/<int:catalogue_id>', methods=['DELETE'])
def delete_catalogue_by_id(catalogue_id):
    try:
        validated_id = validate_int(catalogue_id, "Catalogue ID")
        if catalogue_service.delete_catalogue_by_id(validated_id):
            return jsonify({"message": "Catalogue deleted successfully"}), 200
        else:
            return jsonify({"message": "Catalogue not found"}), 404
    except validationerror as e:
        return jsonify({"error": str(e)}), 400
    except databaseconnectionerror as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"Unhandled error in delete_catalogue_by_id: {e}")
        return jsonify({"error": f"An unexpected server error occurred: {e}"}), 500