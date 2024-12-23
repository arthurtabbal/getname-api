from sqlalchemy import text
from flask import request
from flask_api import status
from resources.connections import engine, MULTI_QUERY
from resources.api_decorator import api_endpoint


@api_endpoint()
def get_multiple_names(db_id):
    data = request.get_json()
    ids_list = data.get("patients", [])
    bind_ids = [":" + str(i + 1) for i in range(len(ids_list))]
    dict_keys = [str(i + 1) for i in range(len(ids_list))]

    names = []
    found = []

    engine = get_engine(db_id)

    with engine.connect() as connection:
        result = connection.execute(
            text(MULTI_QUERY.format(",".join(bind_ids))),
            dict(zip(dict_keys, ids_list)),
        )
        for row in result:
            found.append(str(row[1]))
            names.append({"status": "success", "idPatient": row[1], "name": row[0]})

    for id_patient in ids_list:
        if str(id_patient) not in found:
            names.append(
                {
                    "status": "error",
                    "idPatient": id_patient,
                    "name": "Paciente " + str(id_patient),
                }
            )

    return names, status.HTTP_200_OK
