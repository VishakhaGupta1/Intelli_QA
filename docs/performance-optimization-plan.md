# Performance Optimization Plan

## Current Bottlenecks
- Grok latency for one endpoint at a time.
- Serial generation in [ai-generator/main.py](../ai-generator/main.py).
- Collection scans in dashboard API routes.
- Repeated per-day query loops in `/api/results/trend`.
- Fresh browser startup for every UI test in [UITestBase](../test-engine/src/test/java/com/qaplatform/ui/UITestBase.java).

## Optimization Opportunities

| Area | Opportunity | Estimated Impact | Effort |
|---|---|---:|---:|
| Generator | Parallelize endpoint generation with a bounded worker pool | High | Medium |
| Generator | Cache parsed prompts or intermediate endpoint artifacts | Medium | Low |
| MongoDB | Add indexes on result, endpoint, status, and timestamp fields | High | Low |
| Dashboard API | Replace repeated date-loop queries with aggregation pipelines | High | Medium |
| Dashboard API | Add query limits/pagination on result endpoints | Medium | Low |
| UI Tests | Reuse browser sessions per class where safe | Medium | Medium |
| UI | Lazy-load below-the-fold components | Low | Low |

## Expected Throughput
- Small spec: fast enough for local use, usually dominated by model latency.
- 100+ endpoints: generation time becomes the dominant cost unless endpoint calls are parallelized.
- Test execution: 14 tests currently run quickly, but UI tests will dominate as browser count rises.

## Latency Targets
- Generation: under 10s per endpoint as a monitoring target.
- Dashboard API: under 500ms for common queries.
- MongoDB writes: under 100ms per write under nominal load.
- End-to-end test run: under 30s for the current 14-test suite, excluding external service slowness.

## Scaling to 1000+ Tests
- Split generation into batches and use a queue.
- Run Java tests in parallel by class or tag.
- Separate API and UI test execution lanes.
- Use aggregation queries and indexes in MongoDB.
- Move artifacts to object storage instead of relying only on local disk.

## Caching Opportunities
- Cache spec parsing results when the spec has not changed.
- Cache dashboard aggregation output for short intervals if the UI polls frequently.
- Cache Grok prompts only if the inputs are identical and sensitive data has been removed.

## Memory Considerations
- Avoid loading large collections repeatedly in Node.
- Avoid keeping unbounded in-memory test history in the Java process.
- Keep browser sessions short-lived if instability increases.
