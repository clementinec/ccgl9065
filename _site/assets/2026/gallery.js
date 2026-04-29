/* CCGL9065 · 2026 Exhibition gallery
 * Single file, two modes (public, curator), driven by data-mode on .ex2026 root.
 */
(function () {
  "use strict";

  const root = document.querySelector(".ex2026");
  if (!root) return;

  const mode = root.dataset.mode || "public";
  const isCurator = mode === "curator";

  // ----------- Curator expiry gate -----------
  // Hong Kong is UTC+8; "EOD Apr 29, 2026" = midnight HKT = 2026-04-29T16:00:00Z
  const EXPIRY_UTC = Date.parse("2026-04-29T16:00:00Z");
  if (isCurator && Date.now() > EXPIRY_UTC) {
    root.innerHTML = `
      <section class="ex2026__expired">
        <h2>Exhibition closed</h2>
        <p>This presentation tool expired at end of day 29 April 2026.<br>
        The public exhibition remains available.</p>
      </section>`;
    return;
  }

  const dataUrl = isCurator
    ? "data/students_2026_curator.json"
    : "data/students_2026_public.json";

  // ----------- Element refs -----------
  const stage = root.querySelector("[data-stage]");
  const mosaic = root.querySelector("[data-mosaic]");
  const counterEl = root.querySelector("[data-counter]");
  const nextBtn = root.querySelector("[data-next]");
  const prevBtn = root.querySelector("[data-prev]");
  const shuffleBtn = root.querySelector("[data-shuffle]");
  const searchEmail = root.querySelector("[data-search-email]");
  const searchName = root.querySelector("[data-search-name]");
  const resultsEl = root.querySelector("[data-results]");

  let portfolios = [];
  let order = [];      // shuffled index sequence for "next"
  let cursor = 0;

  // ----------- Helpers -----------
  function shuffle(arr) {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  function escapeHtml(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, c =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }

  function placeholderSvg() {
    return `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <rect x="3" y="3" width="18" height="18" rx="1"/>
      <circle cx="8.5" cy="8.5" r="1.5"/>
      <path d="m21 15-5-5L5 21"/></svg>`;
  }

  function renderCollage(p) {
    const c = p.collage || {};
    if (c.kind === "canva" && c.url) {
      return `<iframe src="${escapeHtml(c.url)}" allow="fullscreen" loading="lazy"></iframe>`;
    }
    if (c.kind === "drive" && c.url) {
      // Convert standard share URL to embeddable preview URL
      const m = c.url.match(/\/file\/d\/([^/]+)/);
      const embed = m ? `https://drive.google.com/file/d/${m[1]}/preview` : c.url;
      return `<iframe src="${escapeHtml(embed)}" allow="autoplay" loading="lazy"></iframe>`;
    }
    if (c.kind === "local_pdf" && c.url) {
      // Show the rendered first-page thumb as the visible image; full PDF available via essay link.
      const thumb = p.thumb;
      if (thumb) return `<img src="${escapeHtml(thumb)}" alt="">`;
      return `<iframe src="${escapeHtml(c.url)}" loading="lazy"></iframe>`;
    }
    if (c.url && (c.kind === "ibb_direct" || c.kind === "local_image" || c.kind === "ibb_page")) {
      return `<img src="${escapeHtml(c.url)}" alt="" loading="lazy">`;
    }
    return `<div class="ex2026__placeholder">${placeholderSvg()}<span>Collage pending</span></div>`;
  }

  function renderVideo(p) {
    const v = p.video || {};
    if (v.kind === "youtube" && v.url) {
      return `<div class="ex2026__video-wrap"><iframe src="${escapeHtml(v.url)}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe></div>`;
    }
    if (v.kind === "local" && v.url) {
      return `<div class="ex2026__video-wrap"><video src="${escapeHtml(v.url)}" controls preload="metadata" playsinline></video></div>`;
    }
    return `<div class="ex2026__placeholder" style="aspect-ratio:16/9;min-height:0">${placeholderSvg()}<span>Video pending</span></div>`;
  }

  function renderEssay(p) {
    const e = p.essay || {};
    if (e.available && e.url) {
      return `<a class="ex2026__essay-link" href="${escapeHtml(e.url)}" target="_blank" rel="noopener">
        Read full essay
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 17l10-10M7 7h10v10"/></svg>
      </a>`;
    }
    return `<span class="ex2026__hint">Essay pending</span>`;
  }

  function renderCard(p) {
    if (!p) return "";
    const num = p.id ? p.id.toUpperCase() : "—";
    const title = isCurator ? p.name : p.title;
    const subtitle = isCurator
      ? `<div class="ex2026__hint" style="margin-top:.25rem">${escapeHtml(p.email || "")} · #${escapeHtml(p.student_number || "")}</div>`
      : "";
    return `
      <article class="ex2026__card">
        <div class="ex2026__card-collage">${renderCollage(p)}</div>
        <div class="ex2026__card-meta">
          <div class="ex2026__card-num">№ ${escapeHtml(num)}</div>
          <h2 class="ex2026__card-title">${escapeHtml(title || "Untitled")}</h2>
          ${subtitle}
          <div class="ex2026__card-section">
            <h3>Video Essay</h3>
            ${renderVideo(p)}
          </div>
          <div class="ex2026__card-section">
            <h3>Reflective Essay</h3>
            ${renderEssay(p)}
          </div>
        </div>
      </article>`;
  }

  function showAt(idx) {
    cursor = ((idx % portfolios.length) + portfolios.length) % portfolios.length;
    const p = portfolios[order[cursor]];
    if (stage) stage.innerHTML = renderCard(p);
    if (counterEl) counterEl.textContent = `${cursor + 1} / ${portfolios.length}`;
  }

  function renderMosaic() {
    if (!mosaic) return;
    const tiles = portfolios.map((p, i) => {
      const label = isCurator ? p.name : p.title;
      if (p.thumb) {
        return `<button class="ex2026__tile" data-jump="${i}" type="button" aria-label="${escapeHtml(label)}">
          <img src="${escapeHtml(p.thumb)}" alt="" loading="lazy">
          <div class="ex2026__tile-label">№ ${p.id.toUpperCase()} · ${escapeHtml(label)}</div>
        </button>`;
      }
      return `<button class="ex2026__tile ex2026__tile--placeholder" data-jump="${i}" type="button">
        ${escapeHtml(p.id.toUpperCase())}<br>${escapeHtml(label)}
      </button>`;
    }).join("");
    mosaic.innerHTML = tiles;
    mosaic.addEventListener("click", e => {
      const btn = e.target.closest("[data-jump]");
      if (!btn) return;
      const target = parseInt(btn.dataset.jump, 10);
      cursor = order.indexOf(target);
      showAt(cursor);
      stage?.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }

  // ----------- Curator search -----------
  function renderResults(query) {
    if (!resultsEl) return;
    const q = (query || "").toLowerCase().trim();
    const matches = q
      ? portfolios.filter(p => {
          const fields = [p.name, p.email, p.first_name, p.last_name, p.student_number]
            .filter(Boolean).map(s => s.toLowerCase());
          return fields.some(f => f.includes(q));
        })
      : portfolios;

    const html = matches.map(p => {
      const c = p.collage?.url ? "present" : "missing";
      const v = p.video?.url ? "present" : "missing";
      const e = p.essay?.available ? "present" : "missing";
      return `<button class="ex2026__result" data-jump="${portfolios.indexOf(p)}" type="button">
        ${p.thumb
          ? `<img src="${escapeHtml(p.thumb)}" alt="">`
          : `<div style="width:80px;height:80px;background:var(--ex-bg);border:1px dashed var(--ex-rule)"></div>`}
        <div class="ex2026__result-info">
          <strong>${escapeHtml(p.name)}</strong>
          <span>${escapeHtml(p.email)} · ${escapeHtml(p.student_number)} · № ${p.id.toUpperCase()}</span>
        </div>
        <div class="ex2026__badges">
          <span class="ex2026__badge ex2026__badge--${c}">C</span>
          <span class="ex2026__badge ex2026__badge--${v}">V</span>
          <span class="ex2026__badge ex2026__badge--${e}">E</span>
        </div>
      </button>`;
    }).join("");
    resultsEl.innerHTML = html || `<div class="ex2026__loading">No matches</div>`;
    resultsEl.querySelectorAll("[data-jump]").forEach(btn => {
      btn.addEventListener("click", () => {
        const idx = parseInt(btn.dataset.jump, 10);
        cursor = order.indexOf(idx);
        showAt(cursor);
        stage?.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    });
  }

  function combinedQuery() {
    const a = (searchEmail?.value || "").trim();
    const b = (searchName?.value || "").trim();
    return [a, b].filter(Boolean).join(" ");
  }

  // ----------- Wire up -----------
  function init(data) {
    portfolios = data.portfolios || [];
    if (!portfolios.length) {
      if (stage) stage.innerHTML = `<div class="ex2026__loading">No portfolios yet</div>`;
      return;
    }
    order = shuffle(portfolios.map((_, i) => i));
    showAt(0);
    renderMosaic();
    if (isCurator) renderResults("");

    nextBtn?.addEventListener("click", () => showAt(cursor + 1));
    prevBtn?.addEventListener("click", () => showAt(cursor - 1));
    shuffleBtn?.addEventListener("click", () => {
      order = shuffle(portfolios.map((_, i) => i));
      showAt(0);
    });

    searchEmail?.addEventListener("input", () => renderResults(combinedQuery()));
    searchName?.addEventListener("input", () => renderResults(combinedQuery()));

    document.addEventListener("keydown", e => {
      if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA") return;
      if (e.key === "ArrowRight" || e.key === " ") { e.preventDefault(); showAt(cursor + 1); }
      else if (e.key === "ArrowLeft") showAt(cursor - 1);
      else if (e.key.toLowerCase() === "s") shuffleBtn?.click();
    });
  }

  fetch(dataUrl)
    .then(r => r.json())
    .then(init)
    .catch(err => {
      console.error("Failed to load gallery data:", err);
      if (stage) stage.innerHTML = `<div class="ex2026__loading">Could not load portfolios</div>`;
    });
})();
