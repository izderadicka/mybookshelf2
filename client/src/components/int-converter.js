let replaceRe = /[^\d]/g.compile()

export class IntValueConverter {
  fromView(val) {
    if (typeof val === 'string') {
      val = val.replace(replaceRe, '');
      let number = parseInt(val);
      if (Number.isInteger(number)) return number;
    }
    return null;
  }

  toView(val) {
    if (val !== null && val !== undefined) return val.toString();
    return val;
  }
}
