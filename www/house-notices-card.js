class HouseNoticesCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._config = {};
    this._hass = null;
    this._expanded = null;
    this._detailItemId = null;
    this._collapsedSections = new Set(["upcoming"]);
    this._dismissedHistoryIds = new Set();
  }

  setConfig(config) {
    this._config = config || {};
    this.render();
  }

  set hass(hass) {
    this._hass = hass;
    this.render();
  }

  getCardSize() {
    return 8;
  }

  get timelineEntity() {
    return this._config.timeline_entity || "sensor.house_notice_timeline";
  }

  get historyEntity() {
    return this._config.history_entity || "sensor.house_notice_history";
  }

  get cardTitle() {
    return this._config.title || "Notification center";
  }

  get showTitle() {
    return this._config.show_title !== false;
  }

  parseJson(value, fallback = []) {
    if (!value || value === "unknown" || value === "unavailable") return fallback;
    if (Array.isArray(value)) return value;
    try {
      return JSON.parse(value);
    } catch (_err) {
      return fallback;
    }
  }

  parseDate(value) {
    if (!value || ["unknown", "unavailable", "none"].includes(String(value))) return null;
    const text = String(value).trim();
    const isoDate = /^\d{4}-\d{2}-\d{2}$/.test(text) ? `${text}T12:00:00` : text.replace(" ", "T");
    const parsed = new Date(isoDate);
    return Number.isNaN(parsed.getTime()) ? null : parsed;
  }

  dayStart(date) {
    return new Date(date.getFullYear(), date.getMonth(), date.getDate());
  }

  isInUpcomingWindow(item) {
    const date = this.parseDate(item?.date);
    if (!date) return false;
    const today = this.dayStart(new Date());
    const target = this.dayStart(date);
    const horizon = new Date(today);
    horizon.setDate(horizon.getDate() + 365);
    return target >= today && target <= horizon;
  }

  formatDate(value, opts = {}) {
    const date = this.parseDate(value);
    if (!date) return "";
    return new Intl.DateTimeFormat(undefined, {
      month: "short",
      day: "numeric",
      year: opts.year === false ? undefined : "numeric",
    }).format(date);
  }

  formatRecentTime(value) {
    const date = this.parseDate(value);
    if (!date) return "";
    const today = this.dayStart(new Date());
    const day = this.dayStart(date);
    const diff = Math.round((day - today) / 86400000);
    const time = new Intl.DateTimeFormat(undefined, { hour: "numeric", minute: "2-digit" }).format(date);
    if (diff === 0) return `Today ${time}`;
    if (diff === -1) return `Yesterday ${time}`;
    return `${new Intl.DateTimeFormat(undefined, { month: "short", day: "numeric" }).format(date)} ${time}`;
  }

  relativeDate(value) {
    const date = this.parseDate(value);
    if (!date) return "";
    const today = this.dayStart(new Date());
    const target = this.dayStart(date);
    const days = Math.round((target - today) / 86400000);
    if (days === 0) return "today";
    if (days === 1) return "tomorrow";
    if (days === -1) return "yesterday";
    if (days < 0) {
      const past = Math.abs(days);
      if (past < 45) return `${past} days ago`;
      if (past < 365) return `${Math.max(1, Math.round(past / 30.44))} months ago`;
      return `${Math.max(1, Math.round(past / 365.25))} years ago`;
    }
    if (days < 45) return `in ${days} days`;
    if (days < 365) return `in ${Math.max(1, Math.round(days / 30.44))} months`;
    return `in ${Math.max(1, Math.round(days / 365.25))} years`;
  }

  metaLine(item) {
    const parts = [];
    const date = this.formatDate(item.date);
    const rel = this.relativeDate(item.date);
    if (date) parts.push(`${item.due_prefix || "Due"} ${date}`);
    if (rel) parts.push(rel);
    const basis = this.basisLine(item);
    if (basis) parts.push(basis);
    return parts.join(" · ");
  }

  basisLine(item) {
    if (item.basis) return item.basis;
    if (!item.basis_date || !item.basis_prefix) return "";
    const date = this.formatDate(item.basis_date);
    if (!date) return "";
    return `${item.basis_prefix} ${date}${item.basis_suffix ? ` ${item.basis_suffix}` : ""}`;
  }

  normalizeItems(items) {
    return (items || [])
      .map((item, index) => ({
        id: item.id || `${item.title || "notice"}-${index}`,
        title: item.title || "House notice",
        emoji: item.emoji || "",
        state: item.state || "upcoming",
        severity: item.severity || "info",
        group: item.group || "House",
        narrative: item.narrative || "",
        sortTime: this.parseDate(item.date)?.getTime() || Number.MAX_SAFE_INTEGER,
        ...item,
      }))
      .sort((a, b) => a.sortTime - b.sortTime || a.title.localeCompare(b.title));
  }

  recentHistory(events) {
    const cutoff = Date.now() - 14 * 86400000;
    const sorted = (events || [])
      .map((event, index) => ({
        id: `${event.at || "event"}-${event.tag || ""}-${event.kind || ""}-${index}`,
        kind: event.kind || "sent",
        title: event.title || event.tag || "House notice",
        message: event.message || "",
        severity: event.severity || "info",
        atTime: this.parseDate(event.at)?.getTime() || 0,
        ...event,
      }))
      .filter((event) => event.atTime >= cutoff)
      .sort((a, b) => b.atTime - a.atTime);
    const openSentTags = new Set();
    const filtered = [];
    [...sorted].reverse().forEach((event) => {
      const tag = event.tag || "";
      if (event.kind === "clear") {
        if (!tag || !openSentTags.has(tag)) return;
        openSentTags.delete(tag);
        return;
      }
      if (this.isHousekeepingHistoryEvent(event)) return;
      filtered.push(event);
      if (event.kind === "sent" && tag) openSentTags.add(tag);
    });
    return filtered.reverse().slice(0, 24);
  }

  isHousekeepingHistoryEvent(event) {
    const title = String(event.title || "").trim().toLowerCase();
    const message = String(event.message || "").trim().toLowerCase();
    const tag = String(event.tag || "").trim().toLowerCase();
    const action = String(event.action || event.message || event.title || "").toUpperCase();
    const combined = `${title} ${message} ${tag} ${action}`.toLowerCase();
    if (event.kind === "action" && !this.keepActionInRecent(event)) return true;
    if (combined.includes("garden_mark_watered") || combined.includes("mark watered")) return true;
    return title === "house reminder sleeping"
      || title === "wine cave guardrail"
      || tag.endsWith("-snooze")
      || message.includes("reminders paused");
  }

  keepActionInRecent(event) {
    const recent = String(event.recent ?? "").toLowerCase();
    const keepRecent = String(event.keep_recent ?? "").toLowerCase();
    const history = String(event.history ?? "").toLowerCase();
    return event.recent === true
      || event.keep_recent === true
      || ["true", "on", "1", "yes"].includes(recent)
      || ["true", "on", "1", "yes"].includes(keepRecent)
      || history === "recent";
  }

  render() {
    if (!this.shadowRoot) return;
    const timelineState = this._hass?.states?.[this.timelineEntity];
    const historyState = this._hass?.states?.[this.historyEntity];
    const items = this.normalizeItems(this.parseJson(timelineState?.attributes?.items_json, []));
    const history = this.recentHistory(this.parseJson(historyState?.attributes?.events_json, []))
      .filter((event) => !this._dismissedHistoryIds.has(event.id));
    const attention = items.filter((item) => ["active", "due"].includes(item.state));
    const upcoming = items.filter((item) => !["active", "due"].includes(item.state) && this.isInUpcomingWindow(item));
    const detailItem = this._detailItemId ? items.find((item) => item.id === this._detailItemId) : null;
    if (this._detailItemId && !detailItem) this._detailItemId = null;

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          color: var(--primary-text-color);
          --notice-surface: rgba(15, 23, 42, 0.58);
          --notice-surface-strong: rgba(15, 23, 42, 0.76);
          --notice-line: rgba(148, 163, 184, 0.18);
          --notice-muted: rgba(226, 232, 240, 0.68);
          --notice-soft: rgba(226, 232, 240, 0.1);
        }
        .wrap {
          display: flex;
          flex-direction: column;
          gap: 18px;
          padding: 0 0 22px;
        }
        .page-head {
          padding: 4px 2px 0;
        }
        .page-title {
          color: #f8fafc;
          font-size: 30px;
          font-weight: 580;
          line-height: 1.1;
        }
        .section {
          border: 1px solid var(--notice-line);
          border-radius: 24px;
          background: var(--notice-surface);
          backdrop-filter: blur(16px);
          -webkit-backdrop-filter: blur(16px);
          overflow: hidden;
        }
        .section-head {
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 12px;
          padding: 16px 18px 8px;
        }
        .section-head.collapsible {
          cursor: pointer;
          user-select: none;
        }
        .section.collapsed .section-head {
          min-height: 64px;
          padding: 0 18px;
        }
        .section-title {
          color: #f8fafc;
          font-size: 15px;
          font-weight: 620;
          line-height: 1.2;
        }
        .section.collapsed .section-title {
          line-height: 1;
        }
        .section-head-right {
          display: inline-flex;
          align-items: center;
          justify-content: flex-end;
          gap: 8px;
          min-width: 0;
        }
        .section-count {
          color: rgba(226, 232, 240, 0.56);
          font-size: 12px;
          line-height: 1;
          display: inline-flex;
          align-items: center;
          min-height: 24px;
          white-space: nowrap;
        }
        .section-toggle {
          width: 24px;
          height: 24px;
          flex: 0 0 24px;
          border-radius: 999px;
          display: grid;
          place-items: center;
          color: rgba(226, 232, 240, 0.58);
          background: rgba(248, 250, 252, 0.05);
          border: 1px solid rgba(148, 163, 184, 0.12);
        }
        .section-toggle ha-icon {
          --mdc-icon-size: 17px;
        }
        .rows {
          padding: 0 16px 6px;
        }
        .row {
          min-width: 0;
          display: grid;
          grid-template-columns: 36px minmax(0, 1fr) auto;
          column-gap: 12px;
          align-items: start;
          padding: 14px 0;
          border-bottom: 1px solid rgba(148, 163, 184, 0.14);
          cursor: pointer;
        }
        .row.has-inline-action {
          grid-template-columns: 36px minmax(0, 1fr) auto auto;
        }
        .row:last-child {
          border-bottom: none;
        }
        .mark {
          width: 36px;
          height: 36px;
          border-radius: 999px;
          display: grid;
          place-items: center;
          background: rgba(148, 163, 184, 0.13);
          font-size: 17px;
          line-height: 1;
        }
        .emoji-mark {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          gap: 1px;
          overflow: hidden;
        }
        .emoji-mark span {
          display: block;
          line-height: 1;
        }
        .mark ha-icon {
          --mdc-icon-size: 18px;
          color: rgba(226, 232, 240, 0.72);
        }
        .copy {
          min-width: 0;
        }
        .title-line {
          display: flex;
          align-items: center;
          gap: 8px;
          min-width: 0;
        }
        .title {
          color: #f8fafc;
          font-size: 15px;
          font-weight: 600;
          line-height: 1.25;
          overflow-wrap: anywhere;
        }
        .pill {
          border-radius: 999px;
          padding: 3px 7px;
          color: rgba(248, 250, 252, 0.86);
          font-size: 10px;
          line-height: 1.1;
          white-space: nowrap;
          background: rgba(148, 163, 184, 0.16);
          border: 1px solid rgba(148, 163, 184, 0.12);
        }
        .pill.active,
        .pill.due {
          background: rgba(251, 191, 36, 0.16);
          border-color: rgba(251, 191, 36, 0.22);
          color: #fde68a;
        }
        .meta {
          margin-top: 5px;
          color: rgba(226, 232, 240, 0.66);
          font-size: 12px;
          line-height: 1.4;
          overflow-wrap: anywhere;
        }
        .narrative {
          margin-top: 4px;
          color: rgba(226, 232, 240, 0.48);
          font-size: 12px;
          line-height: 1.45;
          overflow-wrap: anywhere;
        }
        .chev {
          color: rgba(226, 232, 240, 0.42);
          padding-top: 4px;
        }
        .chev ha-icon {
          --mdc-icon-size: 18px;
        }
        .inline-actions {
          display: flex;
          align-items: flex-start;
          justify-content: flex-end;
          padding-top: 1px;
        }
        button.inline-primary {
          min-height: 30px;
          padding: 0 11px;
          background: rgba(34, 197, 94, 0.18);
          border-color: rgba(74, 222, 128, 0.28);
          color: #dcfce7;
          font-weight: 650;
          white-space: nowrap;
        }
        @media (max-width: 430px) {
          .row.has-inline-action {
            grid-template-columns: 36px minmax(0, 1fr) auto;
          }
          .row.has-inline-action .inline-actions {
            grid-column: 2 / -1;
            grid-row: 2;
            justify-content: flex-start;
            padding-top: 8px;
          }
          .row.has-inline-action .chev {
            grid-column: 3;
            grid-row: 1;
          }
          .row.has-inline-action .detail {
            grid-column: 1 / -1;
          }
        }
        .detail {
          grid-column: 2 / -1;
          margin-top: 12px;
          border-radius: 18px;
          border: 1px solid rgba(148, 163, 184, 0.14);
          background: rgba(2, 6, 23, 0.22);
          padding: 12px;
          cursor: default;
        }
        .detail-text {
          color: rgba(248, 250, 252, 0.78);
          font-size: 13px;
          line-height: 1.45;
          overflow-wrap: anywhere;
        }
        .actions {
          display: flex;
          flex-wrap: wrap;
          gap: 8px;
          margin-top: 12px;
        }
        button {
          appearance: none;
          border: 1px solid rgba(148, 163, 184, 0.16);
          border-radius: 999px;
          background: rgba(248, 250, 252, 0.1);
          color: #f8fafc;
          min-height: 32px;
          padding: 0 12px;
          font: inherit;
          font-size: 12px;
          line-height: 1;
          cursor: pointer;
        }
        button.primary {
          background: rgba(59, 130, 246, 0.26);
          border-color: rgba(96, 165, 250, 0.34);
        }
        .sheet-backdrop {
          position: fixed;
          inset: 0;
          z-index: 30;
          display: flex;
          align-items: flex-end;
          justify-content: center;
          padding: 18px 14px 0;
          background: rgba(2, 6, 23, 0.58);
          backdrop-filter: blur(18px);
          -webkit-backdrop-filter: blur(18px);
        }
        .detail-sheet {
          width: min(100%, 560px);
          max-height: min(88vh, 760px);
          overflow: auto;
          border: 1px solid rgba(148, 163, 184, 0.22);
          border-bottom: none;
          border-radius: 28px 28px 0 0;
          background:
            linear-gradient(180deg, rgba(15, 23, 42, 0.98), rgba(2, 6, 23, 0.98));
          box-shadow: 0 -20px 80px rgba(0, 0, 0, 0.42);
          outline: none;
        }
        .sheet-header {
          display: grid;
          grid-template-columns: 46px minmax(0, 1fr) auto;
          gap: 12px;
          align-items: start;
          padding: 18px 18px 14px;
          border-bottom: 1px solid rgba(148, 163, 184, 0.14);
        }
        .sheet-mark .mark {
          width: 44px;
          height: 44px;
          font-size: 20px;
          background: rgba(148, 163, 184, 0.16);
        }
        .sheet-copy {
          min-width: 0;
        }
        .sheet-title-line {
          display: flex;
          flex-wrap: wrap;
          align-items: center;
          gap: 8px;
          min-width: 0;
        }
        .sheet-title {
          color: #f8fafc;
          font-size: 18px;
          font-weight: 680;
          line-height: 1.2;
          overflow-wrap: anywhere;
        }
        .sheet-subtitle {
          margin-top: 5px;
          color: rgba(226, 232, 240, 0.6);
          font-size: 12px;
          line-height: 1.35;
        }
        button.sheet-close {
          width: 34px;
          height: 34px;
          min-height: 34px;
          padding: 0;
          display: grid;
          place-items: center;
          color: rgba(248, 250, 252, 0.88);
          background: rgba(248, 250, 252, 0.08);
        }
        button.sheet-close ha-icon {
          --mdc-icon-size: 18px;
        }
        .sheet-body {
          padding: 16px 18px 18px;
        }
        .sheet-section + .sheet-section {
          margin-top: 16px;
        }
        .sheet-section-title {
          margin-bottom: 7px;
          color: rgba(248, 250, 252, 0.92);
          font-size: 12px;
          font-weight: 700;
          letter-spacing: 0;
          text-transform: uppercase;
        }
        .sheet-summary,
        .sheet-copy-block {
          color: rgba(248, 250, 252, 0.78);
          font-size: 14px;
          line-height: 1.48;
          overflow-wrap: anywhere;
        }
        .fact-grid {
          display: grid;
          grid-template-columns: repeat(2, minmax(0, 1fr));
          gap: 8px;
        }
        .fact {
          border: 1px solid rgba(148, 163, 184, 0.14);
          border-radius: 14px;
          background: rgba(248, 250, 252, 0.07);
          padding: 10px 11px;
          color: rgba(248, 250, 252, 0.8);
          font-size: 12px;
          line-height: 1.35;
          overflow-wrap: anywhere;
        }
        .sheet-timeline {
          display: grid;
          gap: 8px;
        }
        .timeline-step {
          display: grid;
          grid-template-columns: 10px minmax(0, 1fr);
          gap: 10px;
          align-items: start;
          color: rgba(248, 250, 252, 0.78);
          font-size: 13px;
          line-height: 1.42;
        }
        .timeline-dot {
          width: 8px;
          height: 8px;
          margin-top: 5px;
          border-radius: 999px;
          background: rgba(96, 165, 250, 0.9);
          box-shadow: 0 0 0 4px rgba(96, 165, 250, 0.12);
        }
        .tracking-line {
          margin-top: 8px;
          color: rgba(226, 232, 240, 0.58);
          font-size: 12px;
          line-height: 1.42;
        }
        .sheet-actions {
          display: flex;
          flex-wrap: wrap;
          gap: 9px;
          margin-top: 18px;
          padding-top: 14px;
          border-top: 1px solid rgba(148, 163, 184, 0.14);
        }
        .sheet-actions button {
          min-height: 36px;
          padding: 0 14px;
          font-weight: 650;
        }
        @media (min-width: 640px) {
          .sheet-backdrop {
            align-items: center;
            padding: 24px;
          }
          .detail-sheet {
            border-bottom: 1px solid rgba(148, 163, 184, 0.22);
            border-radius: 28px;
            box-shadow: 0 24px 90px rgba(0, 0, 0, 0.5);
          }
        }
        @media (max-width: 420px) {
          .fact-grid {
            grid-template-columns: minmax(0, 1fr);
          }
          .sheet-actions button {
            flex: 1 1 auto;
          }
        }
        .history-head-actions {
          display: inline-flex;
          align-items: center;
          justify-content: flex-end;
          gap: 8px;
          min-width: 0;
        }
        button.history-clear-all {
          min-height: 24px;
          padding: 0 10px;
          border-radius: 999px;
          background: rgba(248, 113, 113, 0.13);
          border-color: rgba(248, 113, 113, 0.22);
          color: rgba(254, 202, 202, 0.9);
          font-size: 11px;
          font-weight: 650;
          white-space: nowrap;
        }
        .history-row {
          grid-template-columns: 36px minmax(0, 1fr);
          cursor: default;
        }
        .history-swipe {
          --clear-reveal: 0px;
          --clear-opacity: 0;
          --clear-red-alpha: 0;
          --clear-label-opacity: 0;
          position: relative;
          overflow: hidden;
          border-bottom: 1px solid rgba(148, 163, 184, 0.14);
        }
        .history-swipe:last-child {
          border-bottom: none;
        }
        .history-clear-reveal {
          position: absolute;
          inset: 0 0 0 auto;
          width: 92px;
          display: grid;
          place-items: center;
          background: rgba(239, 68, 68, var(--clear-red-alpha));
          color: rgba(255, 255, 255, 0.96);
          font-size: 12px;
          font-weight: 680;
          transform: translate3d(calc(92px - var(--clear-reveal)), 0, 0);
          opacity: var(--clear-opacity);
          transition: transform 170ms cubic-bezier(0.2, 0, 0, 1), opacity 150ms ease, background-color 150ms ease;
          will-change: transform, opacity;
        }
        .history-swipe.dismissing .history-clear-reveal {
          transform: translate3d(0, 0, 0);
          opacity: 1;
        }
        .history-clear-reveal span {
          opacity: var(--clear-label-opacity);
          transition: opacity 120ms ease;
        }
        .history-swipe.swiping .history-clear-reveal,
        .history-swipe.swiping .history-clear-reveal span,
        .history-swipe.swiping .history-row {
          transition: none;
        }
        .history-swipe.dismissing {
          --clear-red-alpha: 0.92;
        }
        .history-swipe.dismissing .history-clear-reveal span {
          opacity: 1;
        }
        .history-swipe .history-row {
          position: relative;
          z-index: 1;
          border-bottom: none;
          background: transparent;
          transition: transform 190ms cubic-bezier(0.2, 0, 0, 1), opacity 180ms ease;
          touch-action: pan-y;
          will-change: transform;
          backface-visibility: hidden;
        }
        .history-swipe.revealing .history-row,
        .history-swipe.dismissing .history-row {
          background: var(--notice-surface);
        }
        .history-swipe.dismissing .history-row {
          transform: translate3d(-110%, 0, 0);
          opacity: 0;
        }
        .history-row.clear {
          opacity: 0.56;
        }
        .empty {
          padding: 4px 18px 18px;
          color: rgba(226, 232, 240, 0.58);
          font-size: 13px;
          line-height: 1.45;
        }
        @media (max-width: 560px) {
          .row {
            grid-template-columns: 34px minmax(0, 1fr) auto;
            column-gap: 10px;
          }
          .detail {
            grid-column: 1 / 4;
          }
        }
      </style>
      <div class="wrap">
        ${this.showTitle ? `
          <header class="page-head">
            <h1 class="page-title">${this.escape(this.cardTitle)}</h1>
          </header>
        ` : ""}
        ${attention.length ? this.renderSection("Needs Attention", attention, { attention: true }) : ""}
        ${this.renderHistory(history)}
        ${this.renderSection("Upcoming", upcoming, { collapsible: true, sectionId: "upcoming" })}
      </div>
      ${detailItem ? this.renderDetailSheet(detailItem) : ""}
    `;
    this.bindEvents();
  }

  renderSection(title, items, opts = {}) {
    const sectionId = opts.sectionId || title.toLowerCase().replace(/\s+/g, "-");
    const collapsed = opts.collapsible && this._collapsedSections.has(sectionId);
    const toggle = opts.collapsible
      ? `<div class="section-toggle" aria-hidden="true"><ha-icon icon="${collapsed ? "mdi:chevron-right" : "mdi:chevron-down"}"></ha-icon></div>`
      : "";
    const rows = items.length
      ? items.map((item) => this.renderItem(item)).join("")
      : `<div class="empty">${opts.attention ? "No active notices." : "Nothing upcoming."}</div>`;
    return `
      <section class="section ${collapsed ? "collapsed" : ""}">
        <div class="section-head ${opts.collapsible ? "collapsible" : ""}" ${opts.collapsible ? `data-section-toggle="${this.escapeAttr(sectionId)}" role="button" tabindex="0" aria-expanded="${collapsed ? "false" : "true"}"` : ""}>
          <div class="section-title">${this.escape(title)}</div>
          <div class="section-head-right">
            <div class="section-count">${items.length ? this.escape(String(items.length)) : ""}</div>
            ${toggle}
          </div>
        </div>
        ${collapsed ? "" : `<div class="rows">${rows}</div>`}
      </section>
    `;
  }

  renderMark(item) {
    const emoji = item.emoji || "";
    if (emoji) {
      const mark = this.emojiParts(emoji)[0] || emoji;
      return `<div class="mark emoji-mark"><span>${this.escape(mark)}</span></div>`;
    }
    return `<div class="mark"><ha-icon icon="${this.escapeAttr(item.icon || "mdi:bell-outline")}"></ha-icon></div>`;
  }

  emojiParts(value) {
    const text = String(value || "").trim();
    if (!text) return [];
    if (typeof Intl !== "undefined" && Intl.Segmenter) {
      const segmenter = new Intl.Segmenter(undefined, { granularity: "grapheme" });
      return [...segmenter.segment(text)].map((part) => part.segment).filter(Boolean);
    }
    return Array.from(text);
  }

  isEmojiMark(value) {
    return /\p{Extended_Pictographic}/u.test(value) || /[\u{1F1E6}-\u{1F1FF}]/u.test(value);
  }

  splitLeadingEmoji(value) {
    const text = String(value || "").trim();
    const parts = this.emojiParts(text);
    const leading = [];
    while (parts.length && this.isEmojiMark(parts[0])) {
      leading.push(parts.shift());
      while (parts.length && !parts[0].trim()) parts.shift();
    }
    if (!leading.length) return { emoji: "", title: text };
    return {
      emoji: leading[leading.length - 1],
      title: parts.join("").trim() || text,
    };
  }

  renderItem(item) {
    const expanded = this._expanded === item.id;
    const stateLabel = item.state === "quiet" ? "current" : item.state;
    const actions = Array.isArray(item.actions) ? item.actions : [];
    const inlineActionIndex = actions.findIndex((action) => action.inline !== false && !action.confirm);
    const inlineAction = ["active", "due"].includes(item.state) && inlineActionIndex >= 0
      ? `<div class="inline-actions"><button class="inline-primary" data-action-for="${this.escapeAttr(item.id)}" data-action-index="${inlineActionIndex}">${this.escape(actions[inlineActionIndex].label || "Done")}</button></div>`
      : "";
    return `
      <div class="row ${inlineAction ? "has-inline-action" : ""}" data-row-id="${this.escapeAttr(item.id)}">
        ${this.renderMark(item)}
        <div class="copy">
          <div class="title-line">
            <div class="title">${this.escape(item.title)}</div>
            <div class="pill ${this.escapeAttr(item.state)}">${this.escape(stateLabel)}</div>
          </div>
          <div class="meta">${this.escape(this.metaLine(item))}</div>
          ${item.narrative ? `<div class="narrative">${this.escape(item.narrative)}</div>` : ""}
        </div>
        ${inlineAction}
        <div class="chev"><ha-icon icon="${expanded ? "mdi:chevron-up" : "mdi:chevron-down"}"></ha-icon></div>
        ${expanded ? this.renderDetail(item) : ""}
      </div>
    `;
  }

  renderDetail(item) {
    const actions = Array.isArray(item.actions) ? item.actions : [];
    const open = item.url ? `<button data-open="${this.escapeAttr(item.url)}">Open page</button>` : "";
    const more = `<button class="primary" data-detail-for="${this.escapeAttr(item.id)}">Details</button>`;
    const actionButtons = actions
      .map((action, index) => `<button data-action-for="${this.escapeAttr(item.id)}" data-action-index="${index}">${this.escape(action.label || "Done")}</button>`)
      .join("");
    return `
      <div class="detail">
        <div class="detail-text">${this.escape(item.narrative || this.metaLine(item))}</div>
        <div class="actions">${more}${actionButtons}${open}</div>
      </div>
    `;
  }

  renderDetailSheet(item) {
    const detail = this.noticeDetail(item);
    const stateLabel = item.state === "quiet" ? "current" : item.state;
    const facts = detail.facts.length
      ? `<div class="sheet-section">
          <div class="sheet-section-title">Why now</div>
          <div class="fact-grid">
            ${detail.facts.map((fact) => `<div class="fact">${this.escape(this.detailLine(fact))}</div>`).join("")}
          </div>
        </div>`
      : "";
    const after = detail.afterAction
      ? `<div class="sheet-section">
          <div class="sheet-section-title">What happens next</div>
          <div class="sheet-copy-block">${this.escape(detail.afterAction)}</div>
          ${detail.tracking ? `<div class="tracking-line">${this.escape(detail.tracking)}</div>` : ""}
        </div>`
      : "";
    const timeline = detail.timeline.length
      ? `<div class="sheet-section">
          <div class="sheet-section-title">Timeline</div>
          <div class="sheet-timeline">
            ${detail.timeline.map((step) => `
              <div class="timeline-step">
                <div class="timeline-dot" aria-hidden="true"></div>
                <div>${this.escape(this.detailLine(step))}</div>
              </div>
            `).join("")}
          </div>
        </div>`
      : "";
    return `
      <div class="sheet-backdrop" data-detail-backdrop>
        <article class="detail-sheet" data-detail-sheet tabindex="-1" role="dialog" aria-modal="true" aria-label="${this.escapeAttr(item.title)} details">
          <div class="sheet-header">
            <div class="sheet-mark">${this.renderMark(item)}</div>
            <div class="sheet-copy">
              <div class="sheet-title-line">
                <div class="sheet-title">${this.escape(item.title)}</div>
                <div class="pill ${this.escapeAttr(item.state)}">${this.escape(stateLabel)}</div>
              </div>
              <div class="sheet-subtitle">${this.escape(item.group || "House")} · ${this.escape(this.metaLine(item) || "Current notice")}</div>
            </div>
            <button class="sheet-close" data-close-detail aria-label="Close details"><ha-icon icon="mdi:close"></ha-icon></button>
          </div>
          <div class="sheet-body">
            <div class="sheet-section">
              <div class="sheet-section-title">What this means</div>
              <div class="sheet-summary">${this.escape(detail.summary)}</div>
            </div>
            ${facts}
            ${after}
            ${timeline}
            <div class="sheet-actions">
              ${this.renderSheetActions(item)}
            </div>
          </div>
        </article>
      </div>
    `;
  }

  noticeDetail(item) {
    const raw = item.details && typeof item.details === "object" ? item.details : {};
    const summary = raw.summary || item.narrative || this.metaLine(item) || "This notice needs a quick look.";
    const fallbackFacts = [
      this.metaLine(item),
      item.group ? `Group: ${item.group}` : "",
    ].filter(Boolean);
    const facts = Array.isArray(raw.facts) ? raw.facts.filter((fact) => this.detailLine(fact)) : fallbackFacts;
    return {
      summary,
      facts: facts.length ? facts : fallbackFacts,
      afterAction: raw.after_action || raw.afterAction || "",
      tracking: raw.tracking || "",
      timeline: Array.isArray(raw.timeline) ? raw.timeline.filter((step) => this.detailLine(step)) : [],
    };
  }

  renderSheetActions(item) {
    const actions = Array.isArray(item.actions) ? item.actions : [];
    const actionButtons = actions
      .map((action, index) => `<button class="${index === 0 ? "primary" : ""}" data-action-for="${this.escapeAttr(item.id)}" data-action-index="${index}">${this.escape(action.label || "Done")}</button>`)
      .join("");
    const open = item.url ? `<button data-open="${this.escapeAttr(item.url)}">Open page</button>` : "";
    return actionButtons || open ? `${actionButtons}${open}` : `<button data-close-detail>Close</button>`;
  }

  detailLine(value) {
    if (value && typeof value === "object") {
      const label = value.label || value.title || "";
      const body = value.value || value.text || value.fact || "";
      if (label && body) return `${label}: ${body}`;
      return String(label || body || "").trim();
    }
    return String(value || "").trim();
  }

  renderHistory(history) {
    const headerAction = history.length
      ? `<button class="history-clear-all" data-clear-history aria-label="Clear all recent notices">Clear</button>`
      : "";
    const rows = history.length
      ? history.map((event) => this.renderHistoryRow(event)).join("")
      : `<div class="empty">All quiet. Recent notices will appear here when something needs your attention.</div>`;
    return `
      <section class="section">
        <div class="section-head">
          <div class="section-title">Recent</div>
          <div class="history-head-actions">
            ${headerAction}
            <div class="section-count">14 days</div>
          </div>
        </div>
        <div class="rows">${rows}</div>
      </section>
    `;
  }

  renderHistoryRow(event) {
    const titleParts = this.splitLeadingEmoji(event.title);
    const icon = event.kind === "action" ? "mdi:gesture-tap-button" : "mdi:bell-outline";
    const mark = titleParts.emoji
      ? `<div class="mark emoji-mark"><span>${this.escape(titleParts.emoji)}</span></div>`
      : `<div class="mark"><ha-icon icon="${this.escapeAttr(icon)}"></ha-icon></div>`;
    const title = titleParts.title;
    const meta = this.formatRecentTime(event.at);
    const narrative = event.kind !== "action"
      && event.message
      && event.message !== "clear_notification"
      && event.message !== event.tag
      && event.message !== event.title
      ? event.message
      : "";
    return `
      <div class="history-swipe" data-history-swipe="${this.escapeAttr(event.id)}">
        <div class="history-clear-reveal" aria-hidden="true"><span>Clear</span></div>
        <div class="row history-row ${this.escapeAttr(event.kind)}" data-history-row="${this.escapeAttr(event.id)}">
          ${mark}
          <div class="copy">
            <div class="title">${this.escape(title)}</div>
            <div class="meta">${this.escape(meta)}</div>
            ${narrative ? `<div class="narrative">${this.escape(narrative)}</div>` : ""}
          </div>
        </div>
      </div>
    `;
  }

  bindEvents() {
    this.shadowRoot.querySelectorAll("[data-section-toggle]").forEach((head) => {
      const toggle = () => {
        const id = head.getAttribute("data-section-toggle");
        if (!id) return;
        if (this._collapsedSections.has(id)) {
          this._collapsedSections.delete(id);
        } else {
          this._collapsedSections.add(id);
        }
        this.render();
      };
      head.addEventListener("click", toggle);
      head.addEventListener("keydown", (event) => {
        if (!["Enter", " "].includes(event.key)) return;
        event.preventDefault();
        toggle();
      });
    });
    this.shadowRoot.querySelectorAll("[data-row-id]").forEach((row) => {
      row.addEventListener("click", () => {
        const id = row.getAttribute("data-row-id");
        this._expanded = this._expanded === id ? null : id;
        this.render();
      });
    });
    this.shadowRoot.querySelectorAll("[data-open]").forEach((button) => {
      button.addEventListener("click", (event) => {
        event.stopPropagation();
        this._detailItemId = null;
        this.navigate(button.getAttribute("data-open"));
      });
    });
    this.shadowRoot.querySelectorAll("[data-detail-for]").forEach((button) => {
      button.addEventListener("click", (event) => {
        event.stopPropagation();
        this._detailItemId = button.getAttribute("data-detail-for");
        this.render();
        window.requestAnimationFrame(() => this.shadowRoot.querySelector("[data-detail-sheet]")?.focus());
      });
    });
    this.shadowRoot.querySelectorAll("[data-close-detail]").forEach((button) => {
      button.addEventListener("click", (event) => {
        event.stopPropagation();
        this._detailItemId = null;
        this.render();
      });
    });
    this.shadowRoot.querySelectorAll("[data-detail-backdrop]").forEach((backdrop) => {
      backdrop.addEventListener("click", (event) => {
        if (event.target !== backdrop) return;
        this._detailItemId = null;
        this.render();
      });
    });
    this.shadowRoot.querySelectorAll("[data-detail-sheet]").forEach((sheet) => {
      sheet.addEventListener("click", (event) => event.stopPropagation());
      sheet.addEventListener("keydown", (event) => {
        if (event.key !== "Escape") return;
        this._detailItemId = null;
        this.render();
      });
    });
    this.shadowRoot.querySelectorAll("[data-action-for]").forEach((button) => {
      button.addEventListener("click", (event) => {
        event.stopPropagation();
        this.handleAction(button.getAttribute("data-action-for"), Number(button.getAttribute("data-action-index")));
      });
    });
    this.shadowRoot.querySelectorAll("[data-clear-history]").forEach((button) => {
      button.addEventListener("click", (event) => {
        event.stopPropagation();
        this.clearRecentHistory();
      });
    });
    this.bindHistorySwipe();
  }

  bindHistorySwipe() {
    this.shadowRoot.querySelectorAll("[data-history-swipe]").forEach((shell) => {
      const row = shell.querySelector("[data-history-row]");
      if (!row) return;

      let startX = 0;
      let startY = 0;
      let currentX = 0;
      let tracking = false;
      let swiping = false;
      let moved = false;
      let dismissing = false;
      const revealMax = 92;
      const dismissThreshold = 64;

      const setReveal = (distance) => {
        const reveal = Math.round(Math.max(0, Math.min(revealMax, distance)));
        const progress = reveal / revealMax;
        shell.style.setProperty("--clear-reveal", `${reveal}px`);
        shell.style.setProperty("--clear-opacity", reveal ? String(Math.min(1, 0.24 + progress * 0.76)) : "0");
        shell.style.setProperty("--clear-red-alpha", reveal ? String(Math.min(0.92, 0.2 + progress * 0.72)) : "0");
        shell.style.setProperty("--clear-label-opacity", progress > 0.58 ? String(Math.min(1, (progress - 0.58) / 0.24)) : "0");
        shell.classList.toggle("revealing", reveal > 1);
      };

      const finish = () => {
        if (!tracking) return;
        tracking = false;
        swiping = false;
        shell.classList.remove("swiping");
        row.style.transition = "";

        if (currentX < -dismissThreshold) {
          dismissing = true;
          setReveal(revealMax);
          row.style.transform = "translate3d(-110%, 0, 0)";
          row.style.opacity = "0";
          shell.classList.add("dismissing");
          window.setTimeout(() => this.dismissHistory(shell.getAttribute("data-history-swipe")), 140);
          return;
        }

        row.style.transform = "";
        setReveal(0);
      };

      row.addEventListener("pointerdown", (event) => {
        if (event.button && event.button !== 0) return;
        tracking = true;
        swiping = false;
        moved = false;
        dismissing = false;
        startX = event.clientX;
        startY = event.clientY;
        currentX = 0;
        row.style.transition = "none";
      });

      row.addEventListener("pointermove", (event) => {
        if (!tracking) return;
        const dx = event.clientX - startX;
        const dy = event.clientY - startY;
        const absX = Math.abs(dx);
        const absY = Math.abs(dy);

        if (!swiping) {
          if (absX < 8 && absY < 8) return;
          if (absY > absX + 3) {
            tracking = false;
            row.style.transition = "";
            return;
          }
          if (dx >= 0) return;
          swiping = true;
          moved = true;
          shell.classList.add("swiping");
          try {
            row.setPointerCapture(event.pointerId);
          } catch (_err) {
            // Pointer capture is best effort; swipe still works without it.
          }
        }

        moved = true;
        if (dx >= 0) {
          currentX = 0;
          setReveal(0);
          row.style.transform = "translate3d(0, 0, 0)";
          event.preventDefault();
          return;
        }

        const drag = -dx;
        const resisted = drag <= 92 ? drag * 0.68 : 62.5 + (drag - 92) * 0.28;
        currentX = -Math.round(Math.min(124, resisted));
        setReveal(-currentX);
        row.style.transform = `translate3d(${currentX}px, 0, 0)`;
        event.preventDefault();
      });

      row.addEventListener("pointerup", finish);
      row.addEventListener("pointercancel", finish);
      row.addEventListener("click", (event) => {
        if (!moved && !dismissing) return;
        event.preventDefault();
        event.stopPropagation();
        moved = false;
      });
    });
  }

  async handleAction(itemId, index) {
    const timelineState = this._hass?.states?.[this.timelineEntity];
    const items = this.normalizeItems(this.parseJson(timelineState?.attributes?.items_json, []));
    const item = items.find((candidate) => candidate.id === itemId);
    const action = item?.actions?.[index];
    if (!item || !action || !action.service) return;
    if (action.confirm && !window.confirm(`${action.label || "Run action"}?`)) return;
    const [domain, service] = String(action.service).split(".");
    if (!domain || !service) return;
    await this.recordAction(item, action);
    await this._hass.callService(domain, service, action.data || {}, action.target || {});
    this._detailItemId = null;
    this._expanded = null;
    this.render();
  }

  async recordAction(item, action) {
    if (!this._hass?.callApi) return;
    try {
      await this._hass.callApi("POST", "events/house_notice_event_recorded", {
        at: new Date().toISOString(),
        kind: "action",
        title: action.label || "Action",
        message: item.title,
        group: item.group || "notices",
        tag: item.id,
        url: item.url || "",
        severity: "info",
        action: action.service,
        source: "house-notices-card",
        recent: action.recent === true || action.keep_recent === true || action.history === "recent",
      });
    } catch (_err) {
      // The service call should still run if history recording is unavailable.
    }
  }

  async dismissHistory(historyId) {
    const historyState = this._hass?.states?.[this.historyEntity];
    const history = this.recentHistory(this.parseJson(historyState?.attributes?.events_json, []));
    const event = history.find((candidate) => candidate.id === historyId);
    if (!event || !this._hass?.callApi) return;

    this._dismissedHistoryIds.add(historyId);
    this.render();

    try {
      await this._hass.callApi("POST", "events/house_notice_event_recorded", {
        at: new Date().toISOString(),
        kind: "dismiss",
        title: "Dismissed",
        message: event.title || "",
        group: event.group || "notices",
        tag: event.tag || "",
        severity: "info",
        source: "house-notices-card",
        dismiss_at: event.at || "",
        dismiss_kind: event.kind || "",
        dismiss_tag: event.tag || "",
        dismiss_title: event.title || "",
        dismiss_message: event.message || "",
        dismiss_action: event.action || "",
        dismiss_source: event.source || "",
      });
    } catch (_err) {
      this._dismissedHistoryIds.delete(historyId);
      this.render();
    }
  }

  async clearRecentHistory() {
    const historyState = this._hass?.states?.[this.historyEntity];
    const recent = this.recentHistory(this.parseJson(historyState?.attributes?.events_json, []));
    if (!recent.length || !this._hass?.callApi) return;

    recent.forEach((event) => this._dismissedHistoryIds.add(event.id));
    this.render();

    try {
      await this._hass.callApi("POST", "events/house_notice_event_recorded", {
        at: new Date().toISOString(),
        kind: "dismiss",
        title: "Cleared recent notices",
        message: `${recent.length} recent notices`,
        group: "notices",
        tag: "recent-history",
        severity: "info",
        source: "house-notices-card",
        dismiss_all_recent: true,
      });
    } catch (_err) {
      recent.forEach((event) => this._dismissedHistoryIds.delete(event.id));
      this.render();
    }
  }

  navigate(path) {
    if (!path) return;
    history.pushState(null, "", path);
    window.dispatchEvent(new CustomEvent("location-changed", { bubbles: true, composed: true }));
  }

  escape(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  escapeAttr(value) {
    return this.escape(value).replace(/`/g, "&#096;");
  }
}

if (!customElements.get("house-notices-card")) {
  customElements.define("house-notices-card", HouseNoticesCard);
}
