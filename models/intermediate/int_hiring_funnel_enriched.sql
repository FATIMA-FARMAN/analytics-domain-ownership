-- Intermediate: Enrich hiring events with dimension lookups
-- Materialized as TABLE for reuse

{{
    config(
        materialized='table',
        schema='intermediate'
    )
}}

with staging_events as (
    select * from {{ ref('stg_hiring_events') }}
),

-- Add stage ordering for funnel analysis
stage_order as (
    select
        'applied' as stage,
        1 as stage_order
    union all
    select 'screened', 2
    union all
    select 'interviewed', 3
    union all
    select 'offered', 4
    union all
    select 'hired', 5
),

enriched as (
    select
        e.event_id,
        e.candidate_id,
        e.event_type,
        e.stage,
        so.stage_order,
        e.valid_event_date as event_date,
        e.recruiter_id,
        e.department,
        e.job_requisition_id,
        e.created_at,
        
        -- Calculate time since application
        date_diff(
            e.valid_event_date,
            min(e.valid_event_date) over (partition by e.candidate_id),
            day
        ) as days_since_application,
        
        -- Flag if this is the candidate's first event
        case
            when row_number() over (
                partition by e.candidate_id 
                order by e.valid_event_date
            ) = 1 then true
            else false
        end as is_first_event

    from staging_events e
    left join stage_order so on e.stage = so.stage
    where e.valid_event_date is not null
)

select * from enriched
