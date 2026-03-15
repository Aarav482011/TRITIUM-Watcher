# Configuration Guide

TRITIUM-Watcher can be customized through environment variables and a configuration file.

---

## Quick Start

Create a `config.yaml` file in your project root:

```yaml
# Minimal configuration
scraping:
  timeout: 30

watchdogs:
  default_interval: 3600
  max_concurrent: 20
```

---

## Configuration Methods

### 1. Configuration File (Recommended)

Create `config.yaml` in project root:

```yaml
# TRITIUM-Watcher Configuration File
# Full configuration options

# ==========================================
# SCRAPING SETTINGS
# ==========================================
scraping:
  # Maximum time to wait for page load (seconds)
  timeout: 30
  
  # User agent string for requests
  user_agent: "Mozilla/5.0 (compatible; TRITIUM-Watcher/1.0)"
  
  # Respect robots.txt directives
  respect_robots_txt: true
  
  # Wait time between requests to same domain (seconds)
  request_delay: 2
  
  # Maximum retries on failure
  max_retries: 3
  
  # Retry backoff multiplier (2s → 4s → 8s)
  retry_backoff: 2

# ==========================================
# WATCHDOG SETTINGS
# ==========================================
watchdogs:
  # Default check interval (seconds)
  # Minimum: 300 (5 minutes)
  default_interval: 3600
  
  # Maximum concurrent watchdogs
  max_concurrent: 50
  
  # Retry failed checks
  retry_on_failure: true
  
  # Notify on every match or only first
  notify_on_every_match: false
  
  # Auto-restart watchdogs after system restart
  persistent: true

# ==========================================
# SCREENSHOT SETTINGS
# ==========================================
screenshots:
  # Enable screenshot capture
  enabled: true
  
  # Highlight color for keyword matches (hex)
  highlight_color: "#FF0000"
  
  # Save directory (relative or absolute path)
  save_directory: "./screenshots"
  
  # Maximum storage in megabytes
  max_storage_mb: 500
  
  # Screenshot quality (1-100)
  quality: 85
  
  # Full page screenshot or viewport only
  full_page: false
  
  # Automatically delete old screenshots
  auto_cleanup: true
  
  # Days to keep screenshots before deletion
  cleanup_days: 30

# ==========================================
# PERSISTENCE SETTINGS
# ==========================================
persistence:
  # Backend: 'local' or 'apify'
  backend: "local"
  
  # Local storage file path
  local_path: "./tritium_data.json"
  
  # Apify Key-Value store name (for cloud deployment)
  apify_store_name: "tritium-watchdogs"
  
  # Auto-save interval (seconds)
  autosave_interval: 60

# ==========================================
# ALERT SETTINGS
# ==========================================
alerts:
  # Log file location
  log_file: "WATCHDOG_LOG.md"
  
  # Maximum log file size (MB) before rotation
  max_log_size_mb: 10
  
  # Webhook URL for notifications (coming soon)
  webhook_url: null
  
  # Email notifications (coming soon)
  email:
    enabled: false
    smtp_server: null
    sender: null
    recipients: []

# ==========================================
# PERFORMANCE SETTINGS
# ==========================================
performance:
  # Enable browser headless mode
  headless: true
  
  # Number of concurrent browser instances
  max_browsers: 3
  
  # Enable JavaScript execution
  javascript_enabled: true
  
  # Wait for network idle before scraping
  wait_for_network_idle: true
  
  # Memory limit per browser instance (MB)
  memory_limit_mb: 512

# ==========================================
# LOGGING SETTINGS
# ==========================================
logging:
  # Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
  level: "INFO"
  
  # Log file location (null for console only)
  file: "tritium.log"
  
  # Maximum log file size (MB)
  max_size_mb: 5
  
  # Number of backup log files to keep
  backup_count: 3
  
  # Log format
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ==========================================
# SECURITY SETTINGS
# ==========================================
security:
  # Enable proxy support
  proxy_enabled: false
  
  # Proxy URL (http://user:pass@host:port)
  proxy_url: null
  
  # Rotate user agents
  rotate_user_agents: false
  
  # SSL verification
  verify_ssl: true
  
  # Allowed domains (empty = all allowed)
  allowed_domains: []
  
  # Blocked domains
  blocked_domains: []
```

### 2. Environment Variables

Set via command line or `.env` file:

```bash
# Core settings
export TRITIUM_CHECK_INTERVAL=3600
export TRITIUM_MAX_WATCHDOGS=50
export TRITIUM_SCREENSHOT_DIR="./screenshots"

# Cloud deployment
export APIFY_TOKEN="your-apify-token-here"

# Advanced
export TRITIUM_HEADLESS=true
export TRITIUM_RESPECT_ROBOTS=true
export TRITIUM_LOG_LEVEL="INFO"
```

### 3. Programmatic Configuration

```python
from tritium_watcher import TritiumWatcher, Config

# Create custom configuration
config = Config(
    scraping_timeout=60,
    max_watchdogs=100,
    screenshot_enabled=True,
    highlight_color="#00FF00"
)

# Initialize with config
watcher = TritiumWatcher(config=config)
```

---

## Configuration Priority

1. **Programmatic** (highest priority)
2. **Environment variables**
3. **config.yaml file**
4. **Default values** (lowest priority)

