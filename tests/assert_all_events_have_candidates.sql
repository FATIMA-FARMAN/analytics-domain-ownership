-- Test: All events should reference valid candidates

select
    f.event_id,
    f.candidate_id
from {{ ref('fct_hiring_funnel_incremental') }} f
left join {{ ref('dim_candidates') }} d
    on f.candidate_id = d.candidate_id
where d.candidate_id is null
