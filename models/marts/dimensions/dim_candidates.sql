-- Dimension: Candidate master data

{{
    config(
        materialized='table',
        schema='marts'
    )
}}

with candidate_events as (
    select
        candidate_id,
        min(event_date) as first_application_date,
        max(event_date) as last_event_date,
        max(case when stage = 'hired' then event_date end) as hire_date,
        max(stage_order) as furthest_stage_reached
    from {{ ref('fct_hiring_funnel_incremental') }}
    group by candidate_id
),

final as (
    select
        candidate_id,
        first_application_date,
        last_event_date,
        hire_date,
        furthest_stage_reached,
        
        -- Derived attributes
        case
            when hire_date is not null then 'Hired'
            when furthest_stage_reached >= 4 then 'Offered but not hired'
            when furthest_stage_reached = 3 then 'Interviewed'
            when furthest_stage_reached = 2 then 'Screened'
            else 'Applied only'
        end as candidate_status,
        
        date_diff(
            coalesce(hire_date, current_date()),
            first_application_date,
            day
        ) as days_in_pipeline,
        
        current_timestamp() as dbt_updated_at
        
    from candidate_events
)

select * from final
