-- Example mart model
-- This model creates a business-ready dataset by combining staging models

with staging_data as (

    select * from {{ ref('stg_example') }}

),

aggregated as (

    select
        date_trunc('day', created_at) as date,
        count(*) as total_records,
        count(distinct field1) as unique_field1_values,
        avg(case when field2 is not null then 1 else 0 end) as completion_rate

    from staging_data
    group by 1

)

select * from aggregated


