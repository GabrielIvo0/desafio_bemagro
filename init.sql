CREATE TABLE parcels (
  id UUID PRIMARY KEY,
  name VARCHAR(100),
  owner VARCHAR(100),
  geometry GEOMETRY(Polygon, 4326)
);

INSERT INTO parcels (id, name, owner, geometry) VALUES
('00000000-0000-0000-0000-000000000001', 'Parcela 1', 'Dono 1',  
 ST_GeomFromText('POLYGON((20.0 20.0, 22.0 20.0, 23.0 22.0, 21.0 24.0, 19.0 22.0, 20.0 20.0))', 4326));

INSERT INTO parcels (id, name, owner, geometry) VALUES
('00000000-0000-0000-0000-000000000002', 'Parcela 2', 'Dono 2',  
 ST_GeomFromText('POLYGON((30.0 30.0, 32.0 30.0, 33.0 32.0, 31.0 34.0, 29.0 32.0, 30.0 30.0))', 4326));

INSERT INTO parcels (id, name, owner, geometry) VALUES
('00000000-0000-0000-0000-000000000003', 'Parcela 3', 'Dono 3',  
 ST_GeomFromText('POLYGON((40.0 40.0, 42.0 40.0, 43.0 42.0, 41.0 44.0, 39.0 42.0, 40.0 40.0))', 4326));

INSERT INTO parcels (id, name, owner, geometry) VALUES
('00000000-0000-0000-0000-000000000004', 'Parcela 4', 'Dono 4',  
 ST_GeomFromText('POLYGON((50.0 50.0, 52.0 50.0, 53.0 52.0, 51.0 54.0, 49.0 52.0, 50.0 50.0))', 4326));

INSERT INTO parcels (id, name, owner, geometry) VALUES
('00000000-0000-0000-0000-000000000005', 'Parcela 5', 'Dono 5',  
 ST_GeomFromText('POLYGON((20.0 20.0, 25.0 20.0, 25.0 25.0, 20.0 25.0, 20.0 20.0))', 4326));

INSERT INTO parcels (id, name, owner, geometry) VALUES
('00000000-0000-0000-0000-000000000006', 'Parcela 6', 'Dono 6',  
 ST_GeomFromText('POLYGON((23.0 23.0, 28.0 23.0, 28.0 28.0, 23.0 28.0, 23.0 23.0))', 4326));

INSERT INTO parcels (id, name, owner, geometry) VALUES
('00000000-0000-0000-0000-000000000007', 'Parcela 7', 'Dono 7',  
 ST_GeomFromText('POLYGON((15.0 15.0, 20.0 15.0, 20.0 20.0, 15.0 20.0, 15.0 15.0))', 4326));

INSERT INTO parcels (id, name, owner, geometry) VALUES
('00000000-0000-0000-0000-000000000008', 'Parcela 8', 'Dono 8',  
 ST_GeomFromText('POLYGON((18.0 18.0, 23.0 18.0, 23.0 23.0, 18.0 23.0, 18.0 18.0))', 4326));