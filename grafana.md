### 1. Recent Conversations Panel

```sql
SELECT
  timestamp AS time,
  question,
  answer,
  relevance
FROM conversations
ORDER BY timestamp DESC
LIMIT 5
```

### 2. Model Usage Panel

```sql
SELECT
  model_used,
  COUNT(*) as count
FROM conversations
GROUP BY model_used
```

### 3. Token Usage Panel

```sql
SELECT    
  AVG(prompt_tokens) AS avg_prompt_tokens,   
  AVG(completion_tokens) AS avg_completion_tokens,   
  AVG(total_tokens) AS avg_total_tokens 
FROM conversations
```

### 4. OpenAI Cost Panel

```sql
SELECT
  timestamp AS time,
  openai_cost
FROM conversations
WHERE openai_cost > 0
ORDER BY timestamp
```

### 5. Response Time Panel

```sql
SELECT
  timestamp AS time,
  response_time
FROM conversations
ORDER BY timestamp
```

### 6. Feedback Rating Analysis

```sql
SELECT    
	user_rating,   
	COUNT(*) AS count 
FROM user_feedback 
GROUP BY user_rating 
order by user_rating
```

### 7. Relevance Distribution

```sql
SELECT
  relevance,
  COUNT(*) as count
FROM conversations
GROUP BY relevance
```
