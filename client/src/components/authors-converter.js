export class AuthorsValueConverter {
  toView(val) {
    if (!val) return '';
    return val.map(a => a.first_name ? `${a.first_name} ${a.last_name}`: a.last_name).join(', ');
  }
}
