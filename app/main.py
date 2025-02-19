try:
    import logging
    from fastapi import FastAPI
    from app.routers import employee, department, job, user
except Exception as error:
    raise ImportError("Erro de biblioteca: %s" % error)

# Configuração básica do logger para exibir INFO e outros níveis
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

app = FastAPI()


app.include_router(employee.router, prefix="/employees", tags=["Employees"])
app.include_router(department.router, prefix="/departments", tags=["Department"])
app.include_router(job.router, prefix="/jobs", tags=["Job"])
app.include_router(user.router, prefix="/users", tags=["User"])
_logger.info("Rotas estabelecidas!")

@app.get("/")
def read_root():
    return {"message": "API is running"}