{{ config(materialized='view') }}

SELECT
    TRIM(REGEXP_REPLACE("Município", '^[0-9]+ ', '')) AS municipio_nome,
    "Total" AS total_nascimentos_2023,
    2023 AS ano
FROM
    {{ source('origem', 'nascimentos_vivos_origem') }}
WHERE
    TRIM(REGEXP_REPLACE("Município", '^[0-9]+ ', '')) != 'Total'