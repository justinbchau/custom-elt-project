{% macro classify_ratings(column_name) %}
    CASE
        WHEN {{ column_name }} >= 4.5 THEN 'Excellent'
        WHEN {{ column_name }} >= 4.0 THEN 'Good'
        WHEN {{ column_name }} >= 3.0 THEN 'Average'
        ELSE 'Poor'
    END
{% endmacro %}