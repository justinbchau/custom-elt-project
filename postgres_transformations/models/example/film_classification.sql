SELECT
    film_id,
    title,
    user_rating,
    {{ classify_ratings('user_rating') }} AS rating_category,
    release_date
FROM {{ ref('films') }}