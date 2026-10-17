"""Optional real-browser acceptance: install Playwright and its three browsers first."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

from unfinished_series_dashboard.cli import main
from unfinished_series_dashboard.core import load_dashboard


def check_browser(browser_type, directory: Path) -> dict:
    source = directory / "input.json"
    original = {
        "version": 1,
        "series": [
            {
                "id": "keep",
                "title": "Keep",
                "status": "delayed",
                "next_release": "unknown",
                "notes": "Private",
                "extra": {"bool": True},
            },
            {"id": "remove", "title": "Remove", "status": "complete", "next_release": None},
        ],
    }
    source.write_text(json.dumps(original))
    before = source.read_bytes()
    html = directory / "editor.html"
    assert (
        main([str(source), "--as-of", "2026-10-17", "--format", "html", "--output", str(html)]) == 0
    )
    browser = browser_type.launch()
    page = browser.new_page(accept_downloads=True)
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    dialog_action = {"accept": True}
    dialogs = []

    def handle_dialog(dialog):
        dialogs.append(dialog.type)
        dialog.accept() if dialog_action["accept"] else dialog.dismiss()

    page.on("dialog", handle_dialog)
    page.goto(html.as_uri())
    page.locator("#add-id").fill("keep")
    page.locator("#add-title").fill("Duplicate")
    page.locator("#add-series").click()
    assert "unique" in page.locator("#status").inner_text()
    assert page.locator("#entries > section").count() == 2
    page.locator("#add-id").fill("new")
    page.locator("#add-title").fill("<img src=x onerror=alert(1)> New | Series")
    page.locator("#add-status").select_option("still-writing")
    page.locator("#add-series").click()
    assert page.locator("#entries > section").count() == 3
    assert page.locator("img").count() == 0
    card = page.locator('section[data-id="new"]')
    card.get_by_label("Completed volumes", exact=True).fill("1.5")
    assert not card.get_by_label("Completed volumes", exact=True).evaluate(
        "input => input.checkValidity()"
    )
    downloads = []
    page.on("download", lambda download: downloads.append(download))
    page.locator("#download").click()
    page.wait_for_timeout(100)
    assert not downloads
    card.get_by_label("Completed volumes", exact=True).fill("2")
    card.get_by_label("Total volumes", exact=True).fill("5")
    assert "2 of 5 completed" in card.inner_text()
    dialog_action["accept"] = False
    page.get_by_role("button", name="Remove series: Remove", exact=True).click()
    assert page.locator("#entries > section").count() == 3
    assert dialogs[-1] == "confirm"
    dialog_action["accept"] = True
    page.get_by_role("button", name="Remove series: Remove", exact=True).click()
    assert page.locator("#entries > section").count() == 2
    with page.expect_download() as download:
        page.locator("#download").click()
    saved = directory / "edited.json"
    download.value.save_as(saved)
    result = load_dashboard(saved)
    assert result["series"][0] == original["series"][0]
    assert result["series"][1]["id"] == "new"
    assert result["series"][1]["completed_volumes"] == 2
    assert result["series"][1]["total_volumes"] == 5
    assert (
        main([str(saved), "--format", "json", "--output", str(directory / "validated.json")]) == 0
    )
    page.get_by_role("button", name="Remove series: Keep", exact=True).click()
    card.get_by_role("button", name="Remove series").click()
    with page.expect_download() as empty:
        page.locator("#download").click()
    empty_path = directory / "empty.json"
    empty.value.save_as(empty_path)
    assert load_dashboard(empty_path)["series"] == []
    page.locator("#add-id").fill("restart")
    page.locator("#add-title").fill("Restart")
    page.locator("#add-series").click()
    assert page.locator("#entries > section").count() == 1
    dialog_action["accept"] = False
    page.evaluate("location.reload()")
    page.wait_for_timeout(200)
    assert dialogs[-1] == "beforeunload"
    assert page.locator('section[data-id="restart"]').count() == 1
    dialog_action["accept"] = True
    page.reload()
    assert page.locator("#entries > section").count() == 2
    page.locator("#add-id").fill("guard")
    page.locator("#add-title").fill("Guard")
    page.locator("#add-series").click()
    dialog_action["accept"] = False
    page.evaluate("location.href='about:blank'")
    page.wait_for_timeout(200)
    assert dialogs[-1] == "beforeunload"
    assert page.locator('section[data-id="guard"]').count() == 1
    with page.expect_download() as exported:
        page.locator("#download").click()
    exported.value.save_as(directory / "guard.json")
    assert len(load_dashboard(directory / "guard.json")["series"]) == 3
    page.locator("#mark-saved").click()
    count = len(dialogs)
    page.reload()
    assert len(dialogs) == count
    keep = page.locator('section[data-id="keep"]')
    keep.get_by_label("Title", exact=True).fill("Edited again")
    assert page.locator("#mark-saved").is_disabled()
    page.evaluate("location.reload()")
    page.wait_for_timeout(200)
    assert dialogs[-1] == "beforeunload"
    assert keep.get_by_label("Title", exact=True).input_value() == "Edited again"
    dialog_action["accept"] = True
    page.reload()
    page.locator("#add-id").fill("unfinished-form")
    count = len(downloads)
    page.locator("#download").click()
    page.wait_for_timeout(100)
    assert len(downloads) == count
    assert "clear its fields" in page.locator("#status").inner_text()
    dialog_action["accept"] = False
    page.evaluate("location.reload()")
    page.wait_for_timeout(200)
    assert dialogs[-1] == "beforeunload"
    assert page.locator("#add-id").input_value() == "unfinished-form"
    page.get_by_role("button", name="Clear new series", exact=True).click()
    count = len(dialogs)
    page.reload()
    assert len(dialogs) == count
    assert source.read_bytes() == before
    assert not errors, errors
    browser.close()
    return {"browser": browser_type.name, "status": "pass", "source_unchanged": True}


def run() -> None:
    with tempfile.TemporaryDirectory() as directory, sync_playwright() as playwright:
        results = []
        for browser in (playwright.chromium, playwright.firefox, playwright.webkit):
            target = Path(directory) / browser.name
            target.mkdir()
            results.append(check_browser(browser, target))
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    run()
