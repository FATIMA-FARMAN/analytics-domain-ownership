-- Staging: Clean raw hiring events data
-- Materialized as VIEW for cost efficiency

{{
    config(
        materialized='view',
        schema='staging'
    )
}}

with source as (
    select * from {{ ref('hiring_events_incremental_demo') }}
),

cleaned as (
    select
        -- Primary keys
        event_id,
        candidate_id,
        
        -- Event details
        event_type,
        stage,
        event_date,
        
        -- Metadata
        recruiter_id,
        department,
        job_requisition_id,
        
        -- Timestamps
        created_at,
        updated_at,
        
        -- Data quality: Remove invalid records
        case 
            when event_date > current_date() then null
            else event_date
        end as valid_event_date

    from source
    
    -- Basic quality filters
    where event_id is not null
      and candidate_id is not null
      and stage is not null
)

select * from cleaned
