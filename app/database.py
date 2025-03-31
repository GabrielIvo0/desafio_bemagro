import os
import uuid
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://root:desafiobemagro@localhost:5432/bemagrodb")
engine = create_engine(DATABASE_URL)

def inserir_parcel(nome: str, proprietario: str, geometria_wkt: str) -> str:
    #Insere uma nova parcel no banco de dados.

    novo_id = str(uuid.uuid4())
    comando = text("""
        INSERT INTO parcels (id, name, owner, geometry)
        VALUES (:id, :name, :owner, ST_GeomFromText(:geometry, 4326))
    """)
    with engine.begin() as conexao:
        conexao.execute(comando, {
            "id": novo_id,
            "name": nome,
            "owner": proprietario,
            "geometry": geometria_wkt
        })
    return novo_id

def obter_todas_parcels():
    #Recupera todas as parcels cadastradas no banco de dados.
    
    comando = text("""
        SELECT 
            id, 
            name, 
            owner,
            ST_Area(geometry) AS area,
            ST_AsText(ST_Envelope(geometry)) AS bounding_box
        FROM parcels
    """)
    with engine.connect() as conexao:
        resultado = conexao.execute(comando)
        parcels = [dict(linha._mapping) for linha in resultado]
    return parcels

def obter_parcels_por_bbox(bbox_str: str):
    #Obtém as parcels que intersectam o bounding box informado.

    minx, miny, maxx, maxy = map(float, bbox_str.split(','))
    consulta = text("""
        SELECT id, 
               name , 
               owner,
               ST_Area(geometry) AS area,
               ST_Envelope(geometry) AS bounding_box
        FROM parcels
        WHERE ST_Intersects(
            geometry,
            ST_MakeEnvelope(:minx, :miny, :maxx, :maxy, 4326)
        )
    """)
    with engine.connect() as conexao:
        resultado = conexao.execute(consulta, {"minx": minx, "miny": miny, "maxx": maxx, "maxy": maxy})
        parcels = [dict(linha._mapping) for linha in resultado]
    return parcels

def obter_parcels_por_bbox_complete(bbox_str: str):
    #Obtém dados completos dos parcels que intersectam o bounding box informado.

    minx, miny, maxx, maxy = map(float, bbox_str.split(','))
    consulta = text("""
        SELECT id, 
               name , 
               owner,
               ST_Area(geometry) AS area,
               ST_AsText(geometry) AS geometria_wkt,
               ST_Envelope(geometry) AS bounding_box
        FROM parcels
        WHERE ST_Intersects(
            geometry,
            ST_MakeEnvelope(:minx, :miny, :maxx, :maxy, 4326)
        )
    """)
    with engine.connect() as conexao:
        resultado = conexao.execute(consulta, {"minx": minx, "miny": miny, "maxx": maxx, "maxy": maxy})
        parcels = [dict(linha._mapping) for linha in resultado]
    return parcels

def armazenar_resultado_uniao(geometria_wkt: str, name: str = "Union Result", owner: str = "System"):
    # Armazena o resultado da união espacial das parcels no banco de dados.
    novo_id = str(uuid.uuid4())
    comando = text("""
        INSERT INTO parcels (id, name, owner, geometry)
        VALUES (:id, :name, :owner, ST_GeomFromText(:geometria, 4326))
    """)
    with engine.begin() as conexao:
        conexao.execute(comando, {
            "id": novo_id, 
            "name": name, 
            "owner": owner, 
            "geometria": geometria_wkt
        })
    return novo_id

def realizar_uniao(parcelas: list) -> str:
    #Realiza a união espacial das parcelas informadas utilizando o ST_Union do PostGIS.

    if not parcelas:
        return None

    placeholders = ", ".join(
        [f"(ST_GeomFromText(:par_{i}, 4326))" for i in range(len(parcelas))]# Placeholders para cada parcela
    )
    
    params = {f"par_{i}": parcel["geometria_wkt"] for i, parcel in enumerate(parcelas)}# Dicionário de parâmetros para os placeholders
    
    query = text(f"""
        SELECT ST_AsText(ST_Union(geom)) AS geometria_unida
        FROM (
            VALUES {placeholders}
        ) AS tmp(geom)
    """)
    
    with engine.connect() as conexao:
        resultado = conexao.execute(query, params)
        linha = resultado.fetchone()
        
        if linha is not None:
            try:
                valor = linha._mapping["geometria_unida"]
            except AttributeError:
                valor = linha[0]
            return valor if valor else None
        return None
