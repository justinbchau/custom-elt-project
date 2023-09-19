-- films.sql
SELECT * FROM {{ source('destination_db', 'films') }}
