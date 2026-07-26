-- Esquema de accident_db.
--
-- POR QUE ESTE FICHERO EXISTE (26/07/2026). No estaba, y sin el este repositorio NO SE PODIA
-- EJECUTAR fuera del portatil donde nacio. Las instrucciones del README iban de `pip install` y
-- `.env` directamente a `python scripts/load_data.py`, y ese script solo hace `USE accident_db`:
-- no crea la base de datos ni las tablas. Cualquiera que clonara el repositorio y siguiera los
-- pasos al pie de la letra fallaba en la primera consulta.
--
-- Es el mismo fallo que este proyecto cuenta como leccion en su propia portada, con otro disfraz:
-- lo que no se ejecuta desde cero no esta comprobado.
--
--     mysql -u tu_usuario -p < sql/schema.sql
--
-- Reconstruido desde las tablas vivas, no escrito de memoria.

CREATE DATABASE IF NOT EXISTS accident_db
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;

USE accident_db;

-- Un accidente es UN NUMERO DE EXPEDIENTE, y esa decision es el corazon del proyecto: contar
-- lineas del Excel en vez de expedientes fue lo que publico 28.773 accidentes donde hay 12.634.
-- La clave primaria sobre `id_accident` es lo que impide que vuelva a pasar.
CREATE TABLE IF NOT EXISTS accidents (
  id_accident          VARCHAR(50)  NOT NULL,
  fecha                DATE         DEFAULT NULL,
  hora                 TIME         DEFAULT NULL,
  calle                VARCHAR(255) DEFAULT NULL,
  distrito             VARCHAR(100) DEFAULT NULL,
  tipo_accidente       VARCHAR(255) DEFAULT NULL,
  estado_meteorologico VARCHAR(100) DEFAULT NULL,
  created_at           TIMESTAMP    NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_accident)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Una fila por persona implicada. Varias por accidente: 2,28 de media.
CREATE TABLE IF NOT EXISTS involved_parties (
  id_involved   INT          NOT NULL AUTO_INCREMENT,
  id_accident   VARCHAR(50)  DEFAULT NULL,
  tipo_persona  VARCHAR(50)  DEFAULT NULL,
  tipo_vehiculo VARCHAR(100) DEFAULT NULL,
  sexo          VARCHAR(20)  DEFAULT NULL,
  edad          VARCHAR(50)  DEFAULT NULL,
  lesividad     VARCHAR(50)  DEFAULT NULL,
  PRIMARY KEY (id_involved),
  KEY id_accident (id_accident),
  CONSTRAINT involved_parties_ibfk_1
    FOREIGN KEY (id_accident) REFERENCES accidents (id_accident)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
