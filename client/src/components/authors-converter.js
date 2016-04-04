export class AuthorsValueConverter {
  toView(val) {
    if (!val) return '';
    return val.map(a => a.firstname ? `${a.firstname} ${a.lastname}`: a.lastname).join(', ');
  }
}