Example:
```python
# config.yaml has: max_watchdogs: 20
# Environment has: TRITIUM_MAX_WATCHDOGS=50
# Result: 50 (environment wins)
```

---

## Configuration Validation

TRITIUM-Watcher validates configuration on startup:

```python
# Automatic validation
watcher = TritiumWatcher()  # Raises ConfigError if invalid

# Manual validation
from tritium_watcher import Config

config = Config.load("config.yaml")
errors = config.validate()

if errors:
    for error in errors:
        print(f"Config error: {error}")
```

### Common Validation Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `InvalidInterval` | Interval < 300 seconds | Increase to at least 300 |
| `InvalidPath` | Directory doesn't exist | Create directory or fix path |
| `InvalidColor` | Bad hex color format | Use format #RRGGBB |
| `InvalidProxy` | Malformed proxy URL | Check URL format |

---

## Environment-Specific Configs

### Development

```yaml
# config.dev.yaml
scraping:
  timeout: 10  # Faster timeouts
  
watchdogs:
  default_interval: 300  # 5 minute checks
  max_concurrent: 5  # Limited concurrency
  
logging:
  level: "DEBUG"  # Verbose logging
  
screenshots:
  enabled: true
  full_page: true
```

### Production

```yaml
# config.prod.yaml
scraping:
  timeout: 30
  respect_robots_txt: true
  
watchdogs:
  default_interval: 3600  # Hourly checks
  max_concurrent: 100
  persistent: true
  
logging:
  level: "WARNING"  # Less verbose
  file: "/var/log/tritium/tritium.log"
  
persistence:
  backend: "apify"  # Cloud storage
  
performance:
  max_browsers: 10  # Higher concurrency
```

Load specific config:
```bash
python tritium_watcher.py --config config.prod.yaml
```

---

## Advanced Configuration

### Rate Limiting

Control request frequency per domain:

```yaml
scraping:
  # Global rate limit (requests per minute)
  global_rate_limit: 60
  
  # Per-domain limits
  domain_limits:
    "example.com": 10  # Max 10 req/min
    "api.site.com": 30  # Max 30 req/min
```

### Custom User Agents

Rotate user agents to avoid detection:

```yaml
scraping:
  rotate_user_agents: true
  user_agents:
    - "Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."
    - "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)..."
    - "Mozilla/5.0 (X11; Linux x86_64)..."
```

### Proxy Configuration

Use proxies for sensitive monitoring:

```yaml
security:
  proxy_enabled: true
  proxy_url: "http://user:pass@proxy.example.com:8080"
  
  # Or use proxy rotation
  proxy_rotation: true
  proxy_list:
    - "http://proxy1.example.com:8080"
    - "http://proxy2.example.com:8080"
    - "http://proxy3.example.com:8080"
```

### Content Filtering

Filter unwanted content:

```yaml
scraping:
  # Blocked CSS selectors (won't be extracted)
  blocked_selectors:
    - ".advertisement"
    - "#cookie-banner"
    - ".newsletter-popup"
  
  # Required selectors (page must contain)
  required_selectors:
    - "article"
    - ".content"
```

---

## Docker Configuration

When using Docker, pass config via volume:

```bash
# docker-compose.yml
version: '3.8'
services:
  tritium:
    image: tritium-watcher:latest
    volumes:
      - ./config.yaml:/app/config.yaml
      - ./screenshots:/app/screenshots
    environment:
      - APIFY_TOKEN=${APIFY_TOKEN}
```

---

## Cloud Deployment (Apify)

Configuration for Apify deployment:

```yaml
# config.apify.yaml
persistence:
  backend: "apify"
  apify_store_name: "tritium-watchdogs"
  
performance:
  # Use Apify's infrastructure
  max_browsers: 20
  memory_limit_mb: 2048
  
screenshots:
  # Store in Apify dataset
  save_to_dataset: true
  
alerts:
  # Use Apify webhooks
  webhook_url: "${APIFY_WEBHOOK_URL}"
```

Set Apify token:
```bash
export APIFY_TOKEN="your_token_here"
```

---

## Troubleshooting

### Config Not Loading

```bash
# Check config file location
python -c "from tritium_watcher import Config; print(Config.get_config_path())"

# Validate config
python -c "from tritium_watcher import Config; Config.load('config.yaml').validate()"
```

### Performance Issues

```yaml
# Reduce memory usage
performance:
  max_browsers: 1
  memory_limit_mb: 256
  
watchdogs:
  max_concurrent: 10
```

### Getting Blocked

```yaml
# More respectful scraping
scraping:
  request_delay: 5  # Longer delays
  respect_robots_txt: true
  
security:
  rotate_user_agents: true
  proxy_enabled: true
```

---

## Configuration Examples

See `examples/configs/` directory for:
- `minimal.yaml` - Bare minimum config
- `development.yaml` - Dev environment
- `production.yaml` - Production deployment
- `high-frequency.yaml` - Frequent checks
- `respectful.yaml` - Conservative settings

---

## Support

Questions about configuration?
- Check [API Reference](API_REFERENCE.md)
- Open an [issue](https://github.com/Aarav482011/TRITIUM-Watcher/issues)
- Email: www.forestritium.com@gmail.com
