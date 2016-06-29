export class ListValueConverter {
  toView(list) {
    if (!list || !list.length) return '';
    return list.join(', ');
  }
}
