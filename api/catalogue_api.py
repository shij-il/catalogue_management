from flask import Blueprint, request, jsonify
from service.catalogue_service import Catalogue_Service
from dto.catalogue import Catalogue
from util.validators import validate_str, validate_name_str, validate_int, validate_date, validate_status
from exception.exceptions import validationerror, databaseconnectionerror
from datetime import date

catalogue_api = Blueprint('catalogue_api', __name__)
catalogue_service = Catalogue_Service()

# Ensure catalogue_id is included in formatted output
def format_catalogue_data(db_data):
    if not db_data:
        return None
    return {
        "catalogue_id": db_data.get('catalogue_id'),  # Must match DB key
        "name": db_data.get('catalogue_name'),
        "description": db_data.get('catalogue_description'),
        "start_date": str(db_data.get('start_date')),
        "end_date": str(db_data.get('end_date')),
        "status": db_data.get('status')
    }

@catalogue_api.route('/catalogues', methods=['POST'])
def create_catalogue():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        name = validate_name_str(data.get('name'), "Catalogue Name")
        description = validate_str(data.get('description'), "Description")
        start_date_obj = validate_date(data.get('start_date'), "Start Date")
        end_date_obj = validate_date(data.get('end_date'), "End Date")
        status = validate_status(data.get('status'), "Status")

        if start_date_obj > end_date_obj:
            raise validationerror("Start date cannot be after end date.")

        catalogue = Catalogue(name, description, start_date_obj, end_date_obj, status)
        success = catalogue_service.create_catalogue(catalogue)

        if success:
            return jsonify({"message": "Catalogue created successfully"}), 201
        else:
            return jsonify({"error": "Failed to create catalogue"}), 500

    except validationerror as e:
        return jsonify({"error": str(e)}), 400
    except databaseconnectionerror as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print("Create Catalogue Exception:", e)
        return jsonify({"error": "Unexpected error occurred"}), 500

@catalogue_api.route('/catalogues/<int:catalogue_id>', methods=['GET'])
def get_catalogue_by_id(catalogue_id):
    try:
        validated_id = validate_int(catalogue_id, "Catalogue ID")
        catalogue = catalogue_service.get_catalogue_by_id(validated_id)

        if catalogue:
            return jsonify(format_catalogue_data(catalogue)), 200
        else:
            return jsonify({"error": "Catalogue not found"}), 404

    except validationerror as e:
        return jsonify({"error": str(e)}), 400
    except databaseconnectionerror as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print("Get by ID Exception:", e)
        return jsonify({"error": "Unexpected error occurred"}), 500

@catalogue_api.route('/catalogues', methods=['GET'])
def get_all_catalogues():
    try:
        catalogues = catalogue_service.get_all_catalogues()
        return jsonify([format_catalogue_data(c) for c in catalogues]), 200
    except databaseconnectionerror as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print("Get All Catalogues Exception:", e)
        return jsonify({"error": "Unexpected error occurred"}), 500

@catalogue_api.route('/catalogues/<int:catalogue_id>', methods=['PUT'])
def update_catalogue_by_id(catalogue_id):
    try:
        data = request.get_json()
        validated_id = validate_int(catalogue_id, "Catalogue ID")

        name = validate_name_str(data.get('name'), "Catalogue Name")
        description = validate_str(data.get('description'), "Description")
        start_date_obj = validate_date(data.get('start_date'), "Start Date")
        end_date_obj = validate_date(data.get('end_date'), "End Date")
        status = validate_status(data.get('status'), "Status")

        if start_date_obj > end_date_obj:
            raise validationerror("Start date cannot be after end date.")

        catalogue = Catalogue(name, description, start_date_obj, end_date_obj, status)
        success = catalogue_service.update_catalogue_by_id(validated_id, catalogue)

        if success:
            return jsonify({"message": "Catalogue updated successfully"}), 200
        else:
            return jsonify({"error": "Catalogue not found or no changes made"}), 404

    except validationerror as e:
        return jsonify({"error": str(e)}), 400
    except databaseconnectionerror as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print("Update Exception:", e)
        return jsonify({"error": "Unexpected error occurred"}), 500

@catalogue_api.route('/catalogues/<int:catalogue_id>', methods=['DELETE'])
def delete_catalogue_by_id(catalogue_id):
    try:
        validated_id = validate_int(catalogue_id, "Catalogue ID")
        success = catalogue_service.delete_catalogue_by_id(validated_id)

        if success:
            return jsonify({"message": "Catalogue deleted successfully"}), 200
        else:
            return jsonify({"error": "Catalogue not found"}), 404

    except validationerror as e:
        return jsonify({"error": str(e)}), 400
    except databaseconnectionerror as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print("Delete Exception:", e)
        return jsonify({"error": "Unexpected error occurred"}), 500
