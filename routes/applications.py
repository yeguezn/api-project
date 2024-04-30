from flask import Blueprint, request, jsonify, render_template
import secrets
from db.connection import db
from db.schemas.register_applications import applications_schema
from helper import token_required, get_app_name, apikey_parameter_required
from regex import REDIRECT_URI_REGEX
import re

applications = Blueprint("applications", __name__)

@applications.route("/register_applications", methods=["POST"])
@token_required
def register_applications(current_user):

	if db.apps.count_documents({"redirect_uri":request.json["redirect_uri"]}) > 0:
		return jsonify({"msg":"La URL ingresada ya está registrada"}), 401
	
	if db.apps.count_documents({"app_name":request.json["app_name"]}) > 0:
		return jsonify({"msg":"Ya existe una aplicación ese nombre"}), 401

	if not re.search(REDIRECT_URI_REGEX, request.json["redirect_uri"]):
		return jsonify({"msg": "URL no válida"}), 401
	  
	api_key = secrets.token_hex(20)
	signature = secrets.token_hex(20)
	document = applications_schema(request.json, api_key, signature)
	db.apps.insert_one(document)
	return jsonify({"msg":f"""
	API_KEY='{api_key}'
	LOGIN_URL='http://localhost:5000/login_users/{api_key}'
	(LOGIN_URL abrirá una ventana de login para autenticar a los usuarios de su aplicación a través de este servicio)
	SECRET='{signature}'
	"""})

@applications.route("/delete_application", methods=["DELETE"])
@token_required
@apikey_parameter_required
def delete_application(current_user):
	app_name = get_app_name(request.args.get("api_key"))
	db.apps.delete_one({"api_key":request.args.get("api_key")})
	msg = f"La aplicación {app_name} ha sido eliminada"

	return jsonify({"msg":msg})

@applications.route("/enable_application", methods=["PUT"])
@token_required
@apikey_parameter_required
def enable_application(current_user):
	app_name = get_app_name(request.args.get("api_key"))
	db.apps.update_one({"api_key":request.args.get("api_key")}, {"$set":{"enabled":True}})
	msg = f"La aplicación {app_name} ha sido habilitada"

	return jsonify({"msg":msg})

@applications.route("/disable_application", methods=["PUT"])
@token_required
@apikey_parameter_required
def disable_application(current_user):
	app_name = get_app_name(request.args.get("api_key"))
	db.apps.update_one({"api_key":request.args.get("api_key")}, {"$set":{"enabled":False}})
	msg = f"La aplicación {app_name} ha sido deshabilitada"

	return jsonify({"msg":msg})


	
	