{{ config(materialized='table') }}

WITH municipios AS (
    SELECT DISTINCT
        TRIM(REGEXP_REPLACE("Município", '^[0-9]+ ', '')) AS municipio_nome
    FROM {{ source('origem', 'mortalidades_origem') }}
    WHERE "Município" IS NOT NULL

    UNION

    SELECT DISTINCT
        TRIM(REGEXP_REPLACE("Município", '^[0-9]+ ', '')) AS municipio_nome
    FROM {{ source('origem', 'nascimentos_vivos_origem') }}
    WHERE "Município" IS NOT NULL
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['municipio_nome']) }} AS id_localidade,
    municipio_nome
FROM
    municipios