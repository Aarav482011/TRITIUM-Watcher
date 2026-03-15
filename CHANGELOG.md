# Changelog

All notable changes to TRITIUM-Watcher will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Initial architecture diagram
- Comprehensive API reference documentation
- Contributing guidelines
- Configuration documentation
- Comparison with competitor tools

---

## [0.1.0] - 2026-03-15

### Added
- Core FastMCP server implementation
- `distill_essence` tool for smart content extraction
- `set_watchdog` tool for persistent URL monitoring
- `list_watchdogs` and `clear_watchdogs` management tools
- Playwright-based web scraping with Chromium
- Trafilatura content extraction and filtering
- Screenshot capture with keyword highlighting
- Local JSON persistence
- Apify Key-Value Store cloud persistence
- WATCHDOG_LOG.md for alert tracking
- Docker support
- Professional banner and branding
- README with quick start guide
- LICENSE files (dual licensing model)
- Privacy policy and terms of service
- Support documentation

### Security
- PolyForm Noncommercial License for personal use
- Commercial licensing requirement for business use

---

## Version Format

```
[X.Y.Z] - YYYY-MM-DD

Where:
- X = Major version (breaking changes)
- Y = Minor version (new features, backward compatible)
- Z = Patch version (bug fixes)
```

---

## Categories

- **Added** - New features
- **Changed** - Changes to existing functionality
- **Deprecated** - Soon-to-be removed features
- **Removed** - Removed features
- **Fixed** - Bug fixes
- **Security** - Security fixes or improvements

---

## Future Versions

### [0.2.0] - Planned

**Webhook Support**
- POST requests on keyword matches
- Configurable payload format
- Retry logic

**Export Formats**
- JSON export of watchdog logs
- CSV export for data analysis
- HTML report generation

**CLI Interface**
- Standalone CLI without MCP
- Interactive mode
- Batch operations

### [0.3.0] - Planned

**Advanced Features**
- Diff visualization between checks
- Multi-language keyword detection
- Scheduling options (cron-like)
- Rate limiting protection
- robots.txt compliance toggle

**User Experience**
- Better error messages
- Progress indicators
- Resource limit warnings
- Configuration validation UI

### [1.0.0] - Planned

**Production Ready**
- Full test coverage (>90%)
- Performance optimizations
- Comprehensive error handling
- Production deployment guide
- Security audit
- Documentation completeness

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to suggest changes to this changelog.

---

[Unreleased]: https://github.com/Aarav482011/TRITIUM-Watcher/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Aarav482011/TRITIUM-Watcher/releases/tag/v0.1.0
