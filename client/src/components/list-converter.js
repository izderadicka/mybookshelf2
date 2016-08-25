export class ListValueConverter {
  toView(list, prop) {
    if (!list || !list.length) return '';
    if (prop) list = list.map(i => i[prop]);
    return list.join(', ');
  }
}
