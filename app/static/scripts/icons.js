class HomeIcon extends HTMLElement {
  constructor() { super(); }
  connectedCallback() {
      this.outerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/>
          <path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
        </svg>
      `;
  }
}
customElements.define('x-home-icon', HomeIcon);

class CompassIcon extends HTMLElement {
  constructor() { super(); }
  connectedCallback() {
      this.outerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="m16.24 7.76-1.804 5.411a2 2 0 0 1-1.265 1.265L7.76 16.24l1.804-5.411a2 2 0 0 1 1.265-1.265z"/>
          <circle cx="12" cy="12" r="10"/>
        </svg>
      `;
  }
}
customElements.define('x-compass-icon', CompassIcon);

class Clock3Icon extends HTMLElement {
  constructor() { super(); }
  connectedCallback() {
      this.outerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"/>
          <polyline points="12 6 12 12 16.5 12"/>
        </svg>
      `;
  }
}
customElements.define('x-clock3-icon', Clock3Icon);

class StarIcon extends HTMLElement {
  constructor() { super(); }
  connectedCallback() {
      this.outerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
        </svg>
      `;
  }
}
customElements.define('x-star-icon', StarIcon);

class HeartIcon extends HTMLElement {
  constructor() { super(); }
  connectedCallback() {
      this.outerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>
        </svg>
      `;
  }
}
customElements.define('x-heart-icon', HeartIcon);

class PlusSquareIcon extends HTMLElement {
  constructor() { super(); }
  connectedCallback() {
      this.outerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect width="18" height="18" x="3" y="3" rx="2"/>
          <path d="M8 12h8"/>
          <path d="M12 8v8"/>
        </svg>
      `;
  }
}
customElements.define('x-plus-square-icon', PlusSquareIcon);

class PlusCheckIcon extends HTMLElement {
  constructor() { super(); }
  connectedCallback() {
      this.outerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect width="18" height="18" x="3" y="3" rx="2"/>
          <path d="m9 12 2 2 4-4"/>
        </svg>
      `;
  }
}
customElements.define('x-plus-check-icon', PlusCheckIcon);

class SettingsIcon extends HTMLElement {
  constructor() { super(); }
  connectedCallback() {
      this.outerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/>
        <circle cx="12" cy="12" r="3"/>
        </svg>
      `;
  }
}
customElements.define('x-settings-icon', SettingsIcon);

class LogOutIcon extends HTMLElement {
  constructor() { super(); }
  connectedCallback() {
      this.outerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
          <polyline points="16 17 21 12 16 7"/>
          <line x1="21" x2="9" y1="12" y2="12"/>
        </svg>
      `;
  }
}
customElements.define('x-log-out-icon', LogOutIcon);

class DownIcon extends HTMLElement {
  constructor() { 
    super(); 
  }

  connectedCallback() {
    this.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0;">
        <path d="m6 9 6 6 6-6"/>
      </svg>
    `;

    this.update();
  }

  static get observedAttributes() {
    return ['style', 'class'];
  } 

  update() {
    // Update the style attribute
    if (this.hasAttribute('style')) {
      this.style.cssText = this.getAttribute('style');
    }

    // Update the class attribute
    if (this.hasAttribute('class')) {
      this.className = this.getAttribute('class');
    }
  }
}
customElements.define('x-down-icon', DownIcon);

class UserIcon extends HTMLElement {
  constructor() { super(); }
  connectedCallback() {
    this.outerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/>
        <circle cx="12" cy="7" r="4"/>
      </svg>
    `;
  }
}
customElements.define('x-user-icon', UserIcon);
