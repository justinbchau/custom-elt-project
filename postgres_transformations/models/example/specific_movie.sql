{% set film_title = 'Dunkirk' %}

SELECT *
FROM {{ ref('films') }}
WHERE title = '{{ film_title }}'
