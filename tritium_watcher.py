import asyncio
import logging
import sys
import os

# Silence FastMCP banner and upgrade notifications before importing FastMCP
os.environ["FASTMCP_LOG_LEVEL"] = "ERROR"
os.environ["FASTMCP_BANNER"] = "false"
os.environ["FASTMCP_SKIP_UPDATE_CHECK"] = "true"

import json
import re
from datetime import datetime
from typing import List, Dict, Optional
from fastmcp import FastMCP
from playwright.async_api import async_playwright
import trafilatura
from apify import ApifyClient

# Initialize the FastMCP server
mcp = FastMCP("TRITIUM-Watcher")

# Set up logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("tritium-watcher")

# Paths for persistence and logging
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WATCHDOGS_FILE = os.path.join(BASE_DIR, "watchdogs.json")
WATCHDOG_LOG_FILE = os.path.join(BASE_DIR, "WATCHDOG_LOG.md")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")

# Ensure directories exist
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Store active watchdogs: {watch_id: task}
active_tasks = {}

def get_apify_client():
    """Get ApifyClient if running in Apify environment."""
    token = os.environ.get("APIFY_TOKEN")
    if token:
        return ApifyClient(token)
    return None

def load_watchdogs() -> List[Dict]:
    """Load watchdogs from Apify Key-Value Store or local JSON file."""
    apify_client = get_apify_client()
    if apify_client:
        try:
            # Default Key-Value Store ID is in APIFY_DEFAULT_KEY_VALUE_STORE_ID
            store_id = os.environ.get("APIFY_DEFAULT_KEY_VALUE_STORE_ID")
            if store_id:
                record = apify_client.key_value_store(store_id).get_record("watchdogs")
                if record and record.get("value"):
                    return record["value"]
        except Exception as e:
            logger.error(f"Error loading watchdogs from Apify: {e}")
    
    # Fallback to local file
    if os.path.exists(WATCHDOGS_FILE):
        try:
            with open(WATCHDOGS_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading watchdogs locally: {e}")
    return []

def save_watchdogs(watchdogs: List[Dict]):
    """Save watchdogs to Apify Key-Value Store or local JSON file."""
    apify_client = get_apify_client()
    if apify_client:
        try:
            store_id = os.environ.get("APIFY_DEFAULT_KEY_VALUE_STORE_ID")
            if store_id:
                apify_client.key_value_store(store_id).set_record("watchdogs", watchdogs)
                return
        except Exception as e:
            logger.error(f"Error saving watchdogs to Apify: {e}")

    # Fallback to local file
    try:
        with open(WATCHDOGS_FILE, "w") as f:
            json.dump(watchdogs, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving watchdogs locally: {e}")

async def capture_screenshot(url: str, keyword: str) -> Optional[str]:
    """Captures a screenshot of the page where the keyword was found."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_url = re.sub(r'[^a-zA-Z0-9]', '_', url)[:30]
    filename = f"alert_{safe_url}_{timestamp}.png"
    filepath = os.path.join(SCREENSHOTS_DIR, filename)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto(url, timeout=30000)
            await page.wait_for_load_state("networkidle")
            
            # Try to find the element containing the keyword and highlight it
            # This is a bit advanced; we'll just take a full viewport screenshot for reliability
            # but we'll scroll to the keyword if possible.
            try:
                # Basic search for text and scroll into view
                locator = page.get_by_text(keyword, exact=False).first
                if await locator.count() > 0:
                    await locator.scroll_into_view_if_needed()
                    # Add a red border to the element for visual feedback
                    await locator.evaluate("el => el.style.border = '5px solid red'")
            except Exception as e:
                logger.warning(f"Could not highlight keyword: {e}")
                
            await page.screenshot(path=filepath)
            return filepath
        except Exception as e:
            logger.error(f"Error capturing screenshot for {url}: {e}")
            return None
        finally:
            await browser.close()

def log_alert(url: str, keyword: str, screenshot_path: Optional[str] = None):
    """Update the WATCHDOG_LOG.md file with a new alert."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    screenshot_link = ""
    if screenshot_path:
        rel_path = os.path.relpath(screenshot_path, BASE_DIR)
        screenshot_link = f"\n- **Screenshot**: [View Screenshot]({rel_path})"
    
    log_entry = (
        f"## 🚨 Watchdog Alert\n"
        f"- **Time**: {timestamp}\n"
        f"- **URL**: {url}\n"
        f"- **Keyword Match**: `{keyword}`\n"
        f"{screenshot_link}\n"
        f"- **Status**: Match Found\n\n---\n"
    )
    
    if not os.path.exists(WATCHDOG_LOG_FILE):
        with open(WATCHDOG_LOG_FILE, "w") as f:
            f.write("# 🛰 TRITIUM-Watcher Real-Time Alerts\n\n")
    
    with open(WATCHDOG_LOG_FILE, "a") as f:
        f.write(log_entry)
    logger.info(f"!!! WATCHDOG ALERT !!! Keyword '{keyword}' found at {url}")

async def scrape_url(url: str) -> str:
    """Helper function to scrape text from a URL using Playwright."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto(url, timeout=30000)
            await page.wait_for_load_state("networkidle")
            content = await page.content()
            return content
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return ""
        finally:
            await browser.close()

def extract_clean_text(html_content: str) -> str:
    """Extract clean text using trafilatura."""
    text = trafilatura.extract(html_content, include_comments=False, include_tables=True)
    return text if text else ""

@mcp.tool()
async def distill_essence(url: str) -> List[str]:
    """
    Scrapes a URL and returns the 5 most important sentences/data points.
    """
    logger.info(f"Distilling essence from: {url}")
    html = await scrape_url(url)
    if not html:
        return ["Failed to retrieve content from the URL."]
        
    text = extract_clean_text(html)
    if not text:
        return ["Trafilatura could not extract meaningful content from this page."]
    
    sentences = re.split(r'(?<=[.!?])\s+', text)
    valid_sentences = [s.strip() for s in sentences if len(s.split()) > 8]
    
    def score_sentence(s):
        score = len(s)
        if any(char.isdigit() for char in s): score += 30 
        if any(word[0].isupper() for word in s.split()[1:]): score += 15
        return score

    distilled = sorted(valid_sentences, key=score_sentence, reverse=True)[:5]
    return distilled if distilled else ["No significant data points found."]

async def watchdog_task(url: str, keywords: List[str]):
    """Background task that monitors a URL for multiple keywords."""
    logger.info(f"Started monitoring {url} for keywords: {keywords}")
    while True:
        try:
            html = await scrape_url(url)
            text = extract_clean_text(html)
            
            for kw in keywords:
                if kw.lower() in text.lower():
                    # Match found! Capture screenshot and log alert
                    screenshot_path = await capture_screenshot(url, kw)
                    log_alert(url, kw, screenshot_path)
            
            await asyncio.sleep(60)
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"Watchdog error for {url}: {e}")
            await asyncio.sleep(60)

@mcp.tool()
async def set_watchdog(url: str, keywords: str) -> str:
    """
    Sets a persistent watchdog on a URL to check for multiple keywords (comma-separated).
    """
    kw_list = [k.strip() for k in keywords.split(",") if k.strip()]
    if not kw_list:
        return "Please provide at least one keyword."
        
    watch_id = f"{url}" # Grouped by URL for multi-keyword efficiency
    if watch_id in active_tasks:
        # Stop old task to update with new keywords
        active_tasks[watch_id].cancel()
        logger.info(f"Updating watchdog for {url} with new keywords.")

    # Save to persistence
    watchdogs = load_watchdogs()
    # Update or add
    found = False
    for w in watchdogs:
        if w['url'] == url:
            w['keywords'] = kw_list
            found = True
            break
    if not found:
        watchdogs.append({"url": url, "keywords": kw_list})
    save_watchdogs(watchdogs)
    
    # Start the background task
    task = asyncio.create_task(watchdog_task(url, kw_list))
    active_tasks[watch_id] = task
    
    return f"Watchdog set for {url} with keywords: {', '.join(kw_list)}. Screenshots will be saved on match."

@mcp.tool()
async def list_watchdogs() -> List[str]:
    """Lists all persistent watchdogs."""
    watchdogs = load_watchdogs()
    return [f"{w['url']} (Keywords: {', '.join(w['keywords'])})" for w in watchdogs]

async def start_persistent_watchdogs():
    """Start tasks for all saved watchdogs on startup."""
    watchdogs = load_watchdogs()
    for w in watchdogs:
        watch_id = f"{w['url']}"
        if watch_id not in active_tasks:
            task = asyncio.create_task(watchdog_task(w['url'], w['keywords']))
            active_tasks[watch_id] = task
    if watchdogs:
        logger.info(f"Resumed {len(watchdogs)} persistent watchdogs.")

@mcp.tool()
async def clear_watchdogs() -> str:
    """Clears all persistent watchdogs and stops active tasks."""
    for task in active_tasks.values():
        task.cancel()
    active_tasks.clear()
    save_watchdogs([])
    return "All watchdogs cleared."

if __name__ == "__main__":
    # Apify uses APIFY_CONTAINER_PORT for web services. Default to 8000.
    port = int(os.getenv("APIFY_CONTAINER_PORT", 8000))
    
    # We can't use asyncio.run() because mcp.run() uses anyio.run() internally,
    # and you can't nest event loops. 
    # Instead, we'll use a threading approach to start the background tasks 
    # after the server has initialized its loop.
    
    import threading
    import time

    def run_background_init():
        # Wait a moment for the server to start
        time.sleep(2)
        try:
            # Try to get the loop that mcp.run() created
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(start_persistent_watchdogs())
        except Exception as e:
            logger.error(f"Background initialization failed: {e}")

    # Start a thread that will inject the background task into the loop
    # threading.Thread(target=run_background_init, daemon=True).start()
    
    # Actually, the simplest way for FastMCP v2 is to just run it.
    # Since we can't easily use on_startup, we will rely on the first tool call
    # or a manual trigger if needed, but for now let's just get the server running.
    
    logger.info(f"Starting TRITIUM-Watcher with SSE transport on port {port}")
    mcp.run(transport="sse", port=port)
