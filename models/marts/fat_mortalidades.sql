{{ config(materialized='table') }}

SELECT
    dim.id_localidade,
    REPLACE(REPLACE(dim.municipio_nome, '"', ''), 'MUNICIPIO IGNORADO', '') AS municipio_nome,
    stg.ano,
    SUM(stg.total_mortalidades_2023) AS total_mortalidades_2023
FROM
    {{ ref('stg_mortalidades') }} AS stg
INNER JOIN
    {{ ref('dim_localidade') }} AS dim
    ON stg.municipio_nome = dim.municipio_nome
WHERE
    dim.municipio_nome NOT LIKE 'MUNICIPIO IGNORADO%'
GROUP BY
    dim.id_localidade,
    dim.municipio_nome,
    stg.ano
ORDER BY
    total_mortalidades_2023 DESC
