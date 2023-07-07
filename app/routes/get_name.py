from sqlalchemy import text
from flask_api import status
from connections import engine, QUERY


def get_name(idPatient):
    name = None
    with engine.connect() as connection:
        result = connection.execute(text(QUERY.format(idPatient)))
        for row in result:
            name = row[0]

    if name:
        return {
            "status": "success",
            "idPatient": idPatient,
            "name": name,
        }, status.HTTP_200_OK
    else:
        return {
            "status": "error",
            "idPatient": idPatient,
            "name": "Paciente " + str(idPatient),
        }, status.HTTP_400_BAD_REQUEST
