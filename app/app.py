# app.py
from fastapi import FastAPI, HTTPException, Body
from typing import Union, List
from shapely.geometry import shape
from database import inserir_parcel, obter_parcels_por_bbox, obter_todas_parcels
from tasks import tarefa_uniao

app = FastAPI()

@app.post("/parcels")
async def cadastrar_parcels(parcels: Union[List[dict], dict] = Body(...)):
    #Cadastro de uma ou mais parcels.
    
    if isinstance(parcels, dict):
        parcels = [parcels]
    
    ids_inseridos = []
    for p in parcels:
        try:
            if p.get("type") == "Feature": #GeoJSON
                properties = p.get("properties", {})
                nome = properties.get("name")
                proprietario = properties.get("owner")
                if not nome or not proprietario:
                    raise HTTPException(status_code=400, detail="GeoJSON deve conter 'name' e 'owner' em properties")
        
                geometria_obj = shape(p.get("geometry"))# Shapely para converter a geometria GeoJSON para WKT 
                geometria_wkt = geometria_obj.wkt
            else: #WKT
                nome = p.get("nome")
                proprietario = p.get("proprietario")
                geometria_wkt = p.get("geometria") 
                if not nome or not proprietario or not geometria_wkt:
                    raise HTTPException(status_code=400, detail="Para formato WKT, os campos 'nome', 'proprietario' e 'geometria' são necessários.")
            
            # Insere a parcel no banco de dados
            id_parcel = inserir_parcel(nome, proprietario, geometria_wkt)
            ids_inseridos.append(id_parcel)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    return {"ids": ids_inseridos, "mensagem": "parcels cadastradas com sucesso"}

@app.get("/parcels")
async def listar_parcels(bbox: str = None):
    #Listar parcels, podendo filtrar por bbox, no formato: bbox=minx,miny,maxx,maxy

    try:
        if bbox:
            parcels = obter_parcels_por_bbox(bbox)
        else:
            parcels = obter_todas_parcels()
        return parcels
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/process/union")
async def processar_uniao(bbox: str = Body(..., embed=True)):
    #Processar a união de parcels de forma assíncrona, o tipo do parametro bounding box deve ser no formato:
    # {
    #   "bbox": "minx,miny,maxx,maxy"
    # }
    
    try:
        task = tarefa_uniao.delay(bbox)
        return {"task_id": task.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/process/status/{task_id}")
async def status_tarefa(task_id: str):
    #Consulta o status da tarefa de união pelo ID.
    from celery.result import AsyncResult
    task_result = AsyncResult(task_id)
    if task_result.state == "PENDING":
        return {"Status": "PENDING"}
    elif task_result.state != "FAILURE":
        return {"Status": task_result.state, "Progresso": task_result.info}
    else:
        return {"Status": "FAILURE", "Retorno": str(task_result.info)}
