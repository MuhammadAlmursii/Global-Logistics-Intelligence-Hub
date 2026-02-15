-- Example mart model
-- This model creates a business-ready dataset by combining staging models

with staging_data as (

    select * from {{ ref('stg_example') }}

),

aggregated as (

    select
       *
    from staging_data

)

select * from aggregated


