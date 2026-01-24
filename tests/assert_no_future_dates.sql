-- Test: No events should have future dates

select
    event_id,
    event_date,
    current_date() as today
from {{ ref('fct_hiring_funnel_incremental') }}
where event_date > current_date()
