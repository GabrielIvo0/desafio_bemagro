from celery_app import celery_app
from database import obter_parcels_por_bbox_complete, armazenar_resultado_uniao, realizar_uniao


@celery_app.task(bind=True)
def tarefa_uniao(self, bbox):
    parcels = obter_parcels_por_bbox_complete(bbox)
    total = len(parcels)
    
    self.update_state(state='PROGRESS', meta={'Quantidade a ser processada ': total})
    
    union_geometry = realizar_uniao(parcels)
    
    new_parcel_id = armazenar_resultado_uniao(union_geometry, name="Union Result", owner="System")
    
    return {'Total Processados': total, 'Status': 'COMPLETED', 'ID': new_parcel_id}
