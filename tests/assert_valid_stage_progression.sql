-- Test: Candidates should progress through stages in order
-- (A candidate can't be "hired" before being "interviewed")

with stage_progression as (
    select
        candidate_id,
        max(case when stage = 'hired' then 1 else 0 end) as was_hired,
        max(case when stage = 'interviewed' then 1 else 0 end) as was_interviewed
    from {{ ref('fct_hiring_funnel_incremental') }}
    group by candidate_id
)

select *
from stage_progression
where was_hired = 1
  and was_interviewed = 0  -- Hired without interview = invalid
