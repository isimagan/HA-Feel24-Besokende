class Feel24MoreInfo extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          color: var(--primary-text-color);
          font-family: var(--paper-font-body1_-_font-family, inherit);
        }

        .content {
          display: grid;
          justify-items: center;
          gap: 26px;
          padding: 54px 32px 60px;
        }

        .logo-surface {
          display: grid;
          place-items: center;
          width: min(78%, 300px);
          padding: 14px 18px;
          border-radius: 14px;
          background: rgb(0 0 0 / 6%);
        }

        :host([dark-mode]) .logo-surface {
          background: transparent;
        }

        .logo {
          display: block;
          width: 100%;
          height: auto;
        }

        .copy {
          display: grid;
          justify-items: center;
          gap: 8px;
        }

        .reading {
          margin: 0;
          text-align: center;
          font-size: clamp(18px, 4.5vw, 24px);
          font-weight: 400;
          line-height: 1.3;
        }

        .reading strong {
          font-weight: 500;
        }

        .updated {
          margin: 0;
          color: var(--secondary-text-color);
          font-size: 13px;
          font-weight: 400;
          line-height: 1.4;
        }

        .notification {
          display: flex;
          align-items: center;
          width: min(100%, 360px);
          padding: 10px 4px 10px 16px;
          box-sizing: border-box;
          border: 1px solid var(--divider-color);
          border-radius: 14px;
          background: var(--card-background-color);
        }

        .notification[hidden] {
          display: none;
        }

        .notification-config {
          display: grid;
          flex: 1;
          gap: 3px;
          min-width: 0;
          padding: 4px 12px 4px 0;
          border: 0;
          background: none;
          color: inherit;
          font: inherit;
          text-align: left;
          cursor: pointer;
        }

        .notification-name {
          font-size: 16px;
          font-weight: 500;
        }

        .notification-status {
          color: var(--secondary-text-color);
          font-size: 13px;
        }

        .notification-toggle {
          position: relative;
          display: inline-flex;
          flex: 0 0 auto;
          width: 46px;
          height: 28px;
          margin: 0 8px;
        }

        .notification-toggle input {
          width: 1px;
          height: 1px;
          margin: 0;
          opacity: 0;
        }

        .notification-slider {
          position: absolute;
          inset: 0;
          border-radius: 14px;
          background: var(--switch-unchecked-track-color, rgb(120 120 120 / 45%));
          cursor: pointer;
          transition: background 160ms ease;
        }

        .notification-slider::after {
          content: "";
          position: absolute;
          top: 4px;
          left: 4px;
          width: 20px;
          height: 20px;
          border-radius: 50%;
          background: var(--switch-unchecked-button-color, white);
          box-shadow: 0 1px 3px rgb(0 0 0 / 35%);
          transition: transform 160ms ease;
        }

        .notification-toggle input:checked + .notification-slider {
          background: var(--switch-checked-track-color, var(--primary-color));
        }

        .notification-toggle input:checked + .notification-slider::after {
          transform: translateX(18px);
        }

        .notification-toggle input:focus-visible + .notification-slider {
          outline: 2px solid var(--primary-color);
          outline-offset: 2px;
        }

        .notification-toggle input:disabled + .notification-slider {
          cursor: wait;
          opacity: 0.55;
        }

        .visually-hidden {
          position: absolute;
          width: 1px;
          height: 1px;
          padding: 0;
          margin: -1px;
          overflow: hidden;
          clip: rect(0, 0, 0, 0);
          white-space: nowrap;
          border: 0;
        }

        @media (max-width: 430px) {
          .content {
            padding: 46px 24px 52px;
          }
        }
      </style>
      <div class="content">
        <div class="logo-surface">
          <img class="logo" alt="Feel24" />
        </div>
        <div class="copy" aria-live="polite">
          <p class="reading"></p>
          <p class="updated"></p>
        </div>
        <div class="notification" hidden>
          <button class="notification-config" type="button">
            <span class="notification-name">Varsel</span>
            <span class="notification-status"></span>
          </button>
          <label class="notification-toggle">
            <span class="visually-hidden">Slå varsling av eller på</span>
            <input type="checkbox" role="switch" />
            <span class="notification-slider" aria-hidden="true"></span>
          </label>
        </div>
      </div>
    `;

    this._logo = this.shadowRoot.querySelector(".logo");
    this._reading = this.shadowRoot.querySelector(".reading");
    this._updated = this.shadowRoot.querySelector(".updated");
    this._notification = this.shadowRoot.querySelector(".notification");
    this._notificationStatus =
      this.shadowRoot.querySelector(".notification-status");
    this._notificationToggle =
      this.shadowRoot.querySelector(".notification-toggle input");

    this.shadowRoot
      .querySelector(".notification-config")
      .addEventListener("click", () => this._openNotificationConfig());
    this._notificationToggle.addEventListener("change", (event) =>
      this._toggleNotification(event)
    );
  }

  connectedCallback() {
    this._setDefaultSectionsHidden(true);
  }

  disconnectedCallback() {
    this._setDefaultSectionsHidden(false);
  }

  _setDefaultSectionsHidden(hidden) {
    const moreInfoContent = this.getRootNode()?.host;
    const moreInfoInfo = moreInfoContent?.getRootNode()?.host;
    const defaultContent = moreInfoInfo?.shadowRoot?.querySelector(".content");

    for (const selector of ["state-card-content", "ha-more-info-history"]) {
      const element = defaultContent?.querySelector(selector);
      if (element) {
        element.hidden = hidden;
      }
    }
  }

  set hass(value) {
    this._hass = value;
    this.toggleAttribute("dark-mode", Boolean(value?.themes?.darkMode));
    this._update();
  }

  set stateObj(value) {
    this._stateObj = value;
    this._update();
  }

  set entry(value) {
    this._entry = value;
    this._update();
  }

  set editMode(value) {
    this._editMode = value;
  }

  set data(value) {
    this._data = value;
  }

  _update() {
    if (!this._stateObj) {
      return;
    }

    const attributes = this._stateObj.attributes ?? {};
    const state = this._stateObj.state ?? "—";
    const unit = attributes.unit_of_measurement ?? "besøkende";
    const place = attributes.sted ?? "";
    const logoPath = attributes.logo_path ?? "";

    this._logo.src = logoPath;
    this._logo.hidden = !logoPath;

    this._reading.replaceChildren();
    this._reading.append(this._strong(state), ` ${unit}`);
    if (place) {
      this._reading.append(" på ", this._strong(place));
    }

    const updated = this._formatTime(
      this._stateObj.last_updated ?? this._stateObj.last_changed
    );
    this._updated.textContent = `Sist oppdatert: ${updated}`;
    this._updateNotification();
  }

  _updateNotification() {
    this._notificationEntityId = this._findNotificationEntity();
    const stateObj = this._hass?.states?.[this._notificationEntityId];

    this._notification.hidden = !stateObj;
    if (!stateObj) {
      return;
    }

    const isOn = stateObj.state === "on";
    this._notificationToggle.checked = isOn;
    const status =
      typeof this._hass.formatEntityState === "function"
        ? this._hass.formatEntityState(stateObj)
        : isOn
          ? "På"
          : "Av";
    this._notificationStatus.textContent =
      `${status} · Trykk for å konfigurere`;
  }

  _findNotificationEntity() {
    const configEntryId = this._entry?.config_entry_id;
    if (!configEntryId || !this._hass?.entities) {
      return undefined;
    }

    return Object.entries(this._hass.entities).find(
      ([entityId, entry]) =>
        entityId.startsWith("switch.") &&
        entry.platform === "feel24_visitors" &&
        entry.config_entry_id === configEntryId &&
        entry.unique_id?.endsWith("_varsel")
    )?.[0];
  }

  async _toggleNotification(event) {
    if (!this._notificationEntityId) {
      return;
    }

    const toggle = event.currentTarget;
    toggle.disabled = true;

    try {
      await this._hass.callService(
        "switch",
        toggle.checked ? "turn_on" : "turn_off",
        {},
        { entity_id: this._notificationEntityId }
      );
    } catch (_error) {
      toggle.checked = !toggle.checked;
    } finally {
      toggle.disabled = false;
    }
  }

  _openNotificationConfig() {
    const configEntryId = this._entry?.config_entry_id;
    if (!configEntryId) {
      return;
    }

    let navigated = false;
    const navigateToConfig = () => {
      if (navigated) {
        return;
      }
      navigated = true;
      window.removeEventListener("dialog-closed", navigateToConfig);

      const currentPath =
        window.location.pathname + window.location.search + window.location.hash;
      const path =
        "/config/integrations/dashboard#config_entry=" +
        encodeURIComponent(configEntryId);

      window.history.pushState({ from: currentPath }, "", path);
      window.dispatchEvent(
        new CustomEvent("location-changed", {
          detail: { replace: false },
        })
      );
    };

    window.addEventListener("dialog-closed", navigateToConfig, { once: true });
    this.dispatchEvent(
      new CustomEvent("close-dialog", { bubbles: true, composed: true })
    );
    window.setTimeout(navigateToConfig, 500);
  }

  _strong(value) {
    const element = document.createElement("strong");
    element.textContent = value;
    return element;
  }

  _formatTime(value) {
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) {
      return "—";
    }

    const language = this._hass?.locale?.language ?? navigator.language;
    const options = {
      hour: "2-digit",
      minute: "2-digit",
    };

    if (this._hass?.config?.time_zone) {
      options.timeZone = this._hass.config.time_zone;
    }
    if (this._hass?.locale?.time_format === "12") {
      options.hour12 = true;
    } else if (this._hass?.locale?.time_format === "24") {
      options.hour12 = false;
    }

    return new Intl.DateTimeFormat(language, options).format(date);
  }
}

if (!customElements.get("feel24-more-info")) {
  customElements.define("feel24-more-info", Feel24MoreInfo);
}
