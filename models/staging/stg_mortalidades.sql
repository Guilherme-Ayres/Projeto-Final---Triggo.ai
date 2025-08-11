{{ config(materialized='view') }}

SELECT
    TRIM(REGEXP_REPLACE("Município", '^[0-9]+ ', '')) AS municipio_nome,
    "Óbitos p/Residênc" AS total_mortalidades_2023,
    2023 AS ano
FROM
    {{ source('origem', 'mortalidades_origem') }}
WHERE
    TRIM(REGEXP_REPLACE("Município", '^[0-9]+ ', '')) != 'Total'