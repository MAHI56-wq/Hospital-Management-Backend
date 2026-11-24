import logging,uuid
from flask import Flask,g,request
from .config import Config
from .errors import AppError,problem_response
from .repositories.doctor_repository import DoctorRepository
from .repositories.appointment_repository import AppointmentRepository
from .services.doctor_service import DoctorService
from .services.appointment_service import AppointmentService
from .routes.doctor_routes import bp as doctor_bp
from .routes.appointment_routes import bp as appointment_bp
def create_app(overrides=None):
    app=Flask(__name__); c=Config(overrides)
    app.config.update(APP_ENV=c.APP_ENV,LOG_LEVEL=c.LOG_LEVEL,DATABASE_PATH=c.DATABASE_PATH,TESTING=c.TESTING)
    logging.basicConfig(level=getattr(logging,c.LOG_LEVEL.upper(),logging.INFO),
                        format="%(asctime)s %(levelname)s %(name)s %(message)s")
    logger=logging.getLogger("hospital.http")
    dr=DoctorRepository(c.DATABASE_PATH); ar=AppointmentRepository(c.DATABASE_PATH)
    app.extensions["doctor_service"]=DoctorService(dr)
    app.extensions["appointment_service"]=AppointmentService(ar,dr)
    @app.before_request
    def before():
        g.request_id=request.headers.get("X-Request-ID") or uuid.uuid4().hex[:12]
        logger.info("request started id=%s method=%s path=%s",g.request_id,request.method,request.path)
    @app.after_request
    def after(response):
        response.headers["X-Request-ID"]=getattr(g,"request_id","unknown")
        logger.info("request completed id=%s method=%s path=%s status=%s",getattr(g,"request_id","unknown"),request.method,request.path,response.status_code)
        return response
    @app.errorhandler(AppError)
    def app_error(e): return problem_response(e,getattr(g,"request_id",None))
    @app.errorhandler(Exception)
    def unexpected(e):
        app.logger.exception("unhandled exception request_id=%s",getattr(g,"request_id",None))
        return problem_response(AppError(500,"Internal server error","Something went wrong","internal_error"),getattr(g,"request_id",None))
    app.register_blueprint(doctor_bp,url_prefix="/api/doctors")
    app.register_blueprint(appointment_bp,url_prefix="/api/appointments")
    @app.get("/health")
    def health(): return {"status":"ok"}
    return app
