
export function dispatchCustomEvent(event_name, elem, data) {
  let anEvent;
  if (window.CustomEvent) {
      anEvent = new CustomEvent(event_name, {
          detail: data,
          bubbles: true
      });
  } else {
      anEvent = document.createEvent('CustomEvent');
      anEvent.initCustomEvent(event_name, true, true, {
          detail: data
      });
  }
  elem.dispatchEvent(anEvent);
}


export function rewriteURLParam(name, value) {
  let hash = window.location.hash;
  let parts=hash.split('?');
  if (value) {
    window.location.hash=parts[0]+`?${name}=${value}`
  } else {
    window.location.hash=parts[0];
  }
}
