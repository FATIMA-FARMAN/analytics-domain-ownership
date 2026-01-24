

with src as (
    select
        cast(event_id as int64) as event_id,
        cast(candidate_id as int64) as candidate_id,
        cast(stage as string) as stage,
        TIMESTAMP(event_ts) as event_ts
    from `core-rhythm-462516-n5`.`people_analytics`.`hiring_events_incremental_demo`
)

select *
from src


where event_ts > (select TIMESTAMP(max(event_ts)) from `core-rhythm-462516-n5`.`people_analytics`.`fct_hiring_funnel_incremental`)
