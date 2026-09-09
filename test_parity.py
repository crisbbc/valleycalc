#!/usr/bin/env python3
"""Run focused Golden Valley parity checks in a real Firefox page."""

import json
import queue
import shutil
import subprocess
import tempfile
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS = queue.Queue()

BROWSER_TEST = r"""
<script>
(async () => {
  const failures = [];
  const expect = (condition, message) => { if (!condition) failures.push(message); };
  const selectClass = document.querySelector("#character-class");
  const chips = () => [...document.querySelectorAll("#mini-stats span")].map(node => node.textContent);

  const classes = {
    Fighter: ["Damage Dealer, Main DPS", "Bonuses: +6 AT, +2 MG.", "ACTs SMITE · SKILL / SPELL · DEFEND · ITEMS", ["HP 5", "AT 11", "MG 7", "DF 5", "EN 5"]],
    Healer: ["Primarily Heals, Main Support", "Bonuses: +6 MG, +2 DF, +3 HP.", "ACTs HEAL · SKILL / SPELL · DEFEND · ITEMS", ["HP 8", "AT 5", "MG 11", "DF 7", "EN 5"]],
    Guardian: ["Frontline Damage Absorb/Sub DPS", "Bonuses: +6 DF, +2 AT, +5 HP.", "ACTs FIGHT · SKILL / SPELL · GUARD · ITEMS", ["HP 10", "AT 7", "MG 5", "DF 11", "EN 5"]],
    Caster: ["TP Abuser, Team Buffs/Enemy Debuffs, Sub Support", "Bonuses: +4 MG, +2 DF, +2 EN.", "ACTs BUFF · SKILL / SPELL · DEFEND · ITEMS", ["HP 5", "AT 5", "MG 9", "DF 7", "EN 7"]],
    Cheerleader: ["Versatile and Quick Revives, Sub Support/DPS", "Bonuses: +4 EN, +2 MG, +2 AT, +2 HP.", "ACTs FIGHT · SKILL / SPELL · TAUNT · ITEMS", ["HP 7", "AT 7", "MG 7", "DF 5", "EN 9"]]
  };

  for (const [name, [role, bonus, actions, stats]] of Object.entries(classes)) {
    selectClass.value = name;
    selectClass.dispatchEvent(new Event("change", { bubbles: true }));
    expect(document.querySelector("#preview-class").textContent === `${name} · ${role}`, `${name} role`);
    expect(document.querySelector("#class-bonus").textContent.startsWith(bonus), `${name} bonuses`);
    expect(chips().includes(actions), `${name} ACTs`);
    stats.forEach(stat => expect(chips().includes(stat), `${name} ${stat}`));
  }

  const soulQuotes = {
    Versatile: "You move with the stream, your Will floating past without hassle.",
    Durable: "You held your ground and kept pushing your Will onwards, even if slowly.",
    Passionate: "You took beating after beating, and still refused to change your Will.",
    Attentive: "You put yourself in harm's way so others could join in on your Will."
  };
  const soulGroups = {
    bravery_recklessness: "Passionate", enthusiasm_intensity: "Versatile", freedom_control: "Durable",
    insight_manipulation: "Versatile", integrity_ruthlessness: "Durable", justice_vengeance: "Passionate",
    kindness_sacrifice: "Attentive", loyalty_obsession: "Attentive", mindfulness_prejudice: "Passionate",
    patience_carelessness: "Versatile", perseverance_stubbornness: "Durable", protectiveness_subjugation: "Attentive"
  };

  for (const [id, group] of Object.entries(soulGroups)) {
    document.querySelector(`input[value="${id}"][data-variant="H"]`).click();
    expect(chips().includes(`SOUL · The ${group} — “${soulQuotes[group]}”`), `${id} group and quote`);
  }
  expect(document.querySelector("#preview-soul").alt === "Protectiveness / Subjugation soul", "Soul preview label");
  document.querySelector('input[value="freedom_control"][data-variant="H"]').click();
  expect(document.querySelector("#preview-soul").alt === "Will / Control soul", "Will label");

  await fetch("/__result", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ failures })
  });
})();
</script>
"""


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == "/__parity_test.html":
            page = (ROOT / "index.html").read_text().replace("</body>", BROWSER_TEST + "\n</body>")
            payload = page.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return
        super().do_GET()

    def do_POST(self):
        if self.path != "/__result":
            self.send_error(404)
            return
        payload = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        RESULTS.put(payload)
        self.send_response(204)
        self.end_headers()


def main():
    firefox = shutil.which("firefox")
    if not firefox:
        raise SystemExit("FAIL: Firefox is required for the parity test")

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()

    with tempfile.TemporaryDirectory() as profile:
        process = subprocess.Popen(
            [firefox, "--headless", "--no-remote", "--profile", profile,
             f"http://127.0.0.1:{server.server_port}/__parity_test.html"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        try:
            result = RESULTS.get(timeout=20)
        except queue.Empty:
            process.terminate()
            _, stderr = process.communicate(timeout=5)
            raise SystemExit("FAIL: Firefox did not return test results\n" + "\n".join(stderr.splitlines()[-10:]))
        finally:
            server.shutdown()
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()

    if result["failures"]:
        raise SystemExit("FAIL:\n- " + "\n- ".join(result["failures"]))
    print("PASS: Firefox rendered all class bonuses/roles/ACTs and all 12 Soul group mappings")


if __name__ == "__main__":
    main()
