from dataclasses import asdict
from flask import Blueprint,current_app,jsonify,request,url_for
bp=Blueprint("appointments",__name__)
def service(): return current_app.extensions["appointment_service"]
@bp.post("")
def create():
    x=service().create(request.get_json(silent=True)); r=jsonify(asdict(x)); r.status_code=201
    r.headers["Location"]=url_for("appointments.get_one",appointment_id=x.id); return r
@bp.get("")
def listing(): return jsonify([asdict(x) for x in service().list()])
@bp.get("/<int:appointment_id>")
def get_one(appointment_id): return jsonify(asdict(service().get(appointment_id)))
@bp.put("/<int:appointment_id>")
def update(appointment_id): return jsonify(asdict(service().update(appointment_id,request.get_json(silent=True))))
@bp.delete("/<int:appointment_id>")
def delete(appointment_id): service().delete(appointment_id); return "",204
