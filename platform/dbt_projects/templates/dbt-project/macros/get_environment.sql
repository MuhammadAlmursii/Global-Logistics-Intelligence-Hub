-- Macro to get the current environment
-- This helps with environment-specific logic in dbt models

{% macro get_environment() %}
  {% if target.name == 'dev' %}
    'development'
  {% elif target.name == 'staging' %}
    'staging'
  {% elif target.name == 'prod' %}
    'production'
  {% else %}
    'unknown'
  {% endif %}
{% endmacro %}

-- Macro to get environment-specific schema suffix
{% macro get_schema_suffix() %}
  {% if target.name == 'dev' %}
    '_dev'
  {% elif target.name == 'staging' %}
    '_staging'
  {% else %}
    ''
  {% endif %}
{% endmacro %}


