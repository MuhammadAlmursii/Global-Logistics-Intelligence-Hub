-- Example staging model
-- This model transforms raw data into a clean, consistent format

with source_data as (

    select * from {{ source('raw', 'example_table') }}

),

renamed as (

    select
        id as id,
        field1,
        field2,
        created_at,
        updated_at

    from source_data

)

select * from renamed


