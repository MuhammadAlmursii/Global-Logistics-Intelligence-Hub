{{ config(
    materialized = 'incremental',
    schema = 'raw',
    tags = ['staging', 'policy'],
    description = 'Cleaned and transformed policy & claims data from raw layer'
) }}

SELECT
  policy_id,
  claim_id,
  INITCAP(customer_name) AS customer_name,

  -- Mask email (PII)
  REGEXP_REPLACE(email, r'(^.).*(@.*$)', r'\1***\2') AS email_masked,

  -- Normalize phone (digits only)
  REGEXP_REPLACE(phone, r'[^0-9]', '') AS phone_normalized,

  -- Mask national ID
  CONCAT(SUBSTR(national_id, 1, 3), '-XXXX-XXXX') AS national_id_masked,

  DATE(date_of_birth) AS date_of_birth,
  DATE(claim_date) AS claim_date,
  DATE_DIFF(CURRENT_DATE(), DATE(date_of_birth), YEAR) AS customer_age,

  SPLIT(address, ',')[SAFE_OFFSET(0)] AS city,
  SPLIT(address, ',')[SAFE_OFFSET(1)] AS street,

  UPPER(policy_type) AS policy_type,
  SAFE_CAST(claim_amount AS NUMERIC) AS claim_amount,
  diagnosis,
  hospital_name,

  SAFE_CAST(claim_amount AS NUMERIC) > 10000 AS is_high_value_claim,

  -- Data quality flags
  email IS NOT NULL AS has_email,
  phone IS NOT NULL AS has_phone

FROM {{ ref('stg_policy') }}
