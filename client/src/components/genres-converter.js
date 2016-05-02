export class GenresValueConverter {
  toView(val) {
    if (!val) return '';
    return val.map(g => g.name).join(', ');
  }
}
