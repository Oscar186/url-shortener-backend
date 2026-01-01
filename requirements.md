## URL Shortener – Requirements

### Functional Requirements
- Accept a long URL as input
- Generate a unique short URL
- Redirect short URL to original URL
- Support optional expiry for URLs

### Non-Functional Requirements
- Low latency redirection
- High availability
- Scalable for millions of URLs
- Rate limiting to prevent abuse

### Assumptions
- System is read-heavy
- Short URLs must be unique
- Writes are less frequent than reads



