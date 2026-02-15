-- Example staging model
-- This model transforms raw data into a clean, consistent format

with source_data as (

    select * from {{ source('PLAYVOX_RAW', 'EVALUATIONS') }}

),

renamed as (

    select
       *
    from source_data

)

select * from renamed


