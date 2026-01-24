-- Fact: Hiring funnel metrics (incremental)
-- Tracks candidate progression through hiring stages

{{
    config(
        materialized='incremental',
        unique_key='event_id',
        on_schema_change='append_new_columns',
        incremental_strategy='merge',
        partition_by={
            "field": "event_date",
            "data_type": "date",
            "granularity": "day"
        },
        cluster_by=['stage', 'department']
    )
}}

with enriched_events as (
    select * from {{ ref('int_hiring_funnel_enriched') }}
    
    {% if is_incremental() %}
    -- Only process new events (last 3 days for safety)
    where event_date >= date_sub(current_date(), interval {{ var('incremental_lookback_days', 3) }} day)
    {% endif %}
),

final as (
    select
        -- Grain: One row per hiring event
        event_id,
        
        -- Foreign keys
        candidate_id,
        recruiter_id,
        job_requisition_id,
        
        -- Degenerate dimensions
        event_type,
        stage,
        stage_order,
        department,
        
        -- Dates
        event_date,
        created_at,
        
        -- Metrics
        days_since_application,
        is_first_event,
        
        -- Funnel metrics
        case when stage = 'applied' then 1 else 0 end as applied_count,
        case when stage = 'screened' then 1 else 0 end as screened_count,
        case when stage = 'interviewed' then 1 else 0 end as interviewed_count,
        case when stage = 'offered' then 1 else 0 end as offered_count,
        case when stage = 'hired' then 1 else 0 end as hired_count,
        
        -- Audit
        current_timestamp() as dbt_updated_at

    from enriched_events
)

select * from final
