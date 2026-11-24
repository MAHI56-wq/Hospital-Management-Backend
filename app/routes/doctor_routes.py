from dataclasses import asdict
from flask import Blueprint,current_app,jsonify,request,url_for
bp=Blueprint("doctors",__name__)
def service(): return current_app.extensions["doctor_service"]
@bp.post("")
def create():
    x=service().create(request.get_json(silent=True)); r=jsonify(asdict(x)); r.status_code=201
    r.headers["Location"]=url_for("doctors.get_one",doctor_id=x.id); return r
@bp.get("")
def listing(): return jsonify([asdict(x) for x in service().list()])
@bp.get("/<int:doctor_id>")
def get_one(doctor_id): return jsonify(asdict(service().get(doctor_id)))
@bp.put("/<int:doctor_id>")
def update(doctor_id): return jsonify(asdict(service().update(doctor_id,request.get_json(silent=True))))
@bp.delete("/<int:doctor_id>")
def delete(doctor_id): service().delete(doctor_id); return "",204
