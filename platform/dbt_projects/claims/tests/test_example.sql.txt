-- Example dbt test
-- This test checks for data quality issues in your models

select *
from {{ ref('mart_example') }}
where total_records < 0
   or unique_field1_values < 0
   or completion_rate < 0
   or completion_rate > 1


