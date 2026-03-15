# API Reference

Complete documentation for all TRITIUM-Watcher tools and functions.

---

## `distill_essence`

Extracts the 5 most important sentences or data points from a webpage, filtering out navigation and promotional content.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | Yes | The complete URL to scrape (must include https://) |

### Returns

```python
{
    "insights": [
        "First key insight extracted from the page",
        "Second key insight extracted from the page",
        "Third key insight extracted from the page",
        "Fourth key insight extracted from the page",
        "Fifth key insight extracted from the page"
    ],
    "url": "https://example.com",
    "timestamp": "2026-03-15T10:30:00Z"
}
```

### Example Usage

```python
# Extract insights from a news article
result = distill_essence("https://techcrunch.com/latest-ai-news")

# Access the insights
for insight in result["insights"]:
    print(insight)
```

### Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `URLError` | Invalid URL format | Ensure URL starts with https:// |
| `TimeoutError` | Page took too long to load | Try again or check internet connection |
| `ContentError` | No meaningful content found | URL may be behind paywall or require login |

---

## `set_watchdog`

Deploys a background monitor on a URL to check for specific keywords at regular intervals.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | Yes | The complete URL to monitor |
| `keywords` | string | Yes | Comma-separated list of keywords to watch for |
| `interval` | int | No | Check interval in seconds (default: 3600) |

### Returns

```python
{
    "watchdog_id": "abc123",
    "url": "https://example.com",
    "keywords": ["keyword1", "keyword2", "keyword3"],
    "status": "active",
    "created_at": "2026-03-15T10:30:00Z",
    "next_check": "2026-03-15T11:30:00Z"
}
```

### Example Usage

```python
# Monitor competitor pricing page
watchdog = set_watchdog(
    url="https://competitor.com/pricing",
    keywords="discount, sale, new plan, price drop",
    interval=1800  # Check every 30 minutes
)

# Monitor news for specific topics
watchdog = set_watchdog(
    url="https://techcrunch.com",
    keywords="AI regulation, GPT-5, OpenAI"
)
```

### Keyword Matching

- Case-insensitive matching
- Partial word matching (e.g., "price" matches "prices", "pricing")
- Multiple keyword matching (alerts if ANY keyword is found)

### Screenshots

When keywords match:
- Screenshot automatically captured
- Keywords highlighted in red
- Saved to `screenshots/{watchdog_id}_{timestamp}.png`
- Reference added to `WATCHDOG_LOG.md`

---

## `list_watchdogs`

Displays all currently active monitoring tasks.

### Parameters

None

### Returns

```python
{
    "active_watchdogs": [
        {
            "watchdog_id": "abc123",
            "url": "https://example.com",
            "keywords": ["keyword1", "keyword2"],
            "status": "active",
            "last_check": "2026-03-15T10:00:00Z",
            "matches_found": 3
        },
        {
            "watchdog_id": "def456",
            "url": "https://another-site.com",
            "keywords": ["keyword3"],
            "status": "active",
            "last_check": "2026-03-15T09:45:00Z",
            "matches_found": 0
        }
    ],
    "total_watchdogs": 2
}
```

### Example Usage

```python
# List all active watchdogs
watchdogs = list_watchdogs()

print(f"You have {watchdogs['total_watchdogs']} active watchdogs")
for dog in watchdogs['active_watchdogs']:
    print(f"Monitoring {dog['url']} for {len(dog['keywords'])} keywords")
```

---

## `clear_watchdogs`

Stops all active monitoring tasks and wipes the persistence store.

### Parameters

None

### Returns

```python
{
    "cleared": 5,
    "message": "All watchdogs have been stopped and data cleared"
}
```

### Example Usage

```python
# Stop all watchdogs
result = clear_watchdogs()
print(f"Stopped {result['cleared']} watchdogs")
```

### Warning

This action is irreversible. All watchdog configurations and historical data will be permanently deleted.

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `TRITIUM_CHECK_INTERVAL` | 3600 | Default check interval in seconds |
| `TRITIUM_MAX_WATCHDOGS` | 50 | Maximum concurrent watchdogs |
| `TRITIUM_SCREENSHOT_DIR` | ./screenshots | Screenshot save location |
| `APIFY_TOKEN` | None | Apify API token for cloud deployment |

### Local Configuration File

Create a `config.yaml` in your project root:

```yaml
# TRITIUM-Watcher Configuration

# Scraping settings
scraping:
  timeout: 30  # Page load timeout in seconds
  user_agent: "Mozilla/5.0 (compatible; TRITIUM-Watcher/1.0)"
  respect_robots_txt: true

# Watchdog settings
watchdogs:
  default_interval: 3600  # 1 hour
  max_concurrent: 50
  retry_on_failure: true
  max_retries: 3

# Screenshot settings
screenshots:
  enabled: true
  highlight_color: "#FF0000"
  save_directory: "./screenshots"
  max_storage_mb: 500

# Persistence
persistence:
  backend: "local"  # Options: local, apify
  local_path: "./tritium_data.json"
  
# Alerts
alerts:
  log_file: "WATCHDOG_LOG.md"
  webhook_url: null  # Coming soon
```

---

## Rate Limiting

TRITIUM-Watcher includes built-in rate limiting to avoid getting blocked:

- **Default delay between requests**: 2 seconds
- **Exponential backoff** on failures (2s → 4s → 8s → 16s)
- **Respects `robots.txt`** when enabled in config
- **User-agent rotation** for sensitive sites

### Best Practices

1. **Don't set intervals below 300 seconds** (5 minutes)
2. **Limit concurrent watchdogs to 20** for local deployments
3. **Use proxy support** for high-frequency monitoring
4. **Enable retry logic** to handle temporary failures

---

## Error Codes

| Code | Name | Description | Solution |
|------|------|-------------|----------|
| `E001` | InvalidURL | URL format is incorrect | Check URL starts with https:// |
| `E002` | Timeout | Page load exceeded timeout | Increase timeout in config |
| `E003` | BlockedByRobots | Site's robots.txt blocks scraping | Respect robots.txt or disable |
| `E004` | ContentNotFound | No content could be extracted | Site may require authentication |
| `E005` | MaxWatchdogsReached | Cannot create more watchdogs | Clear some watchdogs or increase limit |
| `E006` | ScreenshotFailed | Could not capture screenshot | Check screenshot directory permissions |
| `E007` | PersistenceError | Failed to save data | Check disk space and permissions |

---

## Advanced Usage

### Custom Content Extraction

```python
from tritium_watcher import TritiumWatcher

watcher = TritiumWatcher()

# Extract specific CSS selectors
result = watcher.extract_custom(
    url="https://example.com",
    selectors={
        "title": "h1.article-title",
        "author": ".author-name",
        "date": "time.published"
    }
)
```

### Webhook Notifications (Coming Soon)

```python
# Set webhook for keyword matches
watchdog = set_watchdog(
    url="https://competitor.com",
    keywords="price drop",
    webhook_url="https://your-server.com/alerts"
)
```

---

## Performance Considerations

### Memory Usage

- Each watchdog: ~5-10 MB
- Screenshot: ~200-500 KB
- Log file: ~1 KB per entry

### Recommended Limits

| Deployment | Max Watchdogs | Check Interval |
|------------|---------------|----------------|
| Local (laptop) | 10-20 | 1 hour |
| VPS (2GB RAM) | 50-100 | 30 minutes |
| Apify Cloud | 500+ | 15 minutes |

---

## Support

For issues or feature requests:
- GitHub Issues: https://github.com/Aarav482011/TRITIUM-Watcher/issues
- Email: www.forestritium.com@gmail.com
