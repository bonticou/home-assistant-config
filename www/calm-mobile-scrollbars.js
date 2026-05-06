(() => {
  const ACTIVE_CLASS = "calm-mobile-scrollbar-clean";
  const STYLE_ATTR = "data-calm-mobile-scrollbars";
  const ACTIVE_PATH_PREFIX = "/calm-mobile";
  const styleByRoot = new Map();
  const observerByRoot = new Map();
  let active = false;
  let scheduled = false;
  let viewRecoveryScheduled = false;
  let attachShadowPatched = false;

  const documentCss = `
    html.${ACTIVE_CLASS} *,
    html.${ACTIVE_CLASS} {
      scrollbar-width: none !important;
      -ms-overflow-style: none !important;
    }
    html.${ACTIVE_CLASS} *::-webkit-scrollbar,
    html.${ACTIVE_CLASS}::-webkit-scrollbar,
    html.${ACTIVE_CLASS} body::-webkit-scrollbar {
      display: none !important;
      width: 0 !important;
      height: 0 !important;
      background: transparent !important;
    }
  `;

  const shadowCss = `
    :host,
    * {
      scrollbar-width: none !important;
      -ms-overflow-style: none !important;
    }
    :host::-webkit-scrollbar,
    *::-webkit-scrollbar {
      display: none !important;
      width: 0 !important;
      height: 0 !important;
      background: transparent !important;
    }
    .content::-webkit-scrollbar,
    #view::-webkit-scrollbar {
      display: none !important;
      width: 0 !important;
      height: 0 !important;
      background: transparent !important;
    }
  `;

  const isCalmMobilePath = () => {
    const path = window.location.pathname.replace(/\/+$/, "");
    return path === ACTIVE_PATH_PREFIX || path.startsWith(`${ACTIVE_PATH_PREFIX}/`);
  };

  const styleTargetFor = (root) => {
    if (root === document) {
      return document.head || document.documentElement;
    }
    return root;
  };

  const cssForRoot = (root) => (root === document ? documentCss : shadowCss);

  const ensureStyle = (root) => {
    if (!active || styleByRoot.has(root)) return;
    const target = styleTargetFor(root);
    if (!target) return;

    const style = document.createElement("style");
    style.setAttribute(STYLE_ATTR, "");
    style.textContent = cssForRoot(root);
    target.appendChild(style);
    styleByRoot.set(root, style);
  };

  const observeRoot = (root) => {
    if (!active || observerByRoot.has(root) || !root.querySelectorAll) return;
    const observer = new MutationObserver((records) => {
      for (const record of records) {
        for (const node of record.addedNodes) {
          scanNode(node);
        }
      }
    });
    observer.observe(root, { childList: true, subtree: true });
    observerByRoot.set(root, observer);
  };

  const scanRoot = (root) => {
    if (!active || !root) return;
    ensureStyle(root);
    observeRoot(root);

    if (!root.querySelectorAll) return;
    for (const element of root.querySelectorAll("*")) {
      if (element.shadowRoot) {
        scanRoot(element.shadowRoot);
      }
    }
  };

  const scanNode = (node) => {
    if (!active || node.nodeType !== Node.ELEMENT_NODE) return;
    if (node.shadowRoot) {
      scanRoot(node.shadowRoot);
    }
    if (!node.querySelectorAll) return;
    for (const element of node.querySelectorAll("*")) {
      if (element.shadowRoot) {
        scanRoot(element.shadowRoot);
      }
    }
  };

  const findDeep = (root, selector) => {
    if (!root?.querySelector) return null;
    const match = root.querySelector(selector);
    if (match) return match;
    for (const element of root.querySelectorAll("*")) {
      if (element.shadowRoot) {
        const shadowMatch = findDeep(element.shadowRoot, selector);
        if (shadowMatch) return shadowMatch;
      }
    }
    return null;
  };

  const selectedViewIndexFor = (huiRoot) => {
    const views = huiRoot?.config?.views || [];
    const path = huiRoot?.route?.path?.split("/").filter(Boolean)[0];
    if (!path) return 0;
    const numericPath = Number(path);
    const index = views.findIndex((view, viewIndex) => (
      view.path === path || (Number.isFinite(numericPath) && viewIndex === numericPath)
    ));
    return index >= 0 ? index : 0;
  };

  const recoverEmptyLovelaceView = () => {
    viewRecoveryScheduled = false;
    if (!active || !isCalmMobilePath()) return;

    const huiRoot = findDeep(document, "hui-root");
    const viewRoot = huiRoot?._viewRoot || huiRoot?.shadowRoot?.querySelector("#view");
    if (
      !huiRoot?.hass ||
      !huiRoot?.lovelace ||
      !huiRoot?.config?.views?.length ||
      typeof huiRoot._selectView !== "function" ||
      !viewRoot ||
      viewRoot.querySelector("hui-view")
    ) {
      return;
    }

    // HA can occasionally hard-load the dashboard shell without mounting the
    // selected view. Keep this scoped to calm-mobile and only repair emptiness.
    huiRoot._viewCache = huiRoot._viewCache || {};
    huiRoot._selectView(selectedViewIndexFor(huiRoot), true);
  };

  const scheduleViewRecovery = () => {
    if (viewRecoveryScheduled) return;
    viewRecoveryScheduled = true;
    [150, 500, 1200].forEach((delay) => {
      window.setTimeout(recoverEmptyLovelaceView, delay);
    });
  };

  const removeStylesAndObservers = () => {
    for (const style of styleByRoot.values()) {
      style.remove();
    }
    styleByRoot.clear();

    for (const observer of observerByRoot.values()) {
      observer.disconnect();
    }
    observerByRoot.clear();

    document.documentElement.classList.remove(ACTIVE_CLASS);
    document.body?.classList.remove(ACTIVE_CLASS);
  };

  const patchAttachShadow = () => {
    if (attachShadowPatched) return;
    attachShadowPatched = true;
    const originalAttachShadow = Element.prototype.attachShadow;
    Element.prototype.attachShadow = function patchedAttachShadow(init) {
      const shadowRoot = originalAttachShadow.call(this, init);
      if (active) {
        requestAnimationFrame(() => scanRoot(shadowRoot));
      }
      return shadowRoot;
    };
  };

  const activate = () => {
    active = true;
    document.documentElement.classList.add(ACTIVE_CLASS);
    document.body?.classList.add(ACTIVE_CLASS);
    patchAttachShadow();
    scanRoot(document);
    scheduleViewRecovery();
    logAuditIfEnabled();
  };

  const deactivate = () => {
    active = false;
    removeStylesAndObservers();
  };

  const refresh = () => {
    scheduled = false;
    const shouldBeActive = isCalmMobilePath();
    if (shouldBeActive) {
      activate();
      scheduleViewRecovery();
    } else if (active || styleByRoot.size) {
      deactivate();
    }
  };

  const scheduleRefresh = () => {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(refresh);
  };

  const patchHistory = () => {
    for (const method of ["pushState", "replaceState"]) {
      const original = history[method];
      history[method] = function patchedHistoryMethod(...args) {
        const result = original.apply(this, args);
        scheduleRefresh();
        return result;
      };
    }
    window.addEventListener("popstate", scheduleRefresh);
    window.addEventListener("location-changed", scheduleRefresh);
  };

  const describeElement = (element) => {
    if (!element) return "";
    const id = element.id ? `#${element.id}` : "";
    const classes = element.classList?.length ? `.${Array.from(element.classList).join(".")}` : "";
    return `${element.localName || element.nodeName}${id}${classes}`;
  };

  const collectScrollers = (
    root,
    label = "document",
    results = [],
    seenRoots = new WeakSet(),
    seenElements = new WeakSet(),
  ) => {
    if (!root || seenRoots.has(root)) return results;
    seenRoots.add(root);

    const elements = [];
    if (root === document) {
      elements.push(document.documentElement, document.body, document.scrollingElement);
    } else if (root.host) {
      elements.push(root.host);
    }

    if (root.querySelectorAll) {
      elements.push(...root.querySelectorAll("*"));
    }

    for (const element of elements.filter(Boolean)) {
      if (seenElements.has(element)) continue;
      seenElements.add(element);

      const style = getComputedStyle(element);
      const overflowY = style.overflowY;
      const scrollable = element.scrollHeight > element.clientHeight + 1;
      const scrollMode = ["auto", "scroll", "overlay"].includes(overflowY);
      if (scrollable && scrollMode) {
        results.push({
          root: label,
          element: describeElement(element),
          overflowY,
          scrollbarWidth: style.scrollbarWidth || "",
          clientHeight: element.clientHeight,
          scrollHeight: element.scrollHeight,
        });
      }
      if (element.shadowRoot) {
        collectScrollers(
          element.shadowRoot,
          `${label} > ${describeElement(element)}#shadowRoot`,
          results,
          seenRoots,
          seenElements,
        );
      }
    }
    return results;
  };

  window.calmMobileScrollbarAudit = () => {
    const results = collectScrollers(document);
    console.table(results);
    return results;
  };

  const logAuditIfEnabled = () => {
    if (window.localStorage?.getItem("calmMobileScrollbarAudit") !== "1") return;
    window.setTimeout(() => {
      console.info("[calm-mobile-scrollbars] active on", window.location.pathname);
      window.calmMobileScrollbarAudit();
    }, 250);
  };

  window.calmMobileScrollbarRefresh = () => {
    refresh();
    scheduleViewRecovery();
    return {
      active,
      path: window.location.pathname,
      calmMobile: isCalmMobilePath(),
    };
  };

  try {
    patchHistory();
  } catch (error) {
    console.warn("[calm-mobile-scrollbars] history patch skipped", error);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", window.calmMobileScrollbarRefresh, { once: true });
  } else {
    window.calmMobileScrollbarRefresh();
  }
  window.addEventListener("load", window.calmMobileScrollbarRefresh, { once: true });
})();
